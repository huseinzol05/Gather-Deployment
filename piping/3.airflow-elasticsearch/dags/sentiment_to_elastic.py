import tensorflow as tf
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import re
import numpy as np
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
import os
import logging

DAG = DAG(
    dag_id = 'sentiment_to_elastic',
    start_date = datetime.now(),
    schedule_interval = None,
)


def clearstring(string):
    string = re.sub('[^A-Za-z0-9 ]+', '', string)
    string = string.split(' ')
    string = filter(None, string)
    string = [y.strip() for y in string]
    string = ' '.join(string)
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
batch_size = 32


def push_sentiment(**context):
    g_sentiment = load_graph('sentiment.pb')
    x_sentiment = g_sentiment.get_tensor_by_name('import/Placeholder:0')
    logits_sentiment = g_sentiment.get_tensor_by_name('import/logits:0')
    sess_sentiment = tf.InteractiveSession(graph = g_sentiment)

    with open('fast-text-sentiment.json') as fopen:
        dict_sentiment = json.load(fopen)

    with open('big-text.txt') as fopen:
        texts = list(filter(None, fopen.read().split('\n')))
    results = []

    for i in range(0, len(texts), batch_size):
        batch_x_text = texts[i : min(i + batch_size, len(texts))]
        batch_x_text = [clearstring(t) for t in batch_x_text]
        batch_x = str_idx(batch_x_text, dict_sentiment['dictionary'], 100)
        output_sentiment = sess_sentiment.run(
            logits_sentiment, feed_dict = {x_sentiment: batch_x}
        )
        labels = [sentiment_label[i] for i in np.argmax(output_sentiment, 1)]
        for no, text in enumerate(batch_x_text):
            results.append({'text': text, 'sentiment_label': labels[no]})

    task_instance = context['task_instance']
    task_instance.xcom_push(key = 'sentiment', value = results)


push_sentiment_task = PythonOperator(
    task_id = 'push_sentiment',
    python_callable = push_sentiment,
    provide_context = True,
    dag = DAG,
)


def pull_to_elastic(**kwargs):
    ti = kwargs['ti']
    sentiments = ti.xcom_pull(task_ids = 'push_sentiment', key = 'sentiment')
    es = Elasticsearch()
    for i in range(0, len(sentiments), batch_size):
        batch = sentiments[i : min(i + batch_size, len(sentiments))]
        actions = [
            {
                '_index': 'test_index',
                '_type': 'text',
                '_id': '%d-text' % (j + i),
                '_source': batch[j],
            }
            for j in range(len(batch))
        ]
        helpers.bulk(es, actions)


pull_to_elastic_task = PythonOperator(
    task_id = 'pull_to_elastic',
    python_callable = pull_to_elastic,
    provide_context = True,
    dag = DAG,
)

push_sentiment_task >> pull_to_elastic_task
