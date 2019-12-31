from flask import Flask, request
from werkzeug import secure_filename
import tensorflow.contrib.slim as slim
import tensorflow as tf
import inception_v1
import json
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)
with open('real-label.json', 'r') as fopen:
    labels = json.load(fopen)
sess = tf.InteractiveSession()
X = tf.placeholder(tf.float32, [None, None, 3])
image = X / 128.0 - 1
image = tf.expand_dims(image, 0)
image = tf.image.resize_images(image, (224, 224))
with slim.arg_scope(inception_v1.inception_v1_arg_scope()):
    logits, endpoints = inception_v1.inception_v1(
        image, num_classes = 1001, is_training = False
    )
sess.run(tf.global_variables_initializer())
var_lists = tf.get_collection(
    tf.GraphKeys.GLOBAL_VARIABLES, scope = 'InceptionV1'
)
saver = tf.train.Saver(var_list = var_lists)
saver.restore(sess, 'inception_v1.ckpt')


@app.route('/inception', methods = ['POST'])
def inception():
    img = np.array(Image.open(io.BytesIO(request.files['file'].read())))
    return json.dumps(
        {
            'label': labels[
                str(np.argmax(sess.run(logits, feed_dict = {X: img})[0]))
            ]
        }
    )


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)
