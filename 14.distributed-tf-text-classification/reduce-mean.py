import tensorflow as tf
import numpy as np

cluster = tf.train.ClusterSpec(
    {'worker': ['192.168.0.101:2222', '192.168.0.104:2223']}
)

x = tf.placeholder(tf.float32, 100)

with tf.device('/job:worker/task:1'):
    first_batch = tf.slice(x, [0], [50])
    mean1 = tf.reduce_mean(first_batch)

with tf.device('/job:worker/task:0'):
    second_batch = tf.slice(x, [50], [-1])
    mean2 = tf.reduce_mean(second_batch)
    mean = (mean1 + mean2) / 2

sess = tf.InteractiveSession('grpc://192.168.0.101:2222')
result = sess.run(mean, feed_dict = {x: np.random.random(100)})
print(result)
