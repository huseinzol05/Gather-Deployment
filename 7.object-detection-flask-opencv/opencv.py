import numpy as np
import cv2
import settings
import os
import tensorflow as tf
import json
from threading import Thread
import threading
import time

sess = tf.InteractiveSession()
# load any model
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver(tf.global_variables())

saver.restore(sess)


class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, frame = self.video.read()
        frame_copy = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
        # do something with frame_copy
        return cv2.imencode('.jpg', frame_copy)[1].tobytes()
