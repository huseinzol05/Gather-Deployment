import cv2
import base64
from socketIO_client import SocketIO, BaseNamespace
import numpy as np
import time
from PIL import Image
from threading import Thread, ThreadError
import io

socketIO = SocketIO('localhost', 5000)
live_namespace = socketIO.define(BaseNamespace, '/live')


def receive_events_thread():
    socketIO.wait()

def on_camera_response(*args):
    print(args[0])



live_namespace.on('camera_update', on_camera_response)
receive_events_thread = Thread(target = receive_events_thread)
receive_events_thread.daemon = True
receive_events_thread.start()

cap = cv2.VideoCapture(0)
count = 0
while True:
    ret, img = cap.read()
    img_b = cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))[
        1
    ].tobytes()
    if count % 20 == 0:
        base64_bytes = base64.b64encode(img_b)
        base64_string = base64_bytes.decode('utf-8')
        live_namespace.emit('livevideo', {'data': base64_string})
        count = 1
    count += 1
