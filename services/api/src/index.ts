import express from 'express';
import { greet } from '@libs/utils';
const app = express();
app.get('/', (req, res) => res.send(greet()));
app.listen(3001, () => console.log('API running at http://localhost:3001'));
