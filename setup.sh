#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="${1:-config}"  # default to ./config
echo "Creating full monorepo config in $BASE_DIR"

# ------------------------
# Create directories
# ------------------------
mkdir -p "$BASE_DIR/monorepo/change-detection"
mkdir -p "$BASE_DIR/monorepo/dependency-management"
mkdir -p "$BASE_DIR/monorepo/orchestration"
mkdir -p "$BASE_DIR/monorepo/scripts"
mkdir -p "$BASE_DIR/services/templates/microservice-python"
mkdir -p "$BASE_DIR/services/templates/microservice-rust/src"

# ------------------------
# Change Detection Scripts
# ------------------------
cat > "$BASE_DIR/monorepo/change-detection/detect-changed-modules.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
BASE_REF="${1:-origin/main}"
echo "🔍 Detecting changed modules since $BASE_REF"
CHANGED_FILES=$(git diff --name-only "$BASE_REF"...HEAD)
if [ -z "$CHANGED_FILES" ]; then
  echo "No changes detected."
  exit 0
fi
MODULES=$(echo "$CHANGED_FILES" | grep -E '^(services/|libs/|ai/|integrations/)' | cut -d/ -f1-2 | sort -u)
if [ -z "$MODULES" ]; then
  echo "No module-level changes detected."
  exit 0
fi
echo "Changed modules:"
echo "$MODULES"
EOF
chmod +x "$BASE_DIR/monorepo/change-detection/detect-changed-modules.sh"

cat > "$BASE_DIR/monorepo/change-detection/affected-tests.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
BASE_REF="${1:-origin/main}"
CHANGED_MODULES=$(./config/monorepo/change-detection/detect-changed-modules.sh "$BASE_REF")
if [ -z "$CHANGED_MODULES" ]; then
  echo "✅ No affected tests to run."
  exit 0
fi
echo "🧪 Running tests for changed modules..."
for mod in $CHANGED_MODULES; do
  if [ -f "$mod/package.json" ]; then
    echo "Running JS/TS tests in $mod"
    (cd "$mod" && npm test || true)
  elif [ -f "$mod/pom.xml" ]; then
    echo "Running Java tests in $mod"
    (cd "$mod" && mvn test || true)
  elif [ -f "$mod/pyproject.toml" ]; then
    echo "Running Python tests in $mod"
    (cd "$mod" && pytest || true)
  elif [ -f "$mod/Cargo.toml" ]; then
    echo "Running Rust tests in $mod"
    (cd "$mod" && cargo test || true)
  elif [ -f "$mod/go.mod" ]; then
    echo "Running Go tests in $mod"
    (cd "$mod" && go test ./... || true)
  else
    echo "ℹ️ No test command defined for $mod"
  fi
done
EOF
chmod +x "$BASE_DIR/monorepo/change-detection/affected-tests.sh"

# ------------------------
# Dependency Management
# ------------------------
cat > "$BASE_DIR/monorepo/dependency-management/upgrade-deps.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "⬆️ Upgrading dependencies across the monorepo..."
find services libs -name package.json | while read -r pkg; do
  echo "Upgrading Node deps in $(dirname "$pkg")"
  (cd "$(dirname "$pkg")" && npm update)
done
find services libs -name pom.xml | while read -r pom; do
  echo "Upgrading Java deps in $(dirname "$pom")"
  (cd "$(dirname "$pom")" && mvn versions:use-latest-releases -B -q)
done
find services libs -name pyproject.toml | while read -r py; do
  echo "Upgrading Python deps in $(dirname "$py")"
  (cd "$(dirname "$py")" && pip-compile --upgrade || true)
done
find services libs -name Cargo.toml | while read -r cargo; do
  echo "Upgrading Rust deps in $(dirname "$cargo")"
  (cd "$(dirname "$cargo")" && cargo update)
done
find services libs -name go.mod | while read -r gomod; do
  echo "Upgrading Go deps in $(dirname "$gomod")"
  (cd "$(dirname "$gomod")" && go get -u ./... && go mod tidy)
done
echo "✅ Dependencies upgraded."
EOF
chmod +x "$BASE_DIR/monorepo/dependency-management/upgrade-deps.sh"

cat > "$BASE_DIR/monorepo/dependency-management/dependency-report.yaml" <<'EOF'
version: 1
generated: true
description: Cross-language dependency report.
modules:
  - name: common-lib-java
    language: java
    deps:
      - org.apache.commons:commons-lang3:3.14.0
  - name: common-lib-node
    language: node
    deps:
      - express: ^4.18.2
      - lodash: ^4.17.21
  - name: microservice-python
    language: python
    deps:
      - fastapi==0.103.1
      - uvicorn==0.23.2
  - name: microservice-rust
    language: rust
    deps:
      - actix-web: "4"
  - name: microservice-go
    language: go
    deps:
      - github.com/gorilla/mux: v1.8.0
EOF

