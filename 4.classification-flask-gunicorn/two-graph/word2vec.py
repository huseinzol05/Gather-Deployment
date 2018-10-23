import collections
import numpy as np
import random
from model_word2vec import *
import cPickle
import time
import os
from sklearn.preprocessing import LabelEncoder
import re

def clearstring(string):
    string = re.sub('[^A-Za-z0-9 ]+', '', string)
    string = string.split(' ')
    string = filter(None, string)
    string = [y.strip() for y in string]
    string = ' '.join(string)
    return string.lower()

def read_data():
    list_folder = os.listdir('data/')
    label = list_folder
    label.sort()
    outer_string, outer_label = [], []
    for i in range(len(list_folder)):
        list_file = os.listdir('data/' + list_folder[i])
        strings = []
        for x in range(len(list_file)):
            with open('data/' + list_folder[i] + '/' + list_file[x], 'rb') as fopen:
                strings += fopen.read().split('\n')
        strings = filter(None, strings)
        for k in range(len(strings)):
            strings[k], length = clearstring(strings[k])
        labels = [i] * len(strings)
        outer_string += strings
        outer_label += labels
    
    dataset = np.array([outer_string, outer_label])
    dataset = dataset.T
    np.random.shuffle(dataset)
    
    string = []
    for i in range(dataset.shape[0]):
        string += dataset[i][0].split()
    
    return string, dataset, label
    
def build_dataset(words, vocabulary_size):
    count = []
    # extend count
    # sorted decending order of words
    count.extend(collections.Counter(words).most_common(vocabulary_size))
    dictionary = dict()
    for word, _ in count:
        #simply add dictionary of word, used frequently placed top
        dictionary[word] = len(dictionary) + 1
    data = []
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]

        data.append(index)
    dictionary['PAD'] = 0
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return data, dictionary, reverse_dictionary

def generate_batch_skipgram(words, batch_size, num_skips, skip_window):
    data_index = 0
    
    #check batch_size able to convert into number of skip in skip-grams method
    assert batch_size % num_skips == 0
    
    assert num_skips <= 2 * skip_window
    
    # create batch for model input
    batch = np.ndarray(shape=(batch_size), dtype=np.int32)
    labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    span = 2 * skip_window + 1
    
    # a buffer to placed skip-grams sentence
    buffer = collections.deque(maxlen=span)
    
    for i in xrange(span):
        buffer.append(words[data_index])
        data_index = (data_index + 1) % len(words)
    
    for i in xrange(batch_size // num_skips):
        target = skip_window
        targets_to_avoid = [skip_window]
        
        for j in xrange(num_skips):
            
            while target in targets_to_avoid:
                # random a word from the sentence
                # if random word still a word already chosen, simply keep looping
                target = random.randint(0, span - 1)
            
            targets_to_avoid.append(target)
            batch[i * num_skips + j] = buffer[skip_window]
            labels[i * num_skips + j, 0] = buffer[target]
        
        buffer.append(words[data_index])
        data_index = (data_index + 1) % len(words)
    
    data_index = (data_index + len(words) - span) % len(words)
    return batch, labels

def generatevector(dimension, batch_size, skip_size, skip_window, num_skips, iteration, words_real):
    
    print "Data size: " + str(len(words_real))

    data, dictionary, reverse_dictionary = build_dataset(words_real, len(words_real))
    
    sess = tf.InteractiveSession()
    print "Creating Word2Vec model.."
    
    model = Model(batch_size, dimension, 0.1, len(dictionary))
    sess.run(tf.global_variables_initializer())
    
    last_time = time.time()
    
    for step in xrange(iteration):
        new_time = time.time()
        batch_inputs, batch_labels = generate_batch_skipgram(data, batch_size, num_skips, skip_window)
        feed_dict = {model.train_inputs: batch_inputs, model.train_labels: batch_labels}
        
        _, loss = sess.run([model.optimizer, model.loss], feed_dict=feed_dict)
        
        if ((step + 1) % 1000) == 0:
            print "epoch: " + str(step + 1) + ", loss: " + str(loss) + ", speed: " + str((time.time() - new_time) * 1000) + " s / 1000 epoch"
    
    tf.reset_default_graph()       
    return dictionary, reverse_dictionary, model.normalized_embeddings.eval()