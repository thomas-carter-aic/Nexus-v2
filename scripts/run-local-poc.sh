#!/usr/bin/env bash
# run-local-poc.sh - starts workspace-service (node), orchestration (go), infra (go), and user (spring boot) locally for POC
# Requires: node, go, mvn installed locally

set -euo pipefail
echo "Starting workspace-service (node)"
pushd services/workspace-service >/dev/null
npm ci || true
nohup node index.js > ../../workspace-service.log 2>&1 &
popd >/dev/null
echo "Starting orchestration-service (go)"
pushd services/orchestration-service/cmd/orchestration >/dev/null
nohup go run . > ../../orchestration.log 2>&1 &
popd >/dev/null
echo "Starting infra-service (go)"
pushd services/infra-service/cmd/infra >/dev/null
nohup go run . > ../../infra.log 2>&1 &
popd >/dev/null
echo "Starting user-service (spring boot)"
pushd services/user-service >/dev/null
# build with mvn package then run - requires maven
nohup mvn -q -DskipTests package spring-boot:run > ../../user-service.log 2>&1 &
popd >/dev/null
echo "All POC services started. Check *_service.log files at repo root."
