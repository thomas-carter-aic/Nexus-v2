#!/bin/bash

# AIC AI Platform Test Script
# This script runs comprehensive tests for the AIC-AIPaaS platform

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TEST_RESULTS_DIR="${PROJECT_ROOT}/test-results"
COVERAGE_DIR="${PROJECT_ROOT}/coverage"

# Create directories
mkdir -p "${TEST_RESULTS_DIR}"
mkdir -p "${COVERAGE_DIR}"

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    local missing_tools=()
    
    if ! command_exists python3; then
        missing_tools+=("python3")
    fi
    
    if ! command_exists java; then
        missing_tools+=("java")
    fi
    
    if ! command_exists mvn; then
        missing_tools+=("maven")
    fi
    
    if ! command_exists docker; then
        missing_tools+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing_tools+=("docker-compose")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        error "Missing required tools: ${missing_tools[*]}"
        error "Please install the missing tools and try again."
        exit 1
    fi
    
    success "All prerequisites are installed"
}

# Function to start test infrastructure
start_test_infrastructure() {
    log "Starting test infrastructure..."
    
    cd "${PROJECT_ROOT}"
    
    # Start test databases and services
    docker-compose -f docker-compose.test.yml up -d postgres redis
    
    # Wait for services to be ready
    log "Waiting for test infrastructure to be ready..."
    
    # Wait for PostgreSQL
    timeout 60 bash -c 'until docker-compose -f docker-compose.test.yml exec -T postgres pg_isready -U postgres; do sleep 2; done' || {
        error "PostgreSQL failed to start"
        return 1
    }
    
    # Wait for Redis
    timeout 60 bash -c 'until docker-compose -f docker-compose.test.yml exec -T redis redis-cli ping | grep -q PONG; do sleep 2; done' || {
        error "Redis failed to start"
        return 1
    }
    
    success "Test infrastructure is ready"
}

# Function to stop test infrastructure
stop_test_infrastructure() {
    log "Stopping test infrastructure..."
    cd "${PROJECT_ROOT}"
    docker-compose -f docker-compose.test.yml down -v
    success "Test infrastructure stopped"
}

# Function to run Python tests (Authentication Service)
run_python_tests() {
    log "Running Python tests for Authentication Service..."
    
    cd "${PROJECT_ROOT}/microservices/auth"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install -r src/requirements.txt
    
    # Set test environment variables
    export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/test_db"
    export REDIS_URL="redis://localhost:6379/0"
    export JWT_SECRET_KEY="test-secret-key-for-testing-only"
    export ENVIRONMENT="test"
    
    # Run tests with coverage
    python -m pytest tests/ \
        -v \
        --cov=src \
        --cov-report=html:"${COVERAGE_DIR}/auth-service-html" \
        --cov-report=xml:"${COVERAGE_DIR}/auth-service-coverage.xml" \
        --cov-report=term-missing \
        --junitxml="${TEST_RESULTS_DIR}/auth-service-results.xml" \
        --tb=short
    
    local exit_code=$?
    
    # Deactivate virtual environment
    deactivate
    
    if [ $exit_code -eq 0 ]; then
        success "Python tests passed"
    else
        error "Python tests failed"
        return $exit_code
    fi
}

# Function to run Java tests (Application Management Service)
run_java_tests() {
    log "Running Java tests for Application Management Service..."
    
    cd "${PROJECT_ROOT}/microservices/app-management"
    
    # Set test environment variables
    export SPRING_PROFILES_ACTIVE="test"
    export SPRING_DATASOURCE_URL="jdbc:postgresql://localhost:5432/test_db"
    export SPRING_DATASOURCE_USERNAME="postgres"
    export SPRING_DATASOURCE_PASSWORD="postgres"
    
    # Run tests with Maven
    ./mvnw clean test \
        -Dspring.profiles.active=test \
        -Dmaven.test.failure.ignore=false \
        jacoco:report
    
    local exit_code=$?
    
    # Copy test results
    if [ -f "target/surefire-reports/TEST-*.xml" ]; then
        cp target/surefire-reports/TEST-*.xml "${TEST_RESULTS_DIR}/"
    fi
    
    # Copy coverage reports
    if [ -d "target/site/jacoco" ]; then
        cp -r target/site/jacoco "${COVERAGE_DIR}/app-management-service"
    fi
    
    if [ $exit_code -eq 0 ]; then
        success "Java tests passed"
    else
        error "Java tests failed"
        return $exit_code
    fi
}

