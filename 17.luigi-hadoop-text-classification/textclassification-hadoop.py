#!/usr/bin/python3

import luigi
import tensorflow as tf
import luigi.contrib.hadoop
import luigi.contrib.hdfs
import json
import numpy as np
import time

class Split_text(luigi.Task):
    filename = luigi.Parameter()
    split_size = luigi.IntParameter(default = 5)
    
    def output(self):
        return [luigi.contrib.hdfs.target.HdfsTarget('/user/input_text/text-%d.txt' % (i)) for i in range(self.split_size)]
    
    def run(self):
        with open(self.filename) as fopen:
            texts = list(filter(None, fopen.read().split('\n')))
        splitted_list = np.array_split(texts, self.split_size)
        for i in range(len(splitted_list)):
            splitted_list[i] = splitted_list[i].tolist()
        for no, file in enumerate(self.output()):
            with file.open('w') as fopen:
                fopen.write('\n'.join(splitted_list[no]))

class Classification_Hadoop(luigi.contrib.hadoop.JobTask):
    filename = luigi.Parameter()
    split_size = luigi.IntParameter(default = 5)

    def requires(self):
        return Split_text(filename = self.filename, split_size = self.split_size)
    
    def extra_files(self):
        return ['frozen_model.pb','dictionary-test.json']

    def output(self):
        return luigi.contrib.hdfs.target.HdfsTarget('/user/input_text/classification')

    def mapper(self, line):
        
        def load_graph(frozen_graph_filename):
            with tf.gfile.GFile(frozen_graph_filename, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
            with tf.Graph().as_default() as graph:
                tf.import_graph_def(graph_def)
            return graph

        g = load_graph('frozen_model.pb')

        label = ['negative', 'positive']

        X = g.get_tensor_by_name('import/Placeholder:0')
        Y = g.get_tensor_by_name('import/logits:0')
        sess = tf.InteractiveSession(graph = g)
        maxlen = 50
        UNK = 3

        with open('dictionary-test.json', 'r') as fopen:
            dic = json.load(fopen)
            
        sentences = list(filter(None, line.split('\n')))
        x = np.zeros((len(sentences), maxlen))
        for i, sentence in enumerate(sentences):
            for no, k in enumerate(sentence.split()[:maxlen][::-1]):
                x[i, -1 - no] = dic.get(k,UNK)
        indices = np.argmax(sess.run(Y, feed_dict = {X: x}), axis = 1)
        for no, index in enumerate(indices):
            yield '%s: %s' %(sentences[no], label[index]), 1
                
    def reducer(self, key, values):
        yield key, sum(values)