from flask import Flask, request, jsonify
from textblob import TextBlob
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons
from ekphrasis.classes.spellcorrect import SpellCorrector

text_processor = TextPreProcessor(
    normalize = [
        'url',
        'email',
        'percent',
        'money',
        'phone',
        'user',
        'time',
        'url',
        'date',
        'number',
    ],
    annotate = {
        'hashtag',
        'allcaps',
        'elongated',
        'repeated',
        'emphasis',
        'censored',
    },
    fix_html = True,
    segmenter = 'twitter',
    corrector = 'twitter',
    unpack_hashtags = True,
    unpack_contractions = True,
    spell_correct_elong = False,
    tokenizer = SocialTokenizer(lowercase = True).tokenize,
    dicts = [emoticons],
)

sp = SpellCorrector(corpus = 'english')
app = Flask(__name__)


def process_text(string):
    return ' '.join(
        [
            sp.correct(c)
            for c in text_processor.pre_process_doc(string)
            if '<' not in c
            and '>' not in c
            and c not in ',!;:{}\'"!@#$%^&*(01234567890?/|\\'
        ]
    )


@app.route('/', methods = ['GET'])
def hello():
    return 'Hello!'


@app.route('/classify', methods = ['GET'])
def classify():
    text = request.args.get('text')
    result = TextBlob(process_text(text))
    return jsonify(
        {
            'polarity': result.sentiment.polarity,
            'subjectivity': result.sentiment.subjectivity,
        }
    )


application = app
