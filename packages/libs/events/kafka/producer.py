from confluent_kafka import Producer

class KafkaProducer:
def __init__(self, bootstrap_servers='kafka:9092'):
    self.producer = Producer({'bootstrap.servers': bootstrap_servers})

def publish(self, topic, event):
    self.producer.produce(topic, event.encode('utf-8'))
    self.producer.flush()

def __del__(self):
    self.producer.flush()
