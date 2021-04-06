from flask import Flask, request
from kafka import KafkaConsumer
import json
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!'


@app.route('/topic/<string:topic>/')
def get_topics(topic):
    consumer = KafkaConsumer(
        topic,
        auto_offset_reset = 'earliest',
        bootstrap_servers = ['localhost:9092'],
        api_version = (0, 10),
        consumer_timeout_ms = 1000,
    )
    return json.dumps(
        [json.loads(msg.value.decode('utf-8')) for msg in consumer]
    )


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
