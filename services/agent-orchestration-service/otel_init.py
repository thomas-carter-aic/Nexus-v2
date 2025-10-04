from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import os, grpc

def init_tracing():
    endpoint = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'otel-collector:4317')
    cert_file = os.getenv('SSL_CERT_FILE', '/etc/otel/tls/tls.crt')
    if cert_file and os.path.exists(cert_file):
        with open(cert_file, 'rb') as f:
            ca = f.read()
        creds = grpc.ssl_channel_credentials(root_certificates=ca)
        exporter = OTLPSpanExporter(endpoint=endpoint, credentials=creds)
    else:
        exporter = OTLPSpanExporter(endpoint=endpoint)
    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "agent-orchestration-service"}))
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    print('OTel tracing initialized (agent-orchestration-service)')
