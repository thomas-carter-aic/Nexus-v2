#!/usr/bin/env bash
# scaffold-service.sh
# Usage: scaffold-service.sh <service-name> --lang <java|typescript|python|go|rust>
set -euo pipefail

SERVICE_NAME="$1"
shift || true
LANG="typescript"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --lang) LANG="$2"; shift 2;;
    *) shift;;
  esac
done

ROOT="$(cd "$(dirname "$0")/.."; pwd)"
TEMPLATE_DIR="$ROOT/shared/templates/$LANG"
TARGET_DIR="$ROOT/services/$SERVICE_NAME"

if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "Template for $LANG not found at $TEMPLATE_DIR"
  exit 1
fi

if [ -d "$TARGET_DIR" ]; then
  echo "Target $TARGET_DIR already exists"
  exit 1
fi

echo "Scaffolding $SERVICE_NAME using $LANG template..."
mkdir -p "$TARGET_DIR"
cp -R "$TEMPLATE_DIR/." "$TARGET_DIR/"
# Replace placeholders in service.yaml and README.md
sed -i "s/{{SERVICE_NAME}}/$SERVICE_NAME/g" "$TARGET_DIR/service.yaml" || true
sed -i "s/{{SERVICE_NAME}}/$SERVICE_NAME/g" "$TARGET_DIR/README.md" || true

echo "Done. Created $TARGET_DIR"
