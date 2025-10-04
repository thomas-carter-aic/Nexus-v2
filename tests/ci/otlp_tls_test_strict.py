import os, time
import grpc
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def main():
    endpoint = os.environ.get("OTEL_ENDPOINT", "localhost:4317")
    ca_path = "ci-certs/ca.crt"
    if not os.path.exists(ca_path):
        print("CA cert not found:", ca_path)
        raise SystemExit(1)
    with open(ca_path, "rb") as f:
        ca = f.read()
    creds = grpc.ssl_channel_credentials(root_certificates=ca)
    exporter = OTLPSpanExporter(endpoint=endpoint, credentials=creds)
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("ci-strict-span"):
        print("created strict span")
    time.sleep(2)
    print("done (strict)")

if __name__ == '__main__':
    main()
