# Developer Guide - AIC AI Platform

## Getting Started

This guide will help you set up your development environment and start contributing to the AIC AI Platform (AIC-AIPaaS).

## Prerequisites

### Required Software

- **Docker**: Version 20.10 or later
- **Docker Compose**: Version 2.0 or later
- **Kubernetes**: kubectl version 1.28 or later
- **Helm**: Version 3.12 or later
- **Terraform**: Version 1.5 or later
- **Git**: Version 2.30 or later
- **Make**: GNU Make 4.0 or later

### Language-Specific Requirements

#### Python (Authentication Service)
- **Python**: Version 3.11 or later
- **pip**: Latest version
- **virtualenv** or **conda**: For environment management

#### Java (Application Management Service)
- **Java**: OpenJDK 17 or later
- **Maven**: Version 3.9 or later
- **IDE**: IntelliJ IDEA or Eclipse (recommended)

### Development Tools

- **IDE/Editor**: VS Code, IntelliJ IDEA, or your preferred editor
- **API Testing**: Postman, Insomnia, or curl
- **Database Client**: pgAdmin, DBeaver, or similar
- **Container Registry**: Docker Hub account or AWS ECR access

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/thomas-carter-aic/aic-aipaas.git
cd aic-aipaas
```

### 2. Initial Setup

Run the setup command to install dependencies and configure the development environment:

```bash
make setup
```

This command will:
- Install all required dependencies
- Set up pre-commit hooks
- Create necessary configuration files
- Initialize local databases
- Build Docker images

### 3. Environment Configuration

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your local configuration:

```env
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=aic_aipaas
POSTGRES_USER=developer
POSTGRES_PASSWORD=dev_password

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AWS Configuration (for local development)
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Monitoring
PROMETHEUS_URL=http://localhost:9090
GRAFANA_URL=http://localhost:3000
```

## Development Workflow

### 1. Starting Services Locally

Start all services in development mode:

```bash
make dev
```

This will start:
- PostgreSQL database
- Redis cache
- Authentication service (port 8000)
- Application management service (port 8080)
- Prometheus (port 9090)
- Grafana (port 3000)

### 2. Service-Specific Development

#### Authentication Service (Python/FastAPI)

```bash
cd microservices/auth

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r src/requirements.txt

# Run in development mode
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### Application Management Service (Java/Spring Boot)

```bash
cd microservices/app-management

# Run with Maven
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev

# Or build and run JAR
./mvnw clean package -DskipTests
java -jar target/app-management-service-1.0.0.jar --spring.profiles.active=dev
```

### 3. Running Tests

#### Run All Tests
```bash
make test
```

#### Service-Specific Tests

**Authentication Service:**
```bash
cd microservices/auth
python -m pytest tests/ -v --cov=src
```

**Application Management Service:**
```bash
cd microservices/app-management
./mvnw test
```

### 4. Code Quality and Linting

#### Pre-commit Hooks
Pre-commit hooks are automatically installed during setup. They will run:
- Code formatting (Black for Python, Prettier for JS/TS)
- Linting (Flake8 for Python, ESLint for JS/TS)
- Security checks
- Terraform validation

#### Manual Code Quality Checks
```bash
# Run all pre-commit hooks manually
pre-commit run --all-files

# Python-specific checks
cd microservices/auth
black src/ tests/
flake8 src/ tests/
isort src/ tests/

# Java-specific checks
cd microservices/app-management
./mvnw spotless:apply
./mvnw checkstyle:check
```

## API Development

### Authentication Service API

The authentication service provides the following endpoints:

#### Authentication Endpoints
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/me` - Get current user info
- `POST /auth/validate` - Validate JWT token

#### Example Usage

```bash
# Register a new user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "developer",
    "email": "dev@example.com",
    "password": "secure_password"
  }'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "developer",
    "password": "secure_password"
  }'
```

### Application Management Service API

#### Application Endpoints
- `GET /api/v1/applications` - List applications
- `POST /api/v1/applications` - Create application
- `GET /api/v1/applications/{id}` - Get application
- `PUT /api/v1/applications/{id}` - Update application
- `DELETE /api/v1/applications/{id}` - Delete application
- `POST /api/v1/applications/{id}/deploy` - Deploy application
- `POST /api/v1/applications/{id}/stop` - Stop application

#### Example Usage

```bash
# Get JWT token first
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "developer", "password": "secure_password"}' \
  | jq -r '.access_token')

# Create an application
curl -X POST http://localhost:8080/api/v1/applications \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My AI App",
    "description": "A sample AI application",
    "version": "1.0.0",
    "dockerImage": "myapp:latest"
  }'
```

## Database Development

### Schema Management

Database schemas are managed using migrations:

#### Authentication Service (Alembic)
```bash
cd microservices/auth

# Create a new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

#### Application Management Service (Flyway)
```bash
cd microservices/app-management

# Run migrations
./mvnw flyway:migrate

# Get migration info
./mvnw flyway:info

# Clean database (development only)
./mvnw flyway:clean
```

