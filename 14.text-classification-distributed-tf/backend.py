import sys

task_number = int(sys.argv[1])

import tensorflow as tf

cluster = tf.train.ClusterSpec(
    {'worker': ['192.168.0.101:2222', '192.168.0.104:2223']}
)
server = tf.train.Server(cluster, job_name = 'worker', task_index = task_number)

print('Starting server #{}'.format(task_number))

server.start()
server.join()
