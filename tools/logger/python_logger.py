import logging
import json
from logging.handlers import HTTPHandler

class LokiLogger(logging.Handler):
def init(self, loki_url):
super().init()
self.loki_url = loki_url

def emit(self, record):
log_entry = {
"level": record.levelname,
"message": record.getMessage(),
"timestamp": record.created
}
requests.post(self.loki_url + "/loki/api/v1/push", json={"streams": [{"stream": {"app": record.name}, "values": [[str(record.created * 1000), json.dumps(log_entry)]]}]})

logging.getLogger('').addHandler(LokiLogger('http://loki:3100'))
logging.getLogger('').setLevel(logging.INFO)
