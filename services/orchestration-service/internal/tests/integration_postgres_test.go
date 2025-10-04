package tests

import (
  "context"
  "testing"
  "time"
  "encoding/json"
  "net/http"
  "bytes"
  "fmt"
  "os/exec"
  "io/ioutil"
  "os"
  "database/sql"
  _ "github.com/lib/pq"
  dockertest "github.com/ory/dockertest/v3"
)

func TestEndToEndSagaPersistence(t *testing.T) {
  // Start Postgres via dockertest
  pool, err := dockertest.NewPool("")
  if err != nil {
    t.Fatalf("could not connect to docker: %s", err)
  }
  opts := &dockertest.RunOptions{
    Repository: "postgres",
    Tag: "15",
    Env: []string{"POSTGRES_PASSWORD=postgres","POSTGRES_USER=postgres","POSTGRES_DB=postgres"},
  }
  resource, err := pool.RunWithOptions(opts)
  if err != nil {
    t.Fatalf("could not start resource: %s", err)
  }
  defer func() { _ = pool.Purge(resource) }()

  var db *sql.DB
  if err := pool.Retry(func() error {
    var err error
    hostPort := resource.GetHostPort("5432/tcp")
    dsn := fmt.Sprintf("host=localhost port=%s user=postgres password=postgres dbname=postgres sslmode=disable", hostPort)
    db, err = sql.Open("postgres", dsn)
    if err != nil { return err }
    return db.Ping()
  }); err != nil {
    t.Fatalf("could not connect to postgres: %s", err)
  }

  // Start a simple workspace-service stub on port 9000 to accept provision calls
  srv := &http.Server{Addr: ":9000", Handler: http.DefaultServeMux}
  http.HandleFunc("/provision", func(w http.ResponseWriter, r *http.Request){
    body, _ := ioutil.ReadAll(r.Body)
    fmt.Printf("workspace received: %s\n", string(body))
    w.WriteHeader(201)
    w.Write([]byte(`{"status":"provisioning"}`))
  })
  go func(){ _ = srv.ListenAndServe() }()
  defer srv.Shutdown(context.Background())

  // Start orchestration service via 'go run' with POSTGRES_URL env
  hostPort := resource.GetHostPort("5432/tcp")
  dsn := fmt.Sprintf("postgres://postgres:postgres@localhost:%s/postgres?sslmode=disable", hostPort)
  cmd := exec.Command("go", "run", "./cmd/orchestration")
  cmd.Env = append(os.Environ(), "POSTGRES_URL="+dsn, "PORT=18080")
  cmd.Stdout = os.Stdout
  cmd.Stderr = os.Stderr
  if err := cmd.Start(); err != nil {
    t.Fatalf("failed to start orchestration: %v", err)
  }
  defer func() { _ = cmd.Process.Kill() }()

  // Wait for orchestration to be up
  time.Sleep(3 * time.Second)

  // Post a UserCreated event to orchestration
  evt := map[string]interface{}{"type":"UserCreated","payload":map[string]interface{}{"userId":"test-user-1","email":"a@b.com","createdAt":time.Now().UTC().Format(time.RFC3339)}}
  b, _ := json.Marshal(evt)
  resp, err := http.Post("http://localhost:18080/events", "application/json", bytes.NewReader(b))
  if err != nil {
    t.Fatalf("failed to post event: %v", err)
  }
  if resp.StatusCode != 202 && resp.StatusCode != 200 {
    t.Fatalf("unexpected status: %d", resp.StatusCode)
  }

  // wait for saga to be created and persisted
  time.Sleep(2 * time.Second)

  // query Postgres for saga record
  row := db.QueryRow("SELECT id,user_id,state FROM sagas LIMIT 1;" )
  var id, userId, state string
  if err := row.Scan(&id, &userId, &state); err != nil {
    t.Fatalf("failed to query saga: %v", err)
  }
  if userId != "test-user-1" {
    t.Fatalf("expected userId test-user-1 got %s", userId)
  }
  t.Logf("saga %s state=%s user=%s", id, state, userId)
}
