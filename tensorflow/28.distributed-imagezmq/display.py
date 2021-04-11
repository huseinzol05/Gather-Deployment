import cv2
import imagezmq

image_hub = imagezmq.ImageHub()

while True:
    name, image = image_hub.recv_image()
    cv2.imshow(name, image)
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')
