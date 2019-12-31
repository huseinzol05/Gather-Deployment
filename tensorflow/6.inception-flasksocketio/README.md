## How-To

This repository only support Tensorflow Zoo model, can download [here](https://github.com/tensorflow/models/tree/master/research/slim),
if you want to use your own model, you need to change some code in `object_inception.py`

1. Download any zoo models [supported](https://github.com/tensorflow/models/tree/master/research/slim). I use Inception V3 for this one.
2. Extract it in the same directory.
3. Change the folder location in `object-detection.py`
```python
saver.restore(sess, 'inception_v3.ckpt')
```
4. Run the server,
```bash
python3 app.py
```
```text
127.0.0.1 - - [26/Oct/2018 12:51:53] "POST /socket.io/?t=1540529513722-37&EIO=3&transport=polling&sid=0d025fbf678f4a20be71768034ee5c07 HTTP/1.1" 200 -
127.0.0.1 - - [26/Oct/2018 12:51:53] "GET /socket.io/?t=1540529513207-36&EIO=3&transport=polling&sid=0d025fbf678f4a20be71768034ee5c07 HTTP/1.1" 200 -
127.0.0.1 - - [26/Oct/2018 12:51:54] "POST /socket.io/?t=1540529513748-39&EIO=3&transport=polling&sid=0d025fbf678f4a20be71768034ee5c07 HTTP/1.1" 200 -
127.0.0.1 - - [26/Oct/2018 12:51:54] "GET /socket.io/?t=1540529513742-38&EIO=3&transport=polling&sid=0d025fbf678f4a20be71768034ee5c07 HTTP/1.1" 200 -
Client disconnected
```

5. Use any socket-io clients (JS, Python) to get realtime label from the server. Or run `camera.py`,
```bash
python3 camera.py
```
```text
{'label': 'suit, suit of clothes'}
{'label': 'vase'}
{'label': 'coffee mug'}
{'label': 'coffee mug'}
{'label': 'coffee mug'}
{'label': 'coffee mug'}
{'label': 'coffee mug'}
{'label': 'coffee mug'}
{'label': 'coffee mug'}
```
