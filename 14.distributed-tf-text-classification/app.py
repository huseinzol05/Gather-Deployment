import tensorflow as tf
import json
import numpy as np
import os

with open('dictionary-test.json', 'r') as fopen:
    dic = json.load(fopen)

cluster = tf.train.ClusterSpec(
    {'worker': ['192.168.0.101:2222', '192.168.0.104:2223']}
)


class Model:
    def __init__(
        self,
        size_layer,
        num_layers,
        embedded_size,
        dict_size,
        dimension_output,
        learning_rate,
    ):
        def cells(reuse = False):
            return tf.nn.rnn_cell.BasicRNNCell(size_layer, reuse = reuse)

        self.X = tf.placeholder(tf.int32, [None, None])
        self.Y = tf.placeholder(tf.float32, [None, dimension_output])
        encoder_embeddings = tf.Variable(
            tf.random_uniform([dict_size, embedded_size], -1, 1)
        )
        with tf.device('/job:worker/task:0'):
            encoder_embedded = tf.nn.embedding_lookup(
                encoder_embeddings, self.X
            )
            rnn_cells = tf.nn.rnn_cell.MultiRNNCell(
                [cells() for _ in range(num_layers)]
            )

            outputs, _ = tf.nn.dynamic_rnn(
                rnn_cells, encoder_embedded, dtype = tf.float32
            )
        with tf.device('/job:worker/task:1'):
            rnn_W = tf.Variable(
                tf.random_normal((size_layer, dimension_output))
            )
            rnn_B = tf.Variable(tf.random_normal([dimension_output]))
            self.logits = tf.add(
                tf.matmul(outputs[:, -1], rnn_W), rnn_B, name = 'logits'
            )


sess = tf.InteractiveSession('grpc://192.168.0.101:2222')
# based in freeze-model.ipynb
model = Model(
    size_layer = 64,
    num_layers = 1,
    embedded_size = 64,
    dict_size = 3366,
    dimension_output = 2,
    learning_rate = 1e-3,
)
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver(tf.global_variables())
saver.restore(sess, os.getcwd() + '/checkpoint/test')
label = ['negative', 'positive']
UNK = 3
maxlen = 50

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def hello():
    text = request.args.get('text')
    x = np.zeros((1, maxlen))
    for no, k in enumerate(text.split()[:maxlen][::-1]):
        val = dic[k] if k in dic else UNK
        x[0, -1 - no] = val
    index = np.argmax(sess.run(model.logits, feed_dict = {model.X: x})[0])
    return label[index]


application = app
