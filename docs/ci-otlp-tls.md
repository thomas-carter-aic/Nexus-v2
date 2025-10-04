# CI OTLP TLS Strict Test

The GitHub Actions workflow `.github/workflows/otlp-tls-integration.yml` was updated to run a strict TLS test:

- It generates a CA and server certs via openssl in the runner workspace.
- It creates an OTEL collector config with TLS receiver and mounts the certs into the collector container.
- It runs `tests/ci/otlp_tls_test_strict.py`, which uses the CA cert to establish a secure gRPC channel to the collector and export a span.

If the test passes, the collector accepted the TLS connection and the exporter succeeded.
