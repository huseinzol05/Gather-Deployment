import socket
import time
import imagezmq
from utils.webcam import WebcamVideoStream

sender = imagezmq.ImageSender(connect_to = 'tcp://localhost:5556')
cam = WebcamVideoStream().start()
name = 'client2'
print(name)
time.sleep(2.0)
while True:
    image = cam.read()
    sender.send_image(name, image)
    time.sleep(0.3333)
