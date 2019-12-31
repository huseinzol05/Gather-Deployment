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

maxlen = 50
location = os.getcwd()
num_layers = 3
size_layer = 256
learning_rate = 0.0001
output_size = 2

with open('vector-sentiment.p', 'rb') as fopen:
    vectors = pickle.load(fopen)
with open('dictionary-sentiment.p', 'rb') as fopen:
    dictionary = pickle.load(fopen)

sess = tf.InteractiveSession()
model = model.Model(num_layers, size_layer, vectors.shape[1], output_size, learning_rate)
sess.run(tf.global_variables_initializer())
dimension = vectors.shape[1]
saver = tf.train.Saver(tf.global_variables())
saver.restore(sess, os.getcwd() + "/model-rnn-vector-huber.ckpt")

@app.route('/dynamic', methods = ['GET'])
def get_text():
    last_time = time.time()
    batch_x = np.zeros((1, maxlen, dimension))
    tokens = request.args.get('text').split()[:maxlen]
    for no, text in enumerate(tokens[::-1]):
        try:
            batch_x[0, -1 - no, :] += vectors[dictionary[text], :]
        except Exception as e:
            pass
    sess.run(tf.nn.softmax(model.logits), feed_dict = {model.X : batch_x})
    return str(time.time()-last_time)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', threaded = True,  port = 8033)