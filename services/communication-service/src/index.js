const express = require('express');
const { Server } = require('socket.io');
const nodemailer = require('nodemailer');
const { Kafka } = require('kafkajs');

const app = express();
const server = require('http').createServer(app);
const io = new Server(server);

const kafka = new Kafka({ clientId: 'communication-service', brokers: [process.env.KAFKA_BOOTSTRAP_SERVERS] });
const producer = kafka.producer();

app.use(express.json());

io.on('connection', (socket) => {
socket.on('message', async (msg) => {
await producer.send({
topic: 'messages',
messages: [{ value: JSON.stringify({ tenantId: msg.tenantId, message: msg.text }) }],
});
io.emit('message', msg);
});
});

app.post('/email', async (req, res) => {
const { to, subject, text, tenantId } = req.body;
const transporter = nodemailer.createTransport({
service: 'SendGrid',
auth: { user: 'apikey', pass: process.env.SENDGRID_API_KEY },
});
await transporter.sendMail({ to, subject, text });
await producer.send({
topic: 'emails',
messages: [{ value: JSON.stringify({ tenantId, to, subject }) }],
});
res.json({ status: 'sent' });
});

server.listen(3005, () => console.log('Communication service running on port 3005'));
