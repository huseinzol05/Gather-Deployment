from kafka import KafkaProducer
from kafka.partitioner import RoundRobinPartitioner
from datetime import datetime
import json
from itertools import cycle
import time

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
        # producer_instance.flush()
        return True
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))
        return False


with open('big-text.txt') as fopen:
    texts = list(filter(None, fopen.read().split('\n')))
texts = cycle(texts)

while True:
    word = next(texts)
    data = {'word': word, 'datetime': str(datetime.now())}
    if publish_message(
        producer, 'testing-testing', 'streaming', json.dumps(data)
    ):
        print(data)

    time.sleep(1)