# ------------------------
# Orchestration
# ------------------------
cat > "$BASE_DIR/monorepo/orchestration/build-order.yaml" <<'EOF'
version: 1
description: Canonical build/publish order for polyglot monorepo.
stages:
  - name: base-languages
    modules:
      - config/languages/java/maven
      - config/languages/node/npm
      - config/languages/python/pyproject.toml
      - config/languages/rust/cargo-config.toml
      - config/languages/go/go.env
      - config/runtime/docker/base/Dockerfile.base-node
      - config/runtime/docker/base/Dockerfile.base-java
      - config/runtime/docker/base/Dockerfile.base-python
      - config/runtime/docker/base/Dockerfile.base-go
  - name: shared-libraries
    modules:
      - libs/java/*
      - libs/node/*
      - libs/python/*
      - libs/rust/*
      - libs/go/*
  - name: core-services
    modules:
      - services/templates/microservice-java
      - services/templates/microservice-node
      - services/templates/microservice-go
      - services/templates/microservice-python
      - services/templates/microservice-rust
  - name: ai-platform
    modules:
      - ai/models/*
      - ai/mlops/*
      - ai/ai-platform/*
  - name: integrations
    modules:
      - integrations/oauth/*
      - integrations/billing/*
      - integrations/analytics/*
      - integrations/messaging/*
  - name: release-packaging
    modules:
      - config/packaging/deb
      - config/packaging/rpm
      - config/packaging/docker-image-metadata.yaml
      - monorepo/publishing/publish-java.sh
      - monorepo/publishing/publish-node.sh
      - monorepo/publishing/publish-go.sh
      - monorepo/publishing/publish-python.sh
      - monorepo/publishing/publish-rust.sh
EOF

cat > "$BASE_DIR/monorepo/orchestration/release-orchestrator.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
BUILD_ORDER="config/monorepo/orchestration/build-order.yaml"
if ! command -v yq &>/dev/null; then
  echo "❌ yq is required"
  exit 1
fi
echo "🚀 Starting release orchestrator"
STAGES=$(yq '.stages[].name' "$BUILD_ORDER")
for stage in $STAGES; do
  echo ""
  echo "=== Stage: $stage ==="
  MODULES=$(yq ".stages[] | select(.name==\"$stage\") | .modules[]" "$BUILD_ORDER")
  for mod in $MODULES; do
    (
      echo "🔨 Building $mod"
      ./monorepo/scripts/build-module.sh "$mod"
    ) &
  done
  wait
done
echo "✅ Release orchestration complete."
EOF
chmod +x "$BASE_DIR/monorepo/orchestration/release-orchestrator.sh"

cat > "$BASE_DIR/monorepo/scripts/build-module.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
MODULE_PATH="$1"
if [ -f "$MODULE_PATH/pom.xml" ]; then
  (cd "$MODULE_PATH" && mvn clean install -B)
elif [ -f "$MODULE_PATH/build.gradle" ] || [ -f "$MODULE_PATH/build.gradle.kts" ]; then
  (cd "$MODULE_PATH" && ./gradlew build -x test)
elif [ -f "$MODULE_PATH/package.json" ]; then
  (cd "$MODULE_PATH" && npm install && npm run build)
elif [ -f "$MODULE_PATH/pyproject.toml" ]; then
  (cd "$MODULE_PATH" && python3 -m pip install --upgrade build wheel && python3 -m build)
elif [ -f "$MODULE_PATH/Cargo.toml" ]; then
  (cd "$MODULE_PATH" && cargo build --release)
elif [ -f "$MODULE_PATH/go.mod" ]; then
  (cd "$MODULE_PATH" && go build ./...)
elif [ -f "$MODULE_PATH/Dockerfile" ] || [ -f "$MODULE_PATH/docker/Dockerfile" ]; then
  IMAGE_NAME=$(basename "$MODULE_PATH" | tr '[:upper:]' '[:lower:]')
  docker build -f "$MODULE_PATH/Dockerfile" -t "$IMAGE_NAME:latest" "$MODULE_PATH"
fi
EOF
chmod +x "$BASE_DIR/monorepo/scripts/build-module.sh"

# ------------------------
# Python Microservice Template
# ------------------------
PY_MS="$BASE_DIR/services/templates/microservice-python"
cat > "$PY_MS/pyproject.toml" <<'EOF'
[build-system]
requires = ["setuptools>=65.5.0","wheel"]
build-backend = "setuptools.build_meta"

[tool.poetry]
name = "microservice-python"
version = "0.1.0"
description = "Example Python microservice"
authors = ["Your Company <dev@company.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.103.1"
uvicorn = "^0.23.2"

[tool.poetry.dev-dependencies]
pytest = "^8.2.5"
EOF

cat > "$PY_MS/main.py" <<'EOF'
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello from microservice-python"}
EOF

cat > "$PY_MS/Dockerfile" <<'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install --upgrade pip && pip install poetry && poetry install --no-root
COPY . /app
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

cat > "$PY_MS/README.md" <<'EOF'
# Microservice Python Template
Sample Python microservice template with FastAPI and Dockerfile.
EOF

# ------------------------
# Rust Microservice Template
# ------------------------
RUST_MS="$BASE_DIR/services/templates/microservice-rust"
cat > "$RUST_MS/Cargo.toml" <<'EOF'
[package]
name = "microservice-rust"
version = "0.1.0"
edition = "2021"

[dependencies]
actix-web = "4"
tokio = { version="1", features=["full"] }
serde = { version="1.0", features=["derive"] }
serde_json = "1.0"
EOF

cat > "$RUST_MS/src/main.rs" <<'EOF'
use actix_web::{get, App, HttpServer, Responder};

#[get("/")]
async fn hello() -> impl Responder {
    "Hello from microservice-rust"
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().service(hello))
        .bind(("0.0.0.0", 8080))?
        .run()
        .await
}
EOF

cat > "$RUST_MS/Dockerfile" <<'EOF'
FROM rust:1.74 as builder
WORKDIR /usr/src/app
COPY . .
RUN cargo build --release
FROM debian:buster-slim
COPY --from=builder /usr/src/app/target/release/microservice-rust /usr/local/bin/
CMD ["microservice-rust"]
EOF

cat > "$RUST_MS/README.md" <<'EOF'
# Microservice Rust Template
Sample Rust microservice template using Actix Web with Dockerfile.
EOF

echo "✅ Full monorepo config setup complete in $BASE_DIR"
echo "You can now run: ./monorepo/orchestration/release-orchestrator.sh"
