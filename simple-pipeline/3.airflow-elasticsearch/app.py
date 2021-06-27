from flask import Flask, request, render_template, jsonify
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

app = Flask(__name__)


def get_es(index = 'test_index'):
    es = Elasticsearch()
    return Search(using = es, index = index)


def get_sentiment(sentiment):
    s = get_es()
    s = s.filter('terms', sentiment_label__keyword = [sentiment])
    return s.execute().to_dict()


@app.route('/', methods = ['GET'])
def hello():
    return 'HOLLA!'


@app.route('/index/<sentiment>')
def indexing(sentiment):
    if not sentiment:
        return jsonify({'error': 'insert sentiment'})
    return jsonify(get_sentiment(sentiment))


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
