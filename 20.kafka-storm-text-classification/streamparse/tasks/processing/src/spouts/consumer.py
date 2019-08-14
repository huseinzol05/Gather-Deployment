from confluent_kafka import Consumer, KafkaError
from streamparse import Spout
import json


class ConsumerSpout(Spout):
    outputs = ['sentences']

    def initialize(self, stormconf, context):
        self.consumer = Consumer(
            {
                'bootstrap.servers': 'kafka:9092',
                'group.id': 'mygroup',
                'auto.offset.reset': 'latest',
            }
        )
        self.consumer.subscribe(['twitter'])

    def next_tuple(self):
        msg = self.consumer.consume(num_messages = 100, timeout = 10)
        self.emit([[m.value().decode('utf-8') for m in msg]])
