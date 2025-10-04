const express = require('express');
const { Kafka } = require('kafkajs');

const app = express();
const kafka = new Kafka({ clientId: 'realtime-service', brokers: [process.env.KAFKA_BOOTSTRAP_SERVERS] });
const producer = kafka.producer();

app.get('/health', (req, res) => {
res.json({ status: 'healthy' });
});

app.listen(3000, () => console.log('Realtime service running on port 3000'));
