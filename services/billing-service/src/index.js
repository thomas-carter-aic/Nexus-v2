const express = require('express');
const mongoose = require('mongoose');
const { Kafka } = require('kafkajs');

const app = express();
app.use(express.json());

const kafka = new Kafka({ clientId: 'billing-service', brokers: [process.env.KAFKA_BOOTSTRAP_SERVERS] });
const producer = kafka.producer();

mongoose.connect(process.env.MONGODB_URL, { useNewUrlParser: true });

const InvoiceSchema = new mongoose.Schema({
tenantId: String,
amount: Number,
status: String,
});
const Invoice = mongoose.model('Invoice', InvoiceSchema);

app.post('/invoices', async (req, res) => {
const { tenantId, amount } = req.body;
const invoice = new Invoice({ tenantId, amount, status: 'pending' });
await invoice.save();
await producer.send({
topic: 'invoices',
messages: [{ value: JSON.stringify({ event: 'InvoiceCreated', invoice }) }],
});
res.json(invoice);
});

app.listen(3003, () => console.log('Billing service running on port 3003'));
