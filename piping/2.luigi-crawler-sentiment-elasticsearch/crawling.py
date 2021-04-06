import numpy as np
import json
import pickle
from sklearn.naive_bayes import MultinomialNB
import itertools
from tatabahasa import *
from core import *
from unidecode import unidecode
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import luigi
import re

stopword_tatabahasa = list(
    set(
        tanya_list
        + perintah_list
        + pangkal_list
        + bantu_list
        + penguat_list
        + penegas_list
        + nafi_list
        + pemeri_list
        + sendi_list
        + pembenar_list
        + nombor_list
        + suku_bilangan_list
        + pisahan_list
        + keterangan_list
        + arah_list
        + hubung_list
        + gantinama_list
    )
)

with open('sentiment/stop-word-kerulnet', 'r') as fopen:
    stopwords = list(filter(None, fopen.read().split('\n')))

with open('sentiment/tfidf.p', 'rb') as fopen:
    tfidf = pickle.load(fopen)
with open('sentiment/tfidf_bm.p', 'rb') as fopen:
    tfidf_bm = pickle.load(fopen)

with open('sentiment/bayes.p', 'rb') as fopen:
    bayes = pickle.load(fopen)
with open('sentiment/bayes_bm.p', 'rb') as fopen:
    bayes_bm = pickle.load(fopen)

VOWELS = 'aeiou'
PHONES = ['sh', 'ch', 'ph', 'sz', 'cz', 'sch', 'rz', 'dz']


def isWord(word):
    if word:
        consecutiveVowels = 0
        consecutiveConsonents = 0
        for idx, letter in enumerate(word.lower()):
            vowel = True if letter in VOWELS else False
            if idx:
                prev = word[idx - 1]
                prevVowel = True if prev in VOWELS else False
                if not vowel and letter == 'y' and not prevVowel:
                    vowel = True
                if prevVowel != vowel:
                    consecutiveVowels = 0
                    consecutiveConsonents = 0
            if vowel:
                consecutiveVowels += 1
            else:
                consecutiveConsonents += 1
            if consecutiveVowels >= 3 or consecutiveConsonents > 3:
                return False
            if consecutiveConsonents == 3:
                subStr = word[idx - 2 : idx + 1]
                if any(phone in subStr for phone in PHONES):
                    consecutiveConsonents -= 1
                    continue
                return False
    return True


def stemming(word):
    try:
        word = re.findall(r'^(.*?)(%s)$' % ('|'.join(hujung)), word)[0][0]
        mula = re.findall(r'^(.*?)(%s)' % ('|'.join(permulaan[::-1])), word)[0][
            1
        ]
        return word.replace(mula, '')
    except:
        return word


label = ['negative', 'positive']

list_stops = list(set(stopwords + stopword_tatabahasa))
list_laughing = [
    'huhu',
    'haha',
    'gaga',
    'hihi',
    'wkawka',
    'wkwk',
    'kiki',
    'keke',
    'rt',
]


def textcleaning(string):
    string = re.sub(
        'http\S+|www.\S+',
        '',
        ' '.join(
            [i for i in string.split() if i.find('#') < 0 and i.find('@') < 0]
        ),
    )
    string = unidecode(string).replace('.', '. ')
    string = string.replace(',', ', ')
    string = re.sub('[^\'"A-Za-z\- ]+', '', unidecode(string))
    string = [y.strip() for y in string.lower().split() if isWord(y.strip())]
    string = [stemming(y) for y in string if y not in list_stops]
    # string = [st.stem(y) for y in string]
    string = [
        y
        for y in string
        if all([y.find(k) < 0 for k in list_laughing])
        and y[: len(y) // 2] != y[len(y) // 2 :]
    ]
    string = ' '.join(string).lower()
    string = (
        ''.join(''.join(s)[:2] for _, s in itertools.groupby(string))
    ).split()
    return ' '.join([y for y in string if y not in list_stops])


def sentiment(text):
    string = textcleaning(text)
    vectors = tfidf.transform([string])
    results = bayes.predict_proba(vectors)
    if results[0, 0] == 0.5:
        vectors = tfidf_bm.transform([string])
        results = bayes_bm.predict_proba(vectors)
    u = np.where(results >= 0.6)
    res = []
    for i in range(results.shape[0]):
        if i in u[0]:
            res.append(label[np.argmax(results[i, :])])
        else:
            res.append('neutral')
    return res[0]


class Crawl(luigi.Task):
    issue = luigi.Parameter()
    year_start = luigi.IntParameter(default = 2010)
    year_end = luigi.IntParameter(default = 2019)
    limit = luigi.IntParameter(default = 1000)

    def output(self):
        return luigi.LocalTarget('%s.json' % (self.issue))

    def run(self):
        results = google_news_run(
            self.issue,
            limit = self.limit,
            year_start = self.year_start,
            year_end = self.year_end,
            debug = False,
            sleep_time_every_ten_articles = 10,
        )
        with self.output().open('w') as fopen:
            fopen.write(json.dumps(results))


class Sentiment(luigi.Task):
    issue = luigi.Parameter()
    year_start = luigi.IntParameter(default = 2010)
    year_end = luigi.IntParameter(default = 2019)
    limit = luigi.IntParameter(default = 1000)

    def output(self):
        return luigi.LocalTarget('%s-sentiment.json' % (self.issue))

    def requires(self):
        return {
            'Crawl': Crawl(
                issue = self.issue,
                year_start = self.year_start,
                year_end = self.year_end,
                limit = self.limit,
            )
        }

    def run(self):
        with self.input()['Crawl'].open('r') as fopen:
            crawled = json.loads(fopen.read())
        for i in range(len(crawled)):
            if len(crawled[i]['text']) < 2:
                crawled[i]['sentiment'] = 'null'
            else:
                crawled[i]['sentiment'] = sentiment(crawled[i]['text'])
        with self.output().open('w') as fopen:
            fopen.write(json.dumps(crawled))


class Save_to_Elastic(luigi.Task):
    issue = luigi.Parameter()
    year_start = luigi.IntParameter(default = 2010)
    year_end = luigi.IntParameter(default = 2019)
    limit = luigi.IntParameter(default = 1000)
    index = luigi.Parameter()
    batch_size = luigi.IntParameter(default = 10)

    def requires(self):
        return {
            'Sentiment': Sentiment(
                issue = self.issue,
                year_start = self.year_start,
                year_end = self.year_end,
                limit = self.limit,
            )
        }

    def run(self):
        with self.input()['Sentiment'].open('r') as fopen:
            sentiment = json.loads(fopen.read())
        es = Elasticsearch()
        for index in range(0, len(sentiment), self.batch_size):
            batch = sentiment[
                index : min(index + self.batch_size, len(sentiment))
            ]
            actions = [
                {
                    '_index': self.index,
                    '_type': 'news',
                    '_id': batch[j]['url'],
                    '_source': batch[j],
                }
                for j in range(len(batch))
            ]
            helpers.bulk(es, actions)
