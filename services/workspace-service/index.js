const express = require('express');
const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.json());

app.post('/provision', async (req, res) => {
const { Kafka } = require('kafkajs');
async function publishEvent(event) {
  const kafkaBootstrap = process.env.KAFKA_BOOTSTRAP;
  if (!kafkaBootstrap) {
    console.log('Event:', JSON.stringify(event));
    return;
  }
  const kafka = new Kafka({ brokers: [kafkaBootstrap] });
  const producer = kafka.producer();
  await producer.connect();
  await producer.send({ topic: 'platform-events', messages: [{ value: JSON.stringify(event) }] });
  await producer.disconnect();
}

  const payload = req.body || {};
  console.log('Provision request received', payload);
  // Simulate provisioning delay
  setTimeout(() => {
    // Emit a WorkspaceProvisioned event to stdout (placeholder for Kafka)
    const evt = { type: 'WorkspaceProvisioned', payload: { workspaceId: payload.workspaceId || ('ws-' + Date.now()), ownerId: payload.ownerId || 'unknown', createdAt: new Date().toISOString() } };
    console.log(JSON.stringify(evt));
  }, 500);
  res.status(201).json({ status: 'provisioning', workspaceId: payload.workspaceId || ('ws-' + Date.now()) });
});

app.get('/health', (req, res) => res.json({ status: 'ok' }));

const port = process.env.PORT || 9000;
// OpenTelemetry (basic stdout tracer) and Prometheus metrics
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { ConsoleSpanExporter } = require('@opentelemetry/sdk-trace-base');
try {
  const provider = new NodeTracerProvider();
  provider.addSpanProcessor(new SimpleSpanProcessor(new ConsoleSpanExporter()));
  provider.register();
  console.log('OpenTelemetry tracing initialized (console exporter)');
} catch (e) {
  console.warn('otel init failed', e);
}
const promClient = require('prom-client');
const collectDefaultMetrics = promClient.collectDefaultMetrics;
collectDefaultMetrics();
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.end(await promClient.register.metrics());
});

app.listen(port, () => console.log(`workspace-service listening on ${port}`));