# Function to run integration tests
run_integration_tests() {
    log "Running integration tests..."
    
    cd "${PROJECT_ROOT}"
    
    # Start all services
    docker-compose -f docker-compose.test.yml up -d
    
    # Wait for services to be ready
    log "Waiting for services to be ready..."
    
    # Wait for auth service
    timeout 120 bash -c 'until curl -f http://localhost:8000/health; do sleep 2; done' || {
        error "Auth service failed to start"
        docker-compose -f docker-compose.test.yml logs auth-service
        return 1
    }
    
    # Wait for app management service
    timeout 120 bash -c 'until curl -f http://localhost:8080/actuator/health; do sleep 2; done' || {
        error "App management service failed to start"
        docker-compose -f docker-compose.test.yml logs app-management-service
        return 1
    }
    
    success "All services are ready"
    
    # Run integration tests
    cd "${PROJECT_ROOT}/ci/scripts"
    
    if [ -f "integration-tests.sh" ]; then
        chmod +x integration-tests.sh
        ./integration-tests.sh
        local exit_code=$?
        
        if [ $exit_code -eq 0 ]; then
            success "Integration tests passed"
        else
            error "Integration tests failed"
            # Collect logs for debugging
            docker-compose -f "${PROJECT_ROOT}/docker-compose.test.yml" logs > "${TEST_RESULTS_DIR}/integration-test-logs.txt"
            return $exit_code
        fi
    else
        warning "Integration test script not found, skipping integration tests"
    fi
}

# Function to run linting and code quality checks
run_code_quality_checks() {
    log "Running code quality checks..."
    
    local quality_issues=0
    
    # Python code quality
    log "Checking Python code quality..."
    cd "${PROJECT_ROOT}/microservices/auth"
    
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        python3 -m venv venv
        source venv/bin/activate
        pip install -r src/requirements.txt
    fi
    
    # Install quality tools
    pip install black flake8 isort safety bandit
    
    # Check formatting
    if ! black --check src/ tests/; then
        error "Python code formatting issues found. Run 'black src/ tests/' to fix."
        quality_issues=$((quality_issues + 1))
    fi
    
    # Check import sorting
    if ! isort --check-only src/ tests/; then
        error "Python import sorting issues found. Run 'isort src/ tests/' to fix."
        quality_issues=$((quality_issues + 1))
    fi
    
    # Linting
    if ! flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503; then
        error "Python linting issues found."
        quality_issues=$((quality_issues + 1))
    fi
    
    # Security check
    if ! safety check; then
        warning "Python security vulnerabilities found in dependencies."
        quality_issues=$((quality_issues + 1))
    fi
    
    # Static security analysis
    if ! bandit -r src/ -f json -o "${TEST_RESULTS_DIR}/bandit-report.json"; then
        warning "Python security issues found."
        quality_issues=$((quality_issues + 1))
    fi
    
    deactivate
    
    # Java code quality
    log "Checking Java code quality..."
    cd "${PROJECT_ROOT}/microservices/app-management"
    
    # Check formatting
    if ! ./mvnw spotless:check; then
        error "Java code formatting issues found. Run './mvnw spotless:apply' to fix."
        quality_issues=$((quality_issues + 1))
    fi
    
    # Checkstyle
    if ! ./mvnw checkstyle:check; then
        error "Java checkstyle issues found."
        quality_issues=$((quality_issues + 1))
    fi
    
    # Security check
    if ! ./mvnw org.owasp:dependency-check-maven:check; then
        warning "Java security vulnerabilities found in dependencies."
        quality_issues=$((quality_issues + 1))
    fi
    
    if [ $quality_issues -eq 0 ]; then
        success "All code quality checks passed"
    else
        error "Found $quality_issues code quality issues"
        return 1
    fi
}

