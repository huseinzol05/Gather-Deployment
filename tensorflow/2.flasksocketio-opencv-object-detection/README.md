## How-To

This repository only support Tensorflow Zoo model, can download [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md),
if you want to use your own model, you need to change some code in `object_detection.py`

1. Download any zoo models [supported](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md).
2. Extract it in the same directory.
3. Change the folder location in `object-detection.py`
```python
MODEL_NAME = 'ssd_mobilenet'
```
4. Run the server,
```bash
python3 app.py
```

5. Run the client, make sure your edit `client/camera.py` put server ip on any snippets related,
```bash
python3 client/camera.py
```

![alt text](screenshot.png)
