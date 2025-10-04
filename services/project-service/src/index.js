const express = require('express');
const mongoose = require('mongoose');
const { Kafka } = require('kafkajs');

const app = express();
app.use(express.json());

const kafka = new Kafka({ clientId: 'project-service', brokers: [process.env.KAFKA_BOOTSTRAP_SERVERS] });
const producer = kafka.producer();

mongoose.connect(process.env.MONGODB_URL, { useNewUrlParser: true });

const ProjectSchema = new mongoose.Schema({
tenantId: String,
name: String,
tasks: [{ name: String, status: String }],
});
const Project = mongoose.model('Project', ProjectSchema);

app.post('/projects', async (req, res) => {
const { tenantId, name } = req.body;
const project = new Project({ tenantId, name, tasks: [] });
await project.save();
await producer.send({
topic: 'projects',
messages: [{ value: JSON.stringify({ event: 'ProjectCreated', project }) }],
});
res.json(project);
});

app.listen(3004, () => console.log('Project service running on port 3004'));
