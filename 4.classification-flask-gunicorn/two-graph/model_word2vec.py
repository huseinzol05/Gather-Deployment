import tensorflow as tf
import numpy as np

class Model:
    
    def __init__(self, batch_size, dimension_size, learning_rate, vocabulary_size):
        
        self.train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
        self.train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
        
        # randomly generated initial value for each word dimension, between -1.0 to 1.0
        embeddings = tf.Variable(tf.random_uniform([vocabulary_size, dimension_size], -1.0, 1.0))
        
        # find train_inputs from embeddings
        embed = tf.nn.embedding_lookup(embeddings, self.train_inputs)
        
        # estimation for not normalized dataset
        self.nce_weights = tf.Variable(tf.truncated_normal([vocabulary_size, dimension_size], stddev = 1.0 / np.sqrt(dimension_size)))
        
        # each node have their own bias
        self.nce_biases = tf.Variable(tf.zeros([vocabulary_size]))
        
        # calculate loss from nce, then calculate mean
        self.loss = tf.reduce_mean(tf.nn.nce_loss(weights = self.nce_weights, biases = self.nce_biases, labels = self.train_labels,
                                                  inputs=embed, num_sampled = batch_size / 2, num_classes = vocabulary_size))
        
        #for a small neural network, for me, Adam works the best
        self.optimizer = tf.train.AdamOptimizer(learning_rate).minimize(self.loss)
        
        # normalize the data by simply reduce sum
        self.norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
        
        # normalizing each embed
        self.normalized_embeddings = embeddings / self.norm

