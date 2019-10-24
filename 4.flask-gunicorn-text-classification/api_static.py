import os
import pickle
import tensorflow as tf
import time
import model
import numpy as np
from flask import Flask, render_template, request
from werkzeug import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = ''

with open('vector-sentiment.p', 'rb') as fopen:
    vectors = pickle.load(fopen)
with open('dictionary-sentiment.p', 'rb') as fopen:
    dictionary = pickle.load(fopen)
    
def load_graph(frozen_graph_filename):
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def)
    return graph

g=load_graph('frozen_model.pb')
x = g.get_tensor_by_name('import/Placeholder:0')
y = g.get_tensor_by_name('import/logits:0')
sess = tf.InteractiveSession(graph=g)
maxlen = 50
dimension = vectors.shape[1]

@app.route('/static', methods = ['GET'])
def get_text():
    last_time = time.time()
    batch_x = np.zeros((1, maxlen, dimension))
    tokens = request.args.get('text').split()[:maxlen]
    for no, text in enumerate(tokens[::-1]):
        try:
            batch_x[0, -1 - no, :] += vectors[dictionary[text], :]
        except Exception as e:
            pass
    sess.run(tf.nn.softmax(y), feed_dict = {x : batch_x})
    return str(time.time()-last_time)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', threaded = True,  port = 8033)