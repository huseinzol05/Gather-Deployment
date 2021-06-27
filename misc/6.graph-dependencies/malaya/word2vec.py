import collections
import re
import numpy as np
import tensorflow as tf
from sklearn.utils import shuffle
from sklearn.manifold import TSNE
from scipy.spatial.distance import cdist
from urllib.request import urlretrieve
import pickle
import os
import sys
from sklearn.neighbors import NearestNeighbors
from pathlib import Path
from .utils import *

home = str(Path.home())+'/Malaya'

def get_word2vec(size=256):
    if size not in [32,64,128,256,512]:
        raise Exception('size word2vec not supported')
    if not os.path.isfile('%s/word2vec-%d.p'%(home,size)):
        print('downloading word2vec-%d embedded'%(size))
        download_file('http://s3-ap-southeast-1.amazonaws.com/huseinhouse-storage/word2vec-%d.p'%(size),'%s/word2vec-%d.p'%(home,size))
    with open('%s/word2vec-%d.p'%(home,size), 'rb') as fopen:
        return pickle.load(fopen)

def counter_words(sentences):
    word_counter = collections.Counter()
    word_list = []
    num_lines, num_words = (0, 0)
    for i in sentences:
        words = re.findall("[\\w']+|[;:\-\(\)&.,!?\"]", i)
        word_counter.update(words)
        word_list.extend(words)
        num_lines += 1
        num_words += len(words)
    return word_counter, word_list, num_lines, num_words

def build_dict(word_counter, vocab_size=50000):
    top_words = word_counter.most_common(vocab_size)
    top_words.sort(key=lambda t: -t[1])
    dictionary = dict()
    for idx, word in enumerate(map(lambda t: t[0], top_words)):
        dictionary[word] = idx
    return dictionary, {word: idx for idx, word in dictionary.items()}

def doc2num(word_list, dictionary):
    word_array = []
    unknown_val = len(dictionary)
    for word in word_list:
        word_array.append(dictionary.get(word, unknown_val))
    return np.array(word_array, dtype=np.int32)

def build_word_array(sentences, vocab_size):
    word_counter, word_list, num_lines, num_words = counter_words(sentences)
    dictionary, rev_dictionary = build_dict(word_counter, vocab_size)
    word_array = doc2num(word_list, dictionary)
    return word_array, dictionary, rev_dictionary, num_lines, num_words

def build_training_set(word_array):
    num_words = len(word_array)
    x = np.zeros((num_words-4, 4), dtype=np.int32)
    y = np.zeros((num_words-4, 1), dtype=np.int32)
    shift = np.array([-2, -1, 1, 2], dtype=np.int32)
    for idx in range(2, num_words-2):
        y[idx-2, 0] = word_array[idx]
        x[idx-2, :] = word_array[idx+shift]
    return x, y

