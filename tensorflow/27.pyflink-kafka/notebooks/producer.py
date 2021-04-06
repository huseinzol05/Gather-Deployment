from kafka import KafkaProducer
from kafka.partitioner import RoundRobinPartitioner
import time
from datetime import datetime
import json
from itertools import cycle

producer = KafkaProducer(
    bootstrap_servers = ['kafka:9092'],
    api_version = (0, 10),
    partitioner = RoundRobinPartitioner(),
)


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding = 'utf-8')
        value_bytes = bytes(value, encoding = 'utf-8')
        x = producer_instance.send(topic_name, value = value_bytes)
        return True
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))
        return False


with open('/notebooks/big-text.txt') as fopen:
    texts = fopen.read().split('\n')

texts = cycle(texts)

for text in texts:
    data = {'datetime': str(datetime.now()), 'text': text}
    publish_message(producer, 'test', 'streaming', json.dumps(data))
    time.sleep(0.5)
