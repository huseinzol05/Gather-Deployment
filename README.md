# Gather-Tensorflow-Serving
Gather how to deploy tensorflow models as much I can

## Covered

1. Object Detection using Flask SocketIO for WebRTC
2. Object Detection using Flask SocketIO for opencv
3. Speech streaming using Flask SocketIO
4. Classification using Flask + Gunicorn
5. Classification using TF Serving
6. Inception Classification using Flask SocketIO
7. Object Detection using Flask + opencv
8. Face-detection using Flask SocketIO for opencv
9. Face-detection for opencv
10. Inception with Flask using Docker
11. Multiple Inception with Flask using EC2 Docker Swarm + Nginx load balancer

## Why Flask

Flask implements a bare-minimum CGI with powerful routing application.

![alt text](http://flask.pocoo.org/docs/1.0/_static/flask.png)

## Why Flask SocketIO

<p align="left">
    <img src="pictures/diagram.png" width="40%" />
</p>

## Why load balancer

<p align="left">
    <img src="https://f5.com/Portals/1/Images/whitepaper-images/load-balancing-101-nuts-bolts/NutsBolts-fig1.png" width="50%" />
</p>

## Printscreen

![alt text](1.object-detection-flasksocketio-webrtc/screenshot.png)

All folders contain printscreen.

## Notes

1. Deploy them on a server, change `local` in code snippets to your own IP.
2. WebRTC chrome only can tested on HTTPS server.
3. When come to real deployment, always prepare for up-scaling architectures. Learn about DevOps.
4. Please aware with your cloud cost!
