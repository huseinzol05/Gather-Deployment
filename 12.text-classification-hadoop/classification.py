import tensorflow as tf
import numpy as np
import json


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

with open('dictionary-test.json', 'r') as fopen:
    dic = json.load(fopen)


def to_tensor(string, maxlen = 50, UNK = 3):
    x = np.zeros((1, maxlen))
    for no, k in enumerate(string.split()[:maxlen][::-1]):
        val = dic[k] if k in dic else UNK
        x[0, -1 - no] = val
    return x


def result(string):
    x = to_tensor(string)
    return label[np.argmax(test_sess.run(Y, feed_dict = {X: x})[0])]


def mapper(_, record, writer):
    writer.emit('', result(record))
