const fs = require('fs');
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { BatchSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const grpc = require('@grpc/grpc-js');

function init() {
  try {
    const provider = new NodeTracerProvider();
    const endpoint = process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'otel-collector:4317';
    const certPath = process.env.SSL_CERT_FILE || '/etc/otel/tls/tls.crt';
    let exporterOptions = { url: endpoint };
    if (fs.existsSync(certPath)) {
      const rootCert = fs.readFileSync(certPath);
      exporterOptions.credentials = grpc.credentials.createSsl(rootCert);
    } else {
      exporterOptions.credentials = grpc.credentials.createInsecure();
    }
    const exporter = new OTLPTraceExporter(exporterOptions);
    provider.addSpanProcessor(new BatchSpanProcessor(exporter));
    provider.register();
    console.log('OpenTelemetry OTLP exporter initialized (Node user service)');
  } catch (e) {
    console.warn('otel init failed', e);
  }
}

module.exports = { init };