### Data Schemas

The platform uses JSON schemas for data validation. Schemas are located in `data/schemas/`:

- `finance.json` - Financial data schema
- `healthcare.json` - Healthcare data schema

#### Adding New Schemas

1. Create a new JSON schema file in `data/schemas/`
2. Follow JSON Schema Draft 7 specification
3. Include examples and documentation
4. Update the data catalog service to recognize the new schema

## Testing

### Testing Strategy

The platform uses a comprehensive testing strategy:

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test service interactions
3. **End-to-End Tests**: Test complete user workflows
4. **Performance Tests**: Test system performance and scalability
5. **Security Tests**: Test security vulnerabilities

### Writing Tests

#### Python Tests (pytest)

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_user_registration():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
```

#### Java Tests (JUnit 5)

```java
// tests/AppControllerTest.java
@ExtendWith(MockitoExtension.class)
@WebMvcTest(AppController.class)
class AppControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ApplicationService applicationService;

    @Test
    @WithMockUser(roles = "USER")
    void getAllApplications_ShouldReturnPagedApplications() throws Exception {
        // Given
        List<ApplicationResponse> applications = Arrays.asList(mockApplication);
        Page<ApplicationResponse> page = new PageImpl<>(applications);
        when(applicationService.getAllApplications(any(), any(), any()))
                .thenReturn(page);

        // When & Then
        mockMvc.perform(get("/api/v1/applications"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content").isArray());
    }
}
```

### Test Data Management

#### Test Fixtures

Create reusable test data:

```python
# tests/fixtures.py
@pytest.fixture
def sample_user():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }

@pytest.fixture
def authenticated_client(sample_user):
    client = TestClient(app)
    # Register and login user
    client.post("/auth/register", json=sample_user)
    response = client.post("/auth/login", json={
        "username": sample_user["username"],
        "password": sample_user["password"]
    })
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
```

## Deployment

### Local Deployment with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Start specific services
docker-compose up auth-service app-management-service

# View logs
docker-compose logs -f auth-service
```

### Kubernetes Deployment

#### Development Cluster

```bash
# Create local Kubernetes cluster (using kind)
kind create cluster --config infrastructure/kubernetes/kind-config.yaml

# Deploy to local cluster
make deploy-local
```

#### Staging/Production Deployment

```bash
# Deploy to staging
make deploy-staging

# Deploy to production
make deploy-production
```

### Helm Charts

Each service has its own Helm chart in the `helm/` directory:

```bash
# Install auth service
helm install auth-service microservices/auth/helm/

# Upgrade app management service
helm upgrade app-management microservices/app-management/helm/

# Uninstall service
helm uninstall auth-service
```

## Monitoring and Debugging

### Local Monitoring

Access monitoring tools:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Jaeger**: http://localhost:16686

### Application Logs

```bash
# View service logs
docker-compose logs -f auth-service
kubectl logs -f deployment/auth-service -n microservices

# Follow logs with filtering
kubectl logs -f -l app=auth-service --tail=100
```

### Debugging

#### Python Debugging

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use debugpy for remote debugging
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()
```

#### Java Debugging

```bash
# Run with debug mode
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -jar app.jar

# Or with Maven
./mvnw spring-boot:run -Dspring-boot.run.jvmArguments="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005"
```

## Contributing

### Git Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Commit Message Format

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(auth): add OAuth2 integration
fix(api): resolve memory leak in user service
docs(readme): update installation instructions
```

### Code Review Guidelines

1. **Code Quality**: Ensure code follows style guidelines
2. **Tests**: Include appropriate tests for new features
3. **Documentation**: Update documentation for API changes
4. **Security**: Review for security vulnerabilities
5. **Performance**: Consider performance implications

## Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check what's using a port
lsof -i :8000

# Kill process using port
kill -9 $(lsof -t -i:8000)
```

#### Database Connection Issues
```bash
# Check database status
docker-compose ps postgres

# Reset database
docker-compose down -v
docker-compose up postgres
```

#### Docker Issues
```bash
# Clean up Docker
docker system prune -a

# Rebuild images
docker-compose build --no-cache
```

### Getting Help

1. **Documentation**: Check the docs/ directory
2. **Issues**: Search existing GitHub issues
3. **Discussions**: Use GitHub Discussions for questions
4. **Slack**: Join the development Slack channel
5. **Email**: Contact the development team

## Resources

### Documentation
- [Architecture Guide](architecture.md)
- [API Specifications](api-specs/)
- [Operations Runbook](runbook.md)

### External Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Istio Documentation](https://istio.io/latest/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)

### Tools and Libraries
- [Docker](https://docs.docker.com/)
- [Helm](https://helm.sh/docs/)
- [Terraform](https://www.terraform.io/docs/)
- [pytest](https://docs.pytest.org/)
- [JUnit 5](https://junit.org/junit5/docs/current/user-guide/)
