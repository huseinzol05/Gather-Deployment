import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cPickle
import time
from word2vec import *
from model_nn import *
from setting import *

string, data, label = read_data()
location = os.getcwd()

try:
    with open('dictionary.p', 'rb') as fopen:
        dictionary = cPickle.load(fopen)
    with open('vectors.p', 'rb') as fopen:
        vectors = cPickle.load(fopen)
    print "done load embedded files"
except:
    print "Not found any embedded files, creating new.."
    dictionary, reverse_dictionary, vectors = generatevector(dimension, dimension, skip_size, skip_window, num_skips, iteration_train_vectors, string)
    with open('dictionary.p', 'wb') as fopen:
        cPickle.dump(dictionary, fopen)
    with open('vectors.p', 'wb') as fopen:
        cPickle.dump(vectors, fopen)

print "sentence size: " + str(data.shape[0])
sess = tf.InteractiveSession()
model = Model(num_layers, size_layer, dimension, len(label), learning_rate)
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver(tf.global_variables())

try:
    saver.restore(sess, location + "/model.ckpt")
    print "load model.."
except:
    print "start from fresh variables"

for n in range(epoch):
    total_cost, total_accuracy, last_time = 0, 0, time.time()
    for i in range(0, (data.shape[0] // batch) * batch, batch):
        batch_x = np.zeros((batch, maxlen, dimension))
        batch_y = np.zeros((batch, len(label)))
        for k in range(batch):
            tokens = data[i + k, 0].split()[:maxlen]
            emb_data = np.zeros((maxlen, dimension), dtype = np.float32)
            for no, text in enumerate(tokens[::-1]):
                try:
                    emb_data[-1 - no, :] += vectors[dictionary[text], :]
                except:
                    continue
            batch_y[k, int(data[i + k, 1])] = 1.0
            batch_x[k, :, :] = emb_data[:, :]
        loss, _ = sess.run([model.cost, model.optimizer], feed_dict = {model.X : batch_x, model.Y : batch_y})
        total_accuracy += sess.run(model.accuracy, feed_dict = {model.X : batch_x, model.Y : batch_y})
        total_cost += loss
        
    diff = (time.time() - last_time) / (data.shape[0] // batch)
    total_accuracy /= (data.shape[0] // batch)
    total_cost /= (data.shape[0] // batch)
    print("total accuracy during training:", total_accuracy)
    print("epoch:", n + 1, "loss:", total_cost, "speed:", diff)
    saver.save(sess, location + "/model.ckpt")