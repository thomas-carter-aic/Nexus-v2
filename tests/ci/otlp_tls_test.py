import os, time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def main():
    endpoint = os.environ.get("OTEL_ENDPOINT", "localhost:4317")
    exporter = OTLPSpanExporter(endpoint=endpoint)
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("ci-test-span"):
        print("created span")
    time.sleep(2)
    print("done")

if __name__ == '__main__':
    main()
