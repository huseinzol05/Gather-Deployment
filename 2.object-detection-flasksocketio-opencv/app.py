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
from object_detection import detect_object

d = dirname(dirname(abspath(__file__)))

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
    img_np = detect_object(img_np)
    frame = cv2.imencode('.jpg', cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB))[
        1
    ].tobytes()
    base64_bytes = base64.b64encode(frame)
    base64_string = base64_bytes.decode('utf-8')
    emit('camera_update', {'data': base64_string}, broadcast = True)


if __name__ == '__main__':
    socketio.run(app, host = 'localhost', port = 5000, debug = True)
