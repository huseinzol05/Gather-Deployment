from tornado.web import Application, RequestHandler, asynchronous
import numpy as np
import tensorflow as tf
import json


def load_graph(frozen_graph_filename):
    with tf.gfile.GFile(frozen_graph_filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def)
    return graph


with open('dictionary-test.json', 'r') as fopen:
    dic = json.load(fopen)
g = load_graph('frozen_model.pb')
label = ['negative', 'positive']
X = g.get_tensor_by_name('import/Placeholder:0')
Y = g.get_tensor_by_name('import/logits:0')
sess = tf.InteractiveSession(graph = g)
maxlen = 50
UNK = 3


class MainHandler(RequestHandler):
    def get(self):
        self.write('Hello from Tornado')


class TextClassification(RequestHandler):
    def get(self):
        sentence = self.get_argument('sentence', None)
        x = np.zeros((1, maxlen))
        for no, k in enumerate(sentence.split()[:maxlen][::-1]):
            val = dic[k] if k in dic else UNK
            x[0, -1 - no] = val
        index = np.argmax(sess.run(Y, feed_dict = {X: x})[0])
        self.write(json.dumps({'sentiment': label[index]}))


app = Application([(r'/', MainHandler), (r'/classifier', TextClassification)])