class Model:
    def __init__(self, graph_params):
        g_params = graph_params
        tf.reset_default_graph()
        self.sess = tf.InteractiveSession()
        self.X = tf.placeholder(tf.int64, shape=[None, 4])
        self.Y = tf.placeholder(tf.int64, shape=[None, 1])
        w_m2, w_m1, w_p1, w_p2 = tf.unstack(self.X, axis=1)
        self.embed_weights = tf.Variable(tf.random_uniform([g_params['vocab_size'],g_params['embed_size']],
                                                            -g_params['embed_noise'],g_params['embed_noise']))
        embed_m2 = tf.nn.embedding_lookup(self.embed_weights, w_m2)
        embed_m1 = tf.nn.embedding_lookup(self.embed_weights, w_m1)
        embed_p1 = tf.nn.embedding_lookup(self.embed_weights, w_p1)
        embed_p2 = tf.nn.embedding_lookup(self.embed_weights, w_p2)
        embed_stack = tf.concat([embed_m2, embed_m1, embed_p1, embed_p2],1)
        hid_weights = tf.Variable(tf.random_normal([g_params['embed_size'] * 4,
                                                    g_params['hid_size']],
                                                   stddev=g_params['hid_noise']/(g_params['embed_size'] * 4)**0.5))
        hid_bias = tf.Variable(tf.zeros([g_params['hid_size']]))
        hid_out = tf.nn.tanh(tf.matmul(embed_stack, hid_weights) + hid_bias)
        self.nce_weights = tf.Variable(tf.random_normal([g_params['vocab_size'],
                                                         g_params['hid_size']],
                                                        stddev=1.0 / g_params['hid_size'] ** 0.5))
        nce_bias = tf.Variable(tf.zeros([g_params['vocab_size']]))
        self.cost = tf.reduce_mean(tf.nn.nce_loss(self.nce_weights, nce_bias,
                                                  inputs=hid_out, labels=self.Y,
                                                  num_sampled=g_params['neg_samples'],
                                                  num_classes=g_params['vocab_size'],
                                                  num_true=1, remove_accidental_hits=True))
        self.logits = tf.argmax(tf.matmul(hid_out,self.nce_weights, transpose_b=True) + nce_bias, axis=1)
        if g_params['optimizer'] == 'RMSProp':
            self.optimizer = tf.train.RMSPropOptimizer(g_params['learn_rate']).minimize(self.cost)
        elif g_params['optimizer'] == 'Momentum':
            self.optimizer = tf.train.MomentumOptimizer(g_params['learn_rate'],
                                                        g_params['momentum']).minimize(self.cost)
        elif g_params['optimizer'] == 'Adam':
            self.optimizer = tf.train.AdamOptimizer(g_params['learn_rate']).minimize(self.cost)
        else:
            print('Optimizer not supported,exit.')
        self.sess.run(tf.global_variables_initializer())

    def train(self,X, Y, X_val, Y_val,epoch,batch_size):
        num_batches = len(X) // batch_size
        avg_loss, avg_loss_count, batch_count = (0, 0, 0)
        e_train, e_val = ([], [])
        for i in range(1, epoch+1):
            avg_loss, avg_loss_count = (0, 0)
            X, Y = shuffle(X, Y)
            for batch in range(num_batches):
                bot_idx = batch * batch_size
                top_idx = bot_idx + batch_size
                feed_dict = {self.X: X[bot_idx:top_idx, :],self.Y: Y[bot_idx:top_idx, :]}
                _, loss = self.sess.run([self.optimizer,self.cost],feed_dict=feed_dict)
                avg_loss += loss
                avg_loss_count += 1
                batch_count += 1
            num_batches = X_val.shape[0] // batch_size
            avg_loss = avg_loss / avg_loss_count
            e_train.append(avg_loss)
            val_loss = 0
            for batch in range(num_batches):
                bot_idx = batch * batch_size
                top_idx = bot_idx + batch_size
                feed_dict = {self.X: X_val[bot_idx:top_idx, :],
                             self.Y: Y_val[bot_idx:top_idx, :]}
                val_loss += self.sess.run(self.cost, feed_dict=feed_dict)
            val_loss = val_loss / num_batches
            e_val.append(val_loss)
            print('epoch %d, total batch %d, train loss %f, val loss %f'%(i,batch_count,avg_loss, val_loss))
        return self.embed_weights.eval(), self.nce_weights.eval()

class Word2Vec:
    def __init__(self,embed_matrix, dictionary):
        self._embed_matrix = embed_matrix
        self._dictionary = dictionary
        self._reverse_dictionary = {v: k for k, v in dictionary.items()}

    def get_vector_by_name(self, word):
        return np.ravel(self._embed_matrix[self._dictionary[word], :])

    def n_closest(self, word, num_closest=5, metric='cosine', return_similarity=True):
        if return_similarity:
            nn = NearestNeighbors(num_closest + 1,metric=metric).fit(self._embed_matrix)
            distances, idx = nn.kneighbors(self._embed_matrix[self._dictionary[word], :].reshape((1,-1)))
            word_list = []
            for i in range(1,idx.shape[1]):
                word_list.append([self._reverse_dictionary[idx[0,i]],1-distances[0,i]])
            return word_list
        else:
            wv = self.get_vector_by_name(word)
            closest_indices = self.closest_row_indices(wv, num_closest + 1, metric)
            word_list = []
            for i in closest_indices:
                word_list.append(self._reverse_dictionary[i])
            if word in word_list:
                word_list.remove(word)
            return word_list

    def closest_row_indices(self, wv, num, metric):
        dist_array = np.ravel(cdist(self._embed_matrix, wv.reshape((1, -1)),metric=metric))
        sorted_indices = np.argsort(dist_array)
        return sorted_indices[:num]

    def analogy(self, a, b, c, num=1, metric='cosine'):
        va = self.get_vector_by_name(a)
        vb = self.get_vector_by_name(b)
        vc = self.get_vector_by_name(c)
        vd = vb - va + vc
        closest_indices = self.closest_row_indices(vd, num, metric)
        d_word_list = []
        for i in closest_indices:
            d_word_list.append(self._reverse_dictionary[i])
        return d_word_list

    def project_2d(self, start, end):
        tsne = TSNE(n_components=2)
        embed_2d = tsne.fit_transform(self._embed_matrix[start:end, :])
        word_list = []
        for i in range(start, end):
            word_list.append(self._reverse_dictionary[i])
        return embed_2d, word_list
