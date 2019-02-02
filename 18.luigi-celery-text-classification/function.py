import tensorflow as tf
import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import luigi
import re
import json


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
emotion_label = ['anger', 'fear', 'joy', 'love', 'sadness', 'surprise']


def classify_sentiment(text):
    text = clearstring(text)
    batch_x = str_idx([text], dict_sentiment['dictionary'], 100)
    output_sentiment = sess_sentiment.run(
        logits_sentiment, feed_dict = {x_sentiment: batch_x}
    )
    return [sentiment_label[i] for i in np.argmax(output_sentiment, 1)][0]


class Sentiment(luigi.Task):
    filename = luigi.Parameter()
    summary = luigi.Parameter()
    batch_size = luigi.IntParameter(default = 32)

    def output(self):
        return luigi.LocalTarget('%s-sentiment.json' % (self.summary))

    def run(self):

        g_sentiment = load_graph('sentiment.pb')
        x_sentiment = g_sentiment.get_tensor_by_name('import/Placeholder:0')
        logits_sentiment = g_sentiment.get_tensor_by_name('import/logits:0')
        sess_sentiment = tf.InteractiveSession(graph = g_sentiment)

        with open('fast-text-sentiment.json') as fopen:
            dict_sentiment = json.load(fopen)

        with open(self.filename) as fopen:
            texts = list(filter(None, fopen.read().split('\n')))
        results = []
        for i in range(0, len(texts), self.batch_size):
            batch_x_text = texts[i : min(i + self.batch_size, len(texts))]
            batch_x_text = [clearstring(t) for t in batch_x_text]
            batch_x = str_idx(batch_x_text, dict_sentiment['dictionary'], 100)
            output_sentiment = sess_sentiment.run(
                logits_sentiment, feed_dict = {x_sentiment: batch_x}
            )
            labels = [
                sentiment_label[l] for l in np.argmax(output_sentiment, 1)
            ]
            for no, text in enumerate(batch_x_text):
                results.append({'text': text, 'sentiment_label': labels[no]})
        with self.output().open('w') as fopen:
            fopen.write(json.dumps(results))


class Emotion(luigi.Task):
    filename = luigi.Parameter()
    summary = luigi.Parameter()
    batch_size = luigi.IntParameter(default = 32)

    def output(self):
        return luigi.LocalTarget('%s-emotion.json' % (self.summary))

    def requires(self):
        return {
            'Sentiment': Sentiment(
                filename = self.filename,
                summary = self.summary,
                batch_size = self.batch_size,
            )
        }

    def run(self):
        g_emotion = load_graph('emotion.pb')
        x_emotion = g_emotion.get_tensor_by_name('import/Placeholder:0')
        logits_emotion = g_emotion.get_tensor_by_name('import/logits:0')
        sess_emotion = tf.InteractiveSession(graph = g_emotion)

        with open('fast-text-emotion.json') as fopen:
            dict_emotion = json.load(fopen)

        with self.input()['Sentiment'].open('r') as fopen:
            outputs = json.load(fopen)
        for i in range(0, len(outputs), self.batch_size):
            batch_x_text = outputs[i : min(i + self.batch_size, len(outputs))]
            batch_x_text = [t['text'] for t in batch_x_text]
            batch_x_text = [clearstring(t) for t in batch_x_text]
            batch_x = str_idx(batch_x_text, dict_emotion['dictionary'], 100)
            output_emotion = sess_emotion.run(
                logits_emotion, feed_dict = {x_emotion: batch_x}
            )
            labels = [emotion_label[l] for l in np.argmax(output_emotion, 1)]
            for no, label in enumerate(labels):
                outputs[i + no]['emotion_label'] = label

        with self.output().open('w') as fopen:
            fopen.write(json.dumps(outputs))


class Save_to_Elastic(luigi.Task):
    filename = luigi.Parameter()
    summary = luigi.Parameter()
    index = luigi.Parameter()
    batch_size = luigi.IntParameter(default = 32)

    def requires(self):
        return {
            'Emotion': Emotion(
                filename = self.filename,
                summary = self.summary,
                batch_size = self.batch_size,
            )
        }

    def run(self):
        with self.input()['Emotion'].open('r') as fopen:
            emotions = json.load(fopen)
        es = Elasticsearch()
        for i in range(0, len(emotions), self.batch_size):
            batch = emotions[i : min(i + self.batch_size, len(emotions))]
            actions = [
                {
                    '_index': self.index,
                    '_type': 'text',
                    '_id': '%d-%s' % (i + j, self.summary),
                    '_source': batch[j],
                }
                for j in range(len(batch))
            ]
            helpers.bulk(es, actions)
