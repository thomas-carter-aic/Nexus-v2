import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  const url = __ENV.TARGET_URL || 'http://localhost:18080/events';
  const payload = JSON.stringify({ type: 'UserCreated', payload: { userId: `u-${Math.floor(Math.random()*1000000)}`, email: 'load@test.com', createdAt: new Date().toISOString() } });
  const params = { headers: { 'Content-Type': 'application/json' } };
  http.post(url, payload, params);
  sleep(1);
}
