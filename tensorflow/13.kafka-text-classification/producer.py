import numpy as np
import tensorflow as tf
import json
from kafka import KafkaProducer


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding = 'utf-8')
        value_bytes = bytes(value, encoding = 'utf-8')
        producer_instance.send(topic_name, key = key_bytes, value = value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    print('connecting to kafka')
    _producer = None
    try:
        _producer = KafkaProducer(
            bootstrap_servers = ['localhost:9092'], api_version = (0, 10)
        )
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        print('successfully connected to kafka')
        return _producer


def load_graph(frozen_graph_filename):
    with tf.gfile.GFile(frozen_graph_filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def)
    return graph


g = load_graph('frozen_model.pb')

label = ['negative', 'positive']

X = g.get_tensor_by_name('import/Placeholder:0')
Y = g.get_tensor_by_name('import/logits:0')
sess = tf.InteractiveSession(graph = g)
maxlen = 50
UNK = 3

with open('dictionary-test.json', 'r') as fopen:
    dic = json.load(fopen)

with open('text.txt') as fopen:
    sentences = fopen.read().split('\n')

kafka_producer = connect_kafka_producer()

for sentence in sentences:
    x = np.zeros((1, maxlen))
    for no, k in enumerate(sentence.split()[:maxlen][::-1]):
        val = dic[k] if k in dic else UNK
        x[0, -1 - no] = val
    index = np.argmax(sess.run(Y, feed_dict = {X: x})[0])
    print('feeding ' + sentence)
    publish_message(kafka_producer, 'polarities', 'polarity', label[index])
if kafka_producer is not None:
    kafka_producer.close()
