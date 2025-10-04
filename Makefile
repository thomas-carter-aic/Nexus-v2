.PHONY: help setup test clean build deploy

# Default target
help:
	@echo "AICP - Advanced Intelligent Computing Platform"
	@echo ""
	@echo "Available targets:"
	@echo "  setup          - Set up development environment"
	@echo "  test           - Run all tests"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-integration - Run integration tests"
	@echo "  test-e2e       - Run end-to-end tests"
	@echo "  build          - Build all services"
	@echo "  clean          - Clean build artifacts"
	@echo "  deploy-local   - Deploy to local Kubernetes"
	@echo "  deploy-dev     - Deploy to development environment"
	@echo "  docs           - Generate documentation"
	@echo "  lint           - Run code linting"
	@echo "  format         - Format all code"

# Development setup
setup:
	@echo "Setting up development environment..."
	./scripts/setup-dev.sh

# Testing targets
test: test-unit test-integration
	@echo "All tests completed"

test-unit:
	@echo "Running unit tests..."
	./scripts/test-unit.sh

test-integration:
	@echo "Running integration tests..."
	./scripts/test-integration.sh

test-e2e:
	@echo "Running end-to-end tests..."
	./scripts/test-e2e.sh

test-service:
ifndef SERVICE
	@echo "Usage: make test-service SERVICE=service-name"
	@exit 1
endif
	@echo "Testing service: $(SERVICE)"
	./scripts/test-service.sh $(SERVICE)

# Build targets
build:
	@echo "Building all services..."
	./scripts/build-all.sh

clean:
	@echo "Cleaning build artifacts..."
	./scripts/clean.sh

# Deployment targets
deploy-local:
	@echo "Deploying to local Kubernetes..."
	./scripts/deploy-local.sh

deploy-dev:
	@echo "Deploying to development environment..."
	./scripts/deploy-dev.sh

# Documentation
docs:
	@echo "Generating documentation..."
	./scripts/generate-docs.sh

# Code quality
lint:
	@echo "Running linters..."
	./scripts/lint.sh

format:
	@echo "Formatting code..."
	./scripts/format.sh

# Docker targets
docker-build:
	@echo "Building Docker images..."
	./scripts/docker-build.sh

docker-push:
	@echo "Pushing Docker images..."
	./scripts/docker-push.sh
