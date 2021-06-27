import numpy as np
import json
import pickle
from flask import Flask, render_template, request
from flask_cors import CORS
from sklearn.naive_bayes import MultinomialNB
import itertools
from tatabahasa import *
from unidecode import unidecode
import re

app = Flask(__name__)
CORS(app)

stopword_tatabahasa = list(set(tanya_list+perintah_list+pangkal_list+bantu_list+penguat_list+\
                penegas_list+nafi_list+pemeri_list+sendi_list+pembenar_list+nombor_list+\
                suku_bilangan_list+pisahan_list+keterangan_list+arah_list+hubung_list+gantinama_list))

with open('stop-word-kerulnet','r') as fopen:
    stopwords = list(filter(None, fopen.read().split('\n')))

with open('tfidf.p','rb') as fopen:
    tfidf = pickle.load(fopen)
with open('tfidf_bm.p','rb') as fopen:
    tfidf_bm = pickle.load(fopen)

with open('bayes.p','rb') as fopen:
    bayes = pickle.load(fopen)
with open('bayes_bm.p','rb') as fopen:
    bayes_bm = pickle.load(fopen)

VOWELS = "aeiou"
PHONES = ['sh', 'ch', 'ph', 'sz', 'cz', 'sch', 'rz', 'dz']

def isWord(word):
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
                    consecutiveConsonents = 0
            if vowel:
                consecutiveVowels += 1
            else:
                consecutiveConsonents +=1
            if consecutiveVowels >= 3 or consecutiveConsonents > 3:
                return False
            if consecutiveConsonents == 3:
                subStr = word[idx-2:idx+1]
                if any(phone in subStr for phone in PHONES):
                    consecutiveConsonents -= 1
                    continue
                return False
    return True

def stemming(word):
    try:
        word = re.findall(r'^(.*?)(%s)$'%('|'.join(hujung)), word)[0][0]
        mula = re.findall(r'^(.*?)(%s)'%('|'.join(permulaan[::-1])), word)[0][1]
        return word.replace(mula,'')
    except:
        return word

label = ['negative','positive']

list_stops = list(set(stopwords+stopword_tatabahasa))
list_laughing = ['huhu','haha','gaga','hihi','wkawka','wkwk','kiki','keke','rt']
def textcleaning(string):
    string = re.sub('http\S+|www.\S+', '',' '.join([i for i in string.split() if i.find('#')<0 and i.find('@')<0]))
    string = unidecode(string).replace('.', '. ')
    string = string.replace(',', ', ')
    string = re.sub('[^\'\"A-Za-z\- ]+', '', unidecode(string))
    string = [y.strip() for y in string.lower().split() if isWord(y.strip())]
    string = [stemming(y) for y in string if y not in list_stops]
    #string = [st.stem(y) for y in string]
    string = [y for y in string if all([y.find(k) < 0 for k in list_laughing]) and y[:len(y)//2] != y[len(y)//2:]]
    string = ' '.join(string).lower()
    string = (''.join(''.join(s)[:2] for _, s in itertools.groupby(string))).split()
    return ' '.join([y for y in string if y not in list_stops])

@app.route('/sentiment', methods = ['GET'])
def get_sentiment():
    string = textcleaning(request.args.get('text'))
    vectors = tfidf.transform([string])
    results = bayes.predict_proba(vectors)
    if results[0,0] == 0.5:
        vectors = tfidf_bm.transform([string])
        results = bayes_bm.predict_proba(vectors)
    u=np.where(results >= 0.6)
    res = []
    for i in range(results.shape[0]):
        if i in u[0]:
            res.append(label[np.argmax(results[i,:])])
        else:
            res.append('neutral')
    return json.dumps({'label':res[0],'string':string})

if __name__ == '__main__':
	app.run(host = '0.0.0.0', threaded = True, port = 8095)
