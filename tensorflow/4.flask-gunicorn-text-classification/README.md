# Tensorflow-Serving-Comparison

Compare time API request on Dynamic and Static Deep LSTM Recurrent Neural Network classifying POSITIVE or NEGATIVE for a text

## About

dynamic graph
```python
sess = tf.InteractiveSession()
model = model.Model(num_layers, size_layer, vectors.shape[1], output_size, learning_rate)
sess.run(tf.global_variables_initializer())
dimension = vectors.shape[1]
saver = tf.train.Saver(tf.global_variables())
saver.restore(sess, os.getcwd() + "/model-rnn-vector-huber.ckpt")
```

static graph
```python
g=load_graph('frozen_model.pb')
x = g.get_tensor_by_name('import/Placeholder:0')
y = g.get_tensor_by_name('import/logits:0')
sess = tf.InteractiveSession(graph=g)
```

Differences between those types:
1. dynamic graph required model's code, static no need
2. dynamic graph really easy to spawn, static need to specific which placeholder, variables need to freeze

API for dynamic graph, api_dynamic.py
```python
@app.route('/dynamic', methods = ['GET'])
```

API for static graph, api_static.py
```python
@app.route('/static', methods = ['GET'])
```


## How-to

#### How to freeze a model, read sentiment-huber-freeze.ipynb
```python
# only load Variables, placeholder for input, and our logits
strings=','.join([n.name for n in tf.get_default_graph().as_graph_def().node if "Variable" in n.op or n.name.find('Placeholder') >= 0 or n.name.find('logits') == 0])
freeze_graph("", strings)
g=load_graph('frozen_model.pb')
```

#### How to initiate multi-workers using Gunicorn on top of flask, check comparison-request-gunicorn-dynamic.ipynb
```bash
bash run-gunicorn-dynamic.sh number_worker
```

```bash
NUM_WORKER=$1
# bind with any ip and port
BIND_ADDR=0.0.0.0:8033
# which api you want to bind. right now i binded with api_dynamic
gunicorn -w $NUM_WORKER -b $BIND_ADDR -p gunicorn.pid api_dynamic:app
```


## Results

#### Spawn Comparison, comparison-request.ipynb
```text
# for dynamic graph
CPU times: user 816 ms, sys: 40 ms, total: 856 ms
Wall time: 811 ms

# for static graph
CPU times: user 72 ms, sys: 8 ms, total: 80 ms
Wall time: 75.8 ms
```

#### Concurrent stress test
```text
# Stress test 20 requests concurrently on dynamic graph
thread 0, time taken 0.040708 s
thread 2, time taken 0.072802 s
thread 1, time taken 0.092469 s
thread 4, time taken 0.108417 s
thread 7, time taken 0.125185 s
thread 9, time taken 0.146564 s
thread 17, time taken 0.160176 s
thread 3, time taken 0.196733 s
thread 6, time taken 0.212126 s
thread 10, time taken 0.230030 s
thread 11, time taken 0.250885 s
thread 15, time taken 0.269423 s
thread 13, time taken 0.290279 s
thread 18, time taken 0.308505 s
thread 19, time taken 0.327376 s
thread 5, time taken 0.364115 s
thread 8, time taken 0.380689 s
thread 14, time taken 0.395581 s
thread 12, time taken 0.417496 s
thread 16, time taken 0.430993 s
total time taken 4.820551 s, average time taken 0.241028 s

# Stress test 20 requests concurrently on static graph
thread 0, time taken 0.052546 s
thread 1, time taken 0.087430 s
thread 2, time taken 0.111106 s
thread 4, time taken 0.129980 s
thread 5, time taken 0.139806 s
thread 8, time taken 0.164908 s
thread 10, time taken 0.169885 s
thread 13, time taken 0.209557 s
thread 16, time taken 0.213291 s
thread 18, time taken 0.236292 s
thread 6, time taken 0.267163 s
thread 9, time taken 0.311357 s
thread 14, time taken 0.314128 s
thread 11, time taken 0.327267 s
thread 19, time taken 0.364782 s
thread 7, time taken 0.382049 s
thread 12, time taken 0.384515 s
thread 15, time taken 0.427014 s
thread 17, time taken 0.428580 s
thread 3, time taken 0.461565 s
total time taken 5.183223 s, average time taken 0.259161 s

# Run 5 experiments on stress test 20 requests concurrently on dynamic graph
time taken to run experiments 27.863281 s, average 5.572656 s

# Run 5 experiments on stress test 20 requests concurrently on static graph
time taken to run experiments 26.089081 s, average 5.217816 s
```

#### Multi-workers comparison
![alt text](gunicorn/comparison.png)

*It really depends on physical server specifications*
