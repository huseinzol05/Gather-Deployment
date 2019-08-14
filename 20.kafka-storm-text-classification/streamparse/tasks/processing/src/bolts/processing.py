from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
from elasticsearch import helpers
import json
import re
import uuid
from streamparse import Bolt
import tensorflow as tf
import numpy as np

def return_es():
    return Elasticsearch(
        hosts = [{'host': 'elasticsearch', 'port': 9200}],
        connection_class = RequestsHttpConnection,
    )

def load_graph(frozen_graph_filename):
    with tf.gfile.GFile(frozen_graph_filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def)
    return graph

class ProcessingBolt(Bolt):
    outputs = ['processed_text']

    def initialize(self, conf, ctx):
        self.es = return_es()
        with open('/home/storm/dictionary-test.json', 'r') as fopen:
            self.dic = json.load(fopen)
        g = load_graph('/home/storm/frozen_model.pb')
        self.label = ['negative', 'positive']
        self.X = g.get_tensor_by_name('import/Placeholder:0')
        self.Y = g.get_tensor_by_name('import/logits:0')
        self.sess = tf.InteractiveSession(graph = g)
        self.maxlen = 50
        self.UNK = 3

    def process(self, tup):
        sentences = []
        for t in tup.values[0]:
            try:
                if 'Broker: No more' in t:
                    continue
                sentences.append(json.loads(t))
            except:
                pass
        
        x = np.zeros((len(sentences), self.maxlen))
        for i, sentence in enumerate(sentences):
            text = sentence['text']
            # please do preprocessing first
            for no, k in enumerate(text.split()[:self.maxlen][::-1]):
                val = self.dic[k] if k in self.dic else self.UNK
                x[i, -1 - no] = val
        indices = np.argmax(self.sess.run(self.Y, feed_dict = {self.X: x}), axis = 1)
        for i in range(len(sentences)):
            sentences[i]['label'] = self.label[indices[i]]
        
        actions = [
            {
                '_index': 'twitter_test_v1',
                '_type': 'sentence',
                '_id': str(uuid.uuid1()),
                '_source': sentences[k],
            }
            for k in range(len(sentences))
        ]
        helpers.bulk(self.es, actions)
        
        self.emit([sentences])

