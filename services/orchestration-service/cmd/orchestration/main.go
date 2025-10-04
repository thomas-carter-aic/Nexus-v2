package main

import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/stdout/stdouttrace"
    "go.opentelemetry.io/otel/sdk/trace"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"

    "context"
    "github.com/Shopify/sarama"
    "github.com/redis/go-redis/v9"
    "github.com/jackc/pgx/v5/pgxpool"
    migrate "github.com/golang-migrate/migrate/v4"
    "github.com/golang-migrate/migrate/v4/database/postgres"
    _ "github.com/golang-migrate/migrate/v4/source/file""
    "encoding/json"
    "fmt"
    "io"
    "log"
    "net/http"
    "os"
    "sync"
    "time"
)

// Simple in-memory saga coordinator that listens for /events POST and starts a saga for UserCreated
type SagaState string

const (
    SagaStarted   SagaState = "started"
    SagaProvision SagaState = "provisioning_workspace"
    SagaCompleted SagaState = "completed"
    SagaFailed    SagaState = "failed"
)

type Saga struct {
    ID        string    `json:"id"`
    UserID    string    `json:"user_id"`
    State     SagaState `json:"state"`
    UpdatedAt time.Time `json:"updated_at"`
}

var (
    sagastore = make(map[string]*Saga)

var redisClient *redis.Client
var pgPool *pgxpool.Pool

    mu        sync.Mutex
)

func main() {
    // start HTTP handlers
    http.HandleFunc("/events", eventsHandler)
    http.HandleFunc("/sagas", sagasHandler)
    http.HandleFunc("/reconcile", func(w http.ResponseWriter, r *http.Request){ go reconcileStuckSagas(); w.Write([]byte("reconcile_started")); })

    // Context for goroutines
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // init redis client for saga persistence
    initRedis()
    initPostgres()

    // Start Kafka consumer if configured
    if ks := os.Getenv("KAFKA_BOOTSTRAP"); ks != "" {
        go startKafkaConsumer(ctx, ks)
        fmt.Printf("started kafka consumer for %s\n", ks)
    } else {
        fmt.Println("KAFKA_BOOTSTRAP not set; Kafka consumer disabled")
    }

    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }
    log.Printf("orchestration-service listening on :%s", port)
    http.Handle("/metrics", promhttp.Handler())
    log.Fatal(http.ListenAndServe(":"+port, nil))
}


func eventsHandler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    var ev map[string]interface{}
    if err := json.NewDecoder(r.Body).Decode(&ev); err != nil {
        http.Error(w, "invalid json", http.StatusBadRequest)
        return
    }
    // Very small router based on event type field
    et, _ := ev["type"].(string)
    if et == "" {
        if payload, ok := ev["payload"].(map[string]interface{}); ok {
            if t, ok := payload["type"].(string); ok {
                et = t
            }
        }
    }
    switch et {
    case "UserCreated":
        go handleUserCreated(ctx, ev)
        w.WriteHeader(http.StatusAccepted)
        return
    default:
        w.WriteHeader(http.StatusNoContent)
        return
    }
}

func handleUserCreated(ctx context.Context, ev map[string]interface{}) {
    // Create saga
    var userId string
    if payload, ok := ev["payload"].(map[string]interface{}); ok {
        if id, ok := payload["userId"].(string); ok {
            userId = id
        }
    }
    sagaId := fmt.Sprintf("saga-%d", time.Now().UnixNano())
    s := &Saga{ID: sagaId, UserID: userId, State: SagaStarted, UpdatedAt: time.Now()}
    // persist to redis
    if redisClient != nil { if err := saveSagaToRedis(s); err != nil { fmt.Printf("warning: failed to save saga: %v\n", err) } }
    mu.Lock()
    sagastore[sagaId] = s
    mu.Unlock()

    // move to provisioning
    updateSaga(sagaId, SagaProvision)

    // call workspace-service to provision workspace
    ok := callProvisionWorkspaceWithRetries(ctx, userId, sagaId, 3)
    if ok {
        updateSaga(sagaId, SagaCompleted)
        publishEvent("UserOnboarded", map[string]interface{}{"userId": userId, "sagaId": sagaId, "completedAt": time.Now().UTC().Format(time.RFC3339)})
    } else {
        updateSaga(sagaId, SagaFailed)
        publishEvent("SagaFailed", map[string]interface{}{"sagaId": sagaId, "userId": userId, "failedAt": time.Now().UTC().Format(time.RFC3339)})
    }
}

