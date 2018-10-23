import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
import cPickle
import time
from model_nn import *
from setting import *
import json
import re
from flask import Flask, render_template, request
from werkzeug import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

VOWELS = "aeiou"
PHONES = ['sh', 'ch', 'ph', 'sz', 'cz', 'sch', 'rz', 'dz']
label_sentiment = ['negative', 'positive']
label_emotion = ['anger', 'fear', 'joy', 'love', 'sadness', 'surprise']

# we still need to detect non-words, because our neural network still predict unrecognized word
# asdasdasdas is not word
def isWord(word):
    if len(word) < 2 and word.lower() != 'i':
        return False
    if word:
        consecutiveVowels = 0
        consecutiveConsonents = 0
        for idx, letter in enumerate(word.lower()):
            vowel = True if letter in VOWELS else False
            if idx:
                prev = word[idx-1]               
                prevVowel = True if prev in VOWELS else False
                if not vowel and letter == 'y' and not prevVowel:
                    vowel = True
                if prevVowel != vowel:
                    consecutiveVowels = 0
            if vowel:
                consecutiveVowels += 1
            else:
                consecutiveConsonents += 1
            if consecutiveVowels >= 3 or consecutiveConsonents > 4:
                return False
            if consecutiveConsonents == 4:
                subStr = word[idx - 2: idx + 1]
                if any(phone in subStr for phone in PHONES):
                    consecutiveConsonents -= 1
                    continue    
                return False
    return True

try:
    with open('sentiment/dictionary.p', 'rb') as fopen:
        dictionary = cPickle.load(fopen)
    with open('/sentiment/vectors.p', 'rb') as fopen:
        vectors = cPickle.load(fopen)
    print "done load sentiment embedded files"
except:
    print "allocate sentiment embedded files first"
    
try:
    with open('emotion/dictionary.p', 'rb') as fopen:
        dictionary_emotion = cPickle.load(fopen)
    with open('emotion/vectors.p', 'rb') as fopen:
        vectors_emotion = cPickle.load(fopen)
    print "done load emotion embedded files"
except:
    print "allocate emotion embedded files first"

# initiate our sentiment graph
sess = tf.InteractiveSession()
model = Model(num_layers, size_layer, dimension, len(label_sentiment), learning_rate)
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver(tf.global_variables())
saver.restore(sess, "sentiment/model.ckpt")

# initiate our second graph, emotion graph
emotion_graph = tf.Graph()
with emotion_graph.as_default():
    model_emotion = Model(num_layers, size_layer, dimension, len(label_emotion), learning_rate)
emotion_sess = tf.Session(graph = emotion_graph)
with emotion_sess.as_default():
    with emotion_graph.as_default():
        tf.global_variables_initializer().run()
        tf.train.Saver(tf.global_variables()).restore(emotion_sess, 'emotion/model.ckpt')
		
def clearstring(string):
    string = re.sub('[^A-Za-z0-9 ]+', '', string)
    string = string.split(' ')
    string = filter(None, string)
    string = [y.strip() for y in string]
    string = ' '.join(string)
    return string.lower()

@app.route('/sentiment', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return json.dumps({'error': 'only accept GET request'})
    else:
        if request.args.get('text'):
            try:
                text = clearstring(request.args.get('text'))
                if not np.unique(np.array([isWord(i) for i in text.split()]).astype(int), return_counts = True)[1].argmax():
                    return json.dumps({'error': 'insert proper words'})
                tokens = text.split()[:maxlen]
                if len(tokens) > 256:
                    return json.dumps({'error': 'sentence must not more than 256 words'})
                batch_x_sentiment = np.zeros((1, maxlen, dimension), dtype = np.float32)
                batch_x_emotion = np.zeros((1, maxlen, dimension), dtype = np.float32)
                for no, text in enumerate(tokens[::-1]):
                    try:
                        batch_x_sentiment[0, -1 - no, :] += vectors[dictionary[text], :]
                    except:
                        continue
                for no, text in enumerate(tokens[::-1]):
                    try:
                        batch_x_emotion[0, -1 - no, :] += vectors_emotion[dictionary_emotion[text], :]
                    except:
                        continue
                outputs_sentiment = sess.run(tf.nn.softmax(model.logits), feed_dict = {model.X : batch_x_sentiment})[0]
                outputs_emotion = emotion_sess.run(tf.nn.softmax(model_emotion.logits), feed_dict = {model_emotion.X : batch_x_emotion})[0]
                return json.dumps({'sentiment': outputs_sentiment.tolist(), 'emotion': outputs_emotion.tolist(), 
                                   'label_sentiment': label_sentiment, 'label_emotion': label_emotion})
            except Exception as e:
                return json.dumps({'error': str(e)})
		else:
            return json.dumps({'error': 'invalid parameters'})
        
if __name__ == '__main__':
    # 0.0.0.0 for public ip
    # define your port
    # thread = True if want multi-thread, depends on your OS
	app.run(host = '0.0.0.0', threaded = True,  port = 999999)