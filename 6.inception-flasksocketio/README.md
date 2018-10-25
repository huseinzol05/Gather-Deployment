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
```
python3 app.py
```

5. Use any socket-io clients (JS, Python) to get realtime label from the server.
