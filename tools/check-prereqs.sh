#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Checking prerequisites for monorepo bootstrap..."

# List of required CLIs
REQUIRED_TOOLS=(bash kubectl kind helm yq jq git curl docker)

MISSING=()

for tool in "${REQUIRED_TOOLS[@]}"; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "❌ $tool not found"
    MISSING+=("$tool")
  else
    VERSION=$($tool version --short 2>/dev/null || $tool --version 2>/dev/null || echo "unknown")
    echo "✅ $tool found ($VERSION)"
  fi
done

# Flux CLI (optional, but warn if missing)
if ! command -v flux >/dev/null 2>&1; then
  echo "⚠️ flux CLI not found (will be installed by bootstrap if needed)"
else
  echo "✅ flux CLI found ($($(command -v flux) --version 2>/dev/null || echo "unknown"))"
fi

# Docker check
if docker info >/dev/null 2>&1; then
  echo "🐳 Docker is running"
else
  echo "❌ Docker not running (Kind requires Docker)"
  MISSING+=("docker-runtime")
fi

# Kubernetes config sanity
if kubectl version --client >/dev/null 2>&1; then
  echo "✅ kubectl client is working"
else
  echo "❌ kubectl not working correctly"
  MISSING+=("kubectl-config")
fi

# Helm repo sanity check
if helm repo list >/dev/null 2>&1; then
  echo "✅ helm is configured"
else
  echo "⚠️ helm repos not set up (will be added by bootstrap)"
fi

# Languages (optional polyglot support)
LANGUAGES=(node java go python rust)

for lang in "${LANGUAGES[@]}"; do
  case "$lang" in
    node)
      if command -v node >/dev/null 2>&1; then
        echo "✅ Node.js found ($(node --version))"
      else
        echo "⚠️ Node.js not installed (needed for TypeScript/JS apps)"
      fi
      ;;
    java)
      if command -v java >/dev/null 2>&1; then
        echo "✅ Java found ($(java -version 2>&1 | head -n1))"
      else
        echo "⚠️ Java not installed"
      fi
      ;;
    go)
      if command -v go >/dev/null 2>&1; then
        echo "✅ Go found ($(go version))"
      else
        echo "⚠️ Go not installed"
      fi
      ;;
    python)
      if command -v python3 >/dev/null 2>&1; then
        echo "✅ Python found ($(python3 --version))"
      else
        echo "⚠️ Python not installed"
      fi
      ;;
    rust)
      if command -v rustc >/dev/null 2>&1; then
        echo "✅ Rust found ($(rustc --version))"
      else
        echo "⚠️ Rust not installed"
      fi
      ;;
  esac
done

echo
if [ ${#MISSING[@]} -eq 0 ]; then
  echo "🎉 All core prerequisites satisfied! You can run ./ultimate-bootstrap-full.sh safely."
else
  echo "⚠️ Missing critical tools: ${MISSING[*]}"
  echo "   Please install them before continuing."
  exit 1
fi
