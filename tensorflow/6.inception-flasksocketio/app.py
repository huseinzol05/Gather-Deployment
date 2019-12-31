from flask import Flask, Response
from flask_socketio import SocketIO, send, emit
from os.path import dirname, abspath
from queue import Queue
import base64
import cv2
import numpy as np
from PIL import Image
import io
import time
from object_inception import detect_object
from scipy.misc import imsave

app = Flask(__name__)
app.queue = Queue()
socketio = SocketIO(app)


@socketio.on('connect', namespace = '/live')
def test_connect():
    print('Client wants to connect.')
    emit('response', {'data': 'OK'}, broadcast = True)


@socketio.on('disconnect', namespace = '/live')
def test_disconnect():
    print('Client disconnected')


@socketio.on('event', namespace = '/live')
def test_message(message):
    emit('response', {'data': message['data']})
    print(message['data'])


@socketio.on('livevideo', namespace = '/live')
def test_live(message):
    app.queue.put(message['data'])
    img_bytes = base64.b64decode(app.queue.get())
    img_np = np.array(Image.open(io.BytesIO(img_bytes)))
    label, index = detect_object(img_np)
    emit(
        'camera_update',
        {'label': label},
        broadcast = True,
    )


if __name__ == '__main__':
    socketio.run(app, host = 'localhost', port = 5000, debug = True)
