#!/usr/bin/env python3

import tensorflow as tf
import numpy as np
import json
import sys


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

for line in sys.stdin:
    sentences = list(filter(None, line.split('\n')))
    x = np.zeros((len(sentences), maxlen))
    for i, sentence in enumerate(sentences):
        for no, k in enumerate(sentence.split()[:maxlen][::-1]):
            val = dic[k] if k in dic else UNK
            x[i, -1 - no] = val
    indices = np.argmax(sess.run(Y, feed_dict = {X: x}), axis = 1)
    for no, index in enumerate(indices):
        print('%s: %s' %(sentences[no], label[index]))
