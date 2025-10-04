const express = require('express');
const mongoose = require('mongoose');
const { Kafka } = require('kafkajs');

const app = express();
app.use(express.json());

const kafka = new Kafka({ clientId: 'ai-service', brokers: [process.env.KAFKA_BOOTSTRAP_SERVERS] });
const producer = kafka.producer();

mongoose.connect(process.env.MONGODB_URL, { useNewUrlParser: true });

const ModelSchema = new mongoose.Schema({
tenantId: String,
name: String,
status: String,
});
const Model = mongoose.model('Model', ModelSchema);

app.post('/models', async (req, res) => {
const { tenantId, name } = req.body;
const model = new Model({ tenantId, name, status: 'training' });
await model.save();
await producer.send({
topic: 'models',
messages: [{ value: JSON.stringify({ event: 'ModelCreated', model }) }],
});
res.json(model);
});

app.listen(3006, () => console.log('AI service running on port 3006'));
