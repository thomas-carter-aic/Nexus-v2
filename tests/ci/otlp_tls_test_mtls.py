import os, time, grpc, ssl
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def main():
    endpoint = os.environ.get("OTEL_ENDPOINT", "localhost:4317")
    ca = open("ci-certs/ca.crt","rb").read()
    client_cert = open("ci-certs/client.crt","rb").read()
    client_key = open("ci-certs/client.key","rb").read()
    # create grpc credentials with client cert/key and root CA
    creds = grpc.ssl_channel_credentials(root_certificates=ca, private_key=client_key, certificate_chain=client_cert)
    exporter = OTLPSpanExporter(endpoint=endpoint, credentials=creds)
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("ci-mtls-span"):
        print("created mTLS span")
    time.sleep(2)
    print("done (mTLS)")

if __name__ == '__main__':
    main()
