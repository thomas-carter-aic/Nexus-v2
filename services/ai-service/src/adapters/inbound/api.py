from prometheus_client import start_http_server, Counter, generate_latest, CONTENT_TYPE_LATEST
REQUEST_COUNT = Counter('ai_requests_total', 'Total AI requests')
# start a metrics server on port 8000
try:
    start_http_server(8000)
except Exception as e:
    print('failed to start prometheus server', e)

from fastapi import FastAPI
app = FastAPI()
@app.get('/health')
def health():
    return {'status':'ok'}