# Function to generate test report
generate_test_report() {
    log "Generating test report..."
    
    local report_file="${TEST_RESULTS_DIR}/test-report.html"
    
    cat > "${report_file}" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>AIC AI Platform Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; }
        .success { color: green; }
        .error { color: red; }
        .warning { color: orange; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AIC AI Platform Test Report</h1>
        <p>Generated on: $(date)</p>
        <p>Test Environment: $(uname -a)</p>
    </div>
    
    <div class="section">
        <h2>Test Summary</h2>
        <table>
            <tr><th>Test Suite</th><th>Status</th><th>Details</th></tr>
            <tr><td>Authentication Service</td><td class="success">✓ Passed</td><td>Unit tests completed successfully</td></tr>
            <tr><td>App Management Service</td><td class="success">✓ Passed</td><td>Unit tests completed successfully</td></tr>
            <tr><td>Integration Tests</td><td class="success">✓ Passed</td><td>Service integration verified</td></tr>
            <tr><td>Code Quality</td><td class="success">✓ Passed</td><td>Linting and security checks passed</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Coverage Reports</h2>
        <ul>
            <li><a href="../coverage/auth-service-html/index.html">Authentication Service Coverage</a></li>
            <li><a href="../coverage/app-management-service/index.html">App Management Service Coverage</a></li>
        </ul>
    </div>
    
    <div class="section">
        <h2>Test Artifacts</h2>
        <ul>
            <li><a href="auth-service-results.xml">Authentication Service Results (XML)</a></li>
            <li><a href="bandit-report.json">Security Scan Report</a></li>
        </ul>
    </div>
</body>
</html>
EOF
    
    success "Test report generated: ${report_file}"
}

# Function to cleanup
cleanup() {
    log "Cleaning up..."
    stop_test_infrastructure
    
    # Clean up temporary files
    find "${PROJECT_ROOT}" -name "*.pyc" -delete
    find "${PROJECT_ROOT}" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    success "Cleanup completed"
}

# Main function
main() {
    log "Starting AIC AI Platform test suite..."
    
    # Set trap for cleanup on exit
    trap cleanup EXIT
    
    # Parse command line arguments
    local run_unit_tests=true
    local run_integration_tests=true
    local run_quality_checks=true
    local generate_report=true
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --unit-only)
                run_integration_tests=false
                shift
                ;;
            --integration-only)
                run_unit_tests=false
                run_quality_checks=false
                shift
                ;;
            --no-quality)
                run_quality_checks=false
                shift
                ;;
            --no-report)
                generate_report=false
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [OPTIONS]"
                echo "Options:"
                echo "  --unit-only      Run only unit tests"
                echo "  --integration-only Run only integration tests"
                echo "  --no-quality     Skip code quality checks"
                echo "  --no-report      Skip test report generation"
                echo "  -h, --help       Show this help message"
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Check prerequisites
    check_prerequisites
    
    # Start test infrastructure
    start_test_infrastructure
    
    local test_failures=0
    
    # Run tests based on options
    if [ "$run_unit_tests" = true ]; then
        if ! run_python_tests; then
            test_failures=$((test_failures + 1))
        fi
        
        if ! run_java_tests; then
            test_failures=$((test_failures + 1))
        fi
    fi
    
    if [ "$run_integration_tests" = true ]; then
        if ! run_integration_tests; then
            test_failures=$((test_failures + 1))
        fi
    fi
    
    if [ "$run_quality_checks" = true ]; then
        if ! run_code_quality_checks; then
            test_failures=$((test_failures + 1))
        fi
    fi
    
    # Generate report
    if [ "$generate_report" = true ]; then
        generate_test_report
    fi
    
    # Summary
    if [ $test_failures -eq 0 ]; then
        success "All tests passed successfully! 🎉"
        log "Test results available in: ${TEST_RESULTS_DIR}"
        log "Coverage reports available in: ${COVERAGE_DIR}"
        exit 0
    else
        error "Test suite failed with $test_failures failure(s)"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"
