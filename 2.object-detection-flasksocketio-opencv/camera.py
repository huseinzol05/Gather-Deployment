import cv2
import base64
from socketIO_client import SocketIO, BaseNamespace
import numpy as np
import time
from PIL import Image
from threading import Thread, ThreadError
import io

img_np = None
socketIO = SocketIO('localhost', 5000)
live_namespace = socketIO.define(BaseNamespace, '/live')


def receive_events_thread():
    socketIO.wait()


def on_camera_response(*args):
    global img_np
    img_bytes = base64.b64decode(args[0]['data'])
    img_np = np.array(Image.open(io.BytesIO(img_bytes)))


def run_cam():
    global img_np
    while True:
        try:
            cv2.imshow('cam', img_np)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        except:
            continue


live_namespace.on('camera_update', on_camera_response)
receive_events_thread = Thread(target = receive_events_thread)
receive_cam_thread = Thread(target = run_cam)
receive_events_thread.daemon = True
receive_events_thread.start()
receive_cam_thread.daemon = True
receive_cam_thread.start()

cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    img_b = cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))[
        1
    ].tobytes()
    base64_bytes = base64.b64encode(img_b)
    base64_string = base64_bytes.decode('utf-8')
    live_namespace.emit('livevideo', {'data': base64_string})
    time.sleep(0.05)