func updateSaga(id string, state SagaState) {
    mu.Lock()
    defer mu.Unlock()
    if s, ok := sagastore[id]; ok {
        s.State = state
        s.UpdatedAt = time.Now()
    }
}

func callProvisionWorkspace(ctx context.Context, userId string, sagaId string) bool {
    // Resolve workspace-service from env or default
    url := os.Getenv("WORKSPACE_URL")
    if url == "" {
        url = "http://localhost:9000/provision"
    }
    payload := map[string]string{"workspaceId": "ws-" + userId, "ownerId": userId, "sagaId": sagaId}
    b, _ := json.Marshal(payload)
    req, _ := http.NewRequestWithContext(ctx, "POST", url, io.NopCloser(bytesReader(b)))
    req.Header.Set("Content-Type", "application/json")
    client := &http.Client{Timeout: 10 * time.Second}
    resp, err := client.Do(req)
    if err != nil {
        log.Printf("error calling workspace: %v", err)
        return false
    }
    defer resp.Body.Close()
    return resp.StatusCode >= 200 && resp.StatusCode < 300
}

func sagasHandler(w http.ResponseWriter, r *http.Request) {
    mu.Lock()
    defer mu.Unlock()
    list := make([]*Saga, 0, len(sagastore))
    for _, s := range sagastore {
        list = append(list, s)
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(list)
}

// tiny helper to publish event to stdout (placeholder for kafka)
// publishEvent publishes to stdout or Kafka (if KAFKA_BOOTSTRAP set)
func publishEvent(eventType string, payload map[string]interface{}) {
    m := map[string]interface{}{"type": eventType, "payload": payload, "timestamp": time.Now().UTC().Format(time.RFC3339)}
    b, _ := json.Marshal(m)
    // If KAFKA_BOOTSTRAP set, publish to topic "platform-events"
    if ks := os.Getenv("KAFKA_BOOTSTRAP"); ks != "" {
        // create producer (sync) and send message
        config := sarama.NewConfig()
        config.Producer.RequiredAcks = sarama.WaitForLocal
        config.Producer.Return.Successes = true
        producer, err := sarama.NewSyncProducer([]string{ks}, config)
        if err != nil {
            fmt.Printf("kafka producer error: %v\n", err)
            fmt.Println(string(b))
            return
        }
        defer producer.Close()
        msg := &sarama.ProducerMessage{Topic: "platform-events", Value: sarama.ByteEncoder(b)}
        partition, offset, err := producer.SendMessage(msg)
        if err != nil {
            fmt.Printf("failed to send kafka message: %v\n", err)
            // attempt to send to DLQ topic
            dlqMsg := &sarama.ProducerMessage{Topic: "platform-dlq", Value: sarama.ByteEncoder(b)}
            _, _, dlqErr := producer.SendMessage(dlqMsg)
            if dlqErr != nil {
                fmt.Printf("failed to send to dlq: %v\n", dlqErr)
            }
            fmt.Println(string(b))
            return
        }
        fmt.Printf("kafka message sent partition=%d offset=%d\n", partition, offset)
        return
    }
    // fallback to stdout
    fmt.Println(string(b))
}

// bytesReader helper
type bytesReaderType struct{ b []byte; i int }
func bytesReader(b []byte) *bytesReaderType { return &bytesReaderType{b: b, i: 0} }
func (r *bytesReaderType) Read(p []byte) (int, error) {
    if r.i >= len(r.b) { return 0, io.EOF }
    n := copy(p, r.b[r.i:])
    r.i += n
    return n, nil
}
func (r *bytesReaderType) Close() error { return nil }

// Kafka consumer group handler and starter
type consumerGroupHandler struct{}

func (consumerGroupHandler) Setup(_ sarama.ConsumerGroupSession) error   { return nil }
func (consumerGroupHandler) Cleanup(_ sarama.ConsumerGroupSession) error { return nil }
func (consumerGroupHandler) ConsumeClaim(sess sarama.ConsumerGroupSession, claim sarama.ConsumerGroupClaim) error {
    for msg := range claim.Messages() {
        var m map[string]interface{}
        if err := json.Unmarshal(msg.Value, &m); err != nil {
            fmt.Printf("failed to unmarshal kafka message: %v\n", err)
            continue
        }
        et, _ := m["type"].(string)
        payload, _ := m["payload"].(map[string]interface{})
        if et == "" {
            if p, ok := m["payload"].(map[string]interface{}); ok {
                if t, ok := p["type"].(string); ok {
                    et = t
                    payload = p
                }
            }
        }
        switch et {
        case "UserCreated":
            go handleUserCreated(context.Background(), map[string]interface{}{"payload": payload})
        default:
            // ignore
        }
        sess.MarkMessage(msg, "")
    }
    return nil
}

func initRedis()
    initPostgres() {
    addr := os.Getenv("REDIS_ADDR")
    if addr == "" {
        addr = "localhost:6379"
    }
    redisClient = redis.NewClient(&redis.Options{Addr: addr})
}

func saveSagaToRedis(s *Saga) error {
    if redisClient == nil {
        return fmt.Errorf("redis not initialized")
    }
    key := "saga:" + s.ID
    b, _ := json.Marshal(s)
    return redisClient.Set(context.Background(), key, b, 0).Err()
}

func getSagaFromRedis(id string) (*Saga, error) {
    if redisClient == nil {
        return nil, fmt.Errorf("redis not initialized")
    }
    key := "saga:" + id
    val, err := redisClient.Get(context.Background(), key).Result()
    if err != nil {
        return nil, err
    }
    var s Saga
    if err := json.Unmarshal([]byte(val), &s); err != nil {
        return nil, err
    }
    return &s, nil
}



func runMigrations(migrationsPath string) error {
    dbURL := os.Getenv("POSTGRES_URL")
    if dbURL == "" {
        dbURL = "postgres://postgres:postgres@localhost:5432/postgres?sslmode=disable"
    }
    // Initialize migrate with file source and postgres driver
    d, err := postgres.WithInstance(pgPool.Config().ConnConfig, &postgres.Config{})
    if err != nil {
        // fallback: return nil so startup continues
        fmt.Printf("migrate postgres driver error: %v\n", err)
    }
    m, err := migrate.NewWithDatabaseInstance("file://"+migrationsPath, "postgres", d)
    if err != nil {
        fmt.Printf("migrate init error: %v\n", err)
        return err
    }
    if err := m.Up(); err != nil && err != migrate.ErrNoChange {
        fmt.Printf("migrate up error: %v\n", err)
        return err
    }
    fmt.Println("migrations applied (if any)")
    return nil
}


func initTracing() func() {
    // stdout exporter as simple example; replace with OTLP exporter in production
    exp, _ := stdouttrace.New(stdouttrace.WithPrettyPrint())
    tp := sdktrace.NewTracerProvider(sdktrace.WithBatcher(exp))
    otel.SetTracerProvider(tp)
    return func(){ _ = tp.Shutdown(context.Background()) }
}


func initPostgres() {
    pgURL := os.Getenv("POSTGRES_URL") // e.g. postgres://user:pass@host:5432/dbname
    if pgURL == "" {
        pgURL = "postgres://postgres:postgres@localhost:5432/postgres"
    }
    cfg, err := pgxpool.ParseConfig(pgURL)
    if err != nil {
        fmt.Printf("failed to parse postgres config: %v\n", err)
        return
    }
    pool, err := pgxpool.NewWithConfig(context.Background(), cfg)
    if err != nil {
        fmt.Printf("failed to create pg pool: %v\n", err)
        return
    }
    pgPool = pool
    // create saga table if not exists
    _, err = pgPool.Exec(context.Background(), `CREATE TABLE IF NOT EXISTS sagas (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        state TEXT,
        updated_at TIMESTAMP,
        payload JSONB
    );`)
    if err != nil {
        fmt.Printf("failed to ensure sagas table: %v\n", err)
    }
}

func saveSagaToPostgres(s *Saga) error {
    if pgPool == nil {
        return fmt.Errorf("pgPool not initialized")
    }
    payload, _ := json.Marshal(s)
    _, err := pgPool.Exec(context.Background(),
        "INSERT INTO sagas(id,user_id,state,updated_at,payload) VALUES($1,$2,$3,$4,$5) ON CONFLICT (id) DO UPDATE SET state=EXCLUDED.state, updated_at=EXCLUDED.updated_at, payload=EXCLUDED.payload",
        s.ID, s.UserID, string(s.State), s.UpdatedAt, payload)
    return err
}

func getSagaFromPostgres(id string) (*Saga, error) {
    if pgPool == nil {
        return nil, fmt.Errorf("pgPool not initialized")
    }
    var s Saga
    var payload []byte
    row := pgPool.QueryRow(context.Background(), "SELECT id,user_id,state,updated_at,payload FROM sagas WHERE id=$1", id)
    err := row.Scan(&s.ID, &s.UserID, &s.State, &s.UpdatedAt, &payload)
    if err != nil {
        return nil, err
    }
    return &s, nil
}

func reconcileStuckSagas() {
    if pgPool == nil {
        fmt.Println("pgPool not initialized; cannot reconcile")
        return
    }
    rows, err := pgPool.Query(context.Background(), "SELECT id, payload FROM sagas WHERE state=$1 OR state=$2", string(SagaStarted), string(SagaProvision))
    if err != nil {
        fmt.Printf("reconcile query failed: %v\n", err)
        return
    }
    defer rows.Close()
    for rows.Next() {
        var id string
        var payload []byte
        if err := rows.Scan(&id, &payload); err != nil {
            fmt.Printf("scan err: %v\n", err)
            continue
        }
        // naive: attempt to re-run provision for the saga's user id from payload
        var s Saga
        if err := json.Unmarshal(payload, &s); err != nil {
            fmt.Printf("unmarshal saga payload err: %v\n", err)
            continue
        }
        go func(saga *Saga) {
            fmt.Printf("reconciling saga %s user=%s\n", saga.ID, saga.UserID)
            ok := callProvisionWorkspaceWithRetries(context.Background(), saga.UserID, saga.ID, 3)
            if ok {
                saga.State = SagaCompleted
                saga.UpdatedAt = time.Now()
                if err := saveSagaToPostgres(saga); err != nil {
                    fmt.Printf("failed to save saga after reconcile: %v\n", err)
                }
                publishEvent("UserOnboarded", map[string]interface{}{"userId": saga.UserID, "sagaId": saga.ID, "completedAt": time.Now().UTC().Format(time.RFC3339)})
            } else {
                saga.State = SagaFailed
                saga.UpdatedAt = time.Now()
                if err := saveSagaToPostgres(saga); err != nil {
                    fmt.Printf("failed to save saga after reconcile failure: %v\n", err)
                }
                publishEvent("SagaFailed", map[string]interface{}{"sagaId": saga.ID, "userId": saga.UserID, "failedAt": time.Now().UTC().Format(time.RFC3339)})
            }
        }(&s)
    }
}


func startKafkaConsumer(ctx context.Context, brokers string) {
    addrs := []string{brokers}
    groupID := "orchestration-group"
    config := sarama.NewConfig()
    config.Consumer.Return.Errors = true
    config.Version = sarama.V2_1_0_0
    client, err := sarama.NewConsumerGroup(addrs, groupID, config)
    if err != nil {
        fmt.Printf("error creating consumer group: %v\n", err)
        return
    }
    go func() {
        defer client.Close()
        for {
            if err := client.Consume(ctx, []string{"platform-events"}, consumerGroupHandler{}); err != nil {
                fmt.Printf("error from consumer: %v\n", err)
            }
            if ctx.Err() != nil {
                return
            }
        }
    }()
}
