import cv2
import imagezmq
from object_detection import detect_object

image_hub = imagezmq.ImageHub(open_port = 'tcp://*:5556')
sender = imagezmq.ImageSender(connect_to = 'tcp://host.docker.internal:5555')

while True:
    name, image = image_hub.recv_image()
    image = detect_object(image)
    sender.send_image(name, image)
    image_hub.send_reply(b'OK')
