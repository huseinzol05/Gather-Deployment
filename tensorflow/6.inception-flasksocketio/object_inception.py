import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
import os
import cv2
import inception_v3
import json

with open('real-label.json', 'r') as fopen:
    labels = json.load(fopen)
    
tf.reset_default_graph()
sess = tf.InteractiveSession()
X = tf.placeholder(tf.float32,[None,None,3])
image = X / 128.  - 1
image = tf.expand_dims(image, 0)
image = tf.image.resize_images(image, (299, 299))
with slim.arg_scope(inception_v3.inception_v3_arg_scope()):
    logits, endpoints = inception_v3.inception_v3(image,num_classes=1001,is_training=False)
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()
saver.restore(sess, 'inception_v3.ckpt')

def detect_object(img):
    index = np.argmax(sess.run(logits,feed_dict={X:img})[0])
    return labels[str(index)], index