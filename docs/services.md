Microservices
Auth Service (Python, FastAPI)

Purpose: User authentication, authorization, profile management.
Tech: FastAPI, Kafka, PostgreSQL/MongoDB.
Endpoints: /health, /register, /login, /logout, /password/recover, /password/change, /profile.
Run: cd services/auth-service && uvicorn main:app --host 0.0.0.0 --port 8000.

Payment Service (Go)

Purpose: Payment processing.
Tech: Go, Kafka, PostgreSQL/MongoDB.
Endpoints: /health, /process.
Run: cd services/payment-service && go run main.go.

Analytics Service (Java, Spring Boot)

Purpose: Processes analytics data.
Tech: Spring Boot, Kafka, PostgreSQL/MongoDB.
Endpoints: /health, /analytics.
Run: cd services/analytics-service && ./gradlew bootRun.

Realtime Service (Node.js, Express)

Purpose: Real-time updates.
Tech: Express, Kafka, PostgreSQL/MongoDB.
Endpoints: /health, /updates.
Run: cd services/realtime-service && npm run dev.

Billing Service (Node.js, Express)

Purpose: Billing setup and invoice payments.
Tech: Express, Kafka, MongoDB.
Endpoints: /health, /invoices.
Run: cd services/billing-service && npm run dev.

Project Service (Node.js, Express)

Purpose: Organization, team, project, task management.
Tech: Express, Kafka, MongoDB.
Endpoints: /health, /projects.
Run: cd services/project-service && npm run dev.

Communication Service (Node.js, Express)

Purpose: Notifications, chat, messaging/emails.
Tech: Express, Socket.IO, Nodemailer, Kafka.
Endpoints: /health, /email.
Run: cd services/communication-service && npm run dev.

AI Service (Node.js, Express)

Purpose: Model training, deployment, inference, dataset management.
Tech: Express, Kafka, MongoDB.
Endpoints: /health, /models.
Run: cd services/ai-service && npm run dev.
