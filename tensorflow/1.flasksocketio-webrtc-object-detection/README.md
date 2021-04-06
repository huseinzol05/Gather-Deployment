## How-To

This repository only support Tensorflow Zoo model, https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md.

if you want to use your own model, you need to change some code in [object_detection.py](object_detection.py).

1. Run docker-compose,

```bash
docker-compose -f docker-compose.yaml up --build
```

5. Go to [localhost](http://localhost:5000). You can edit the port and exposure in [app.py](app.py),

```python
socketio.run(app, host = 'localhost', port = 5000,debug=True)
```

![alt text](screenshot.png)
