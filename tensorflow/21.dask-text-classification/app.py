import dask.bag as db
import dask.dataframe as dd
import numpy as np
from dask import delayed
import dask.array as da
import tensorflow as tf
import re
import json


def clearstring(string):
    string = re.sub('[^A-Za-z0-9 ]+', ' ', string)
    string = re.sub(r'[ ]+', ' ', string.lower()).strip()
    return string.lower()


def load_graph(frozen_graph_filename):
    with tf.gfile.GFile(frozen_graph_filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def)
    return graph


def str_idx(corpus, dic, maxlen, UNK = 3):
    X = np.zeros((len(corpus), maxlen))
    for i in range(len(corpus)):
        for no, k in enumerate(corpus[i].split()[:maxlen][::-1]):
            X[i, -1 - no] = dic.get(k, UNK)
    return X


sentiment_label = ['negative', 'positive']
g_sentiment = load_graph('sentiment.pb')
x_sentiment = g_sentiment.get_tensor_by_name('import/Placeholder:0')
logits_sentiment = g_sentiment.get_tensor_by_name('import/logits:0')
sess_sentiment = tf.InteractiveSession(graph = g_sentiment)

with open('fast-text-sentiment.json') as fopen:
    dict_sentiment = json.load(fopen)


def classify(texts):
    batch_x_text = [clearstring(t) for t in texts]
    batch_x = str_idx(batch_x_text, dict_sentiment['dictionary'], 100)
    output_sentiment = sess_sentiment.run(
        logits_sentiment, feed_dict = {x_sentiment: batch_x}
    )
    labels = [sentiment_label[l] for l in np.argmax(output_sentiment, 1)]
    return da.stack(labels, axis = 0)


b = db.read_text('big-text.txt')
stacked = da.stack(b, axis = 0).rechunk(20)
result = stacked.map_blocks(classify).rechunk(-1)
da.to_npy_stack('./', result)
