from flask import Flask, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
import requests
import json
from bs4 import BeautifulSoup


def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        'settings': {'number_of_shards': 1, 'number_of_replicas': 0},
        'mappings': {
            'salads': {
                'dynamic': 'strict',
                'properties': {
                    'title': {'type': 'text'},
                    'submitter': {'type': 'text'},
                    'description': {'type': 'text'},
                    'calories': {'type': 'integer'},
                    'ingredients': {
                        'type': 'nested',
                        'properties': {'step': {'type': 'text'}},
                    },
                },
            }
        },
    }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(
                index = index_name, ignore = 400, body = settings
            )
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    is_stored = True
    try:
        outcome = elastic_object.index(
            index = index_name, doc_type = 'salads', body = record
        )
        print(outcome)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False
    finally:
        return is_stored


def parse(u):
    title = '-'
    submit_by = '-'
    description = '-'
    calories = 0
    ingredients = []
    rec = {}

    try:
        r = requests.get(u, headers = headers)

        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            # title
            title_section = soup.select('.recipe-summary__h1')
            # submitter
            submitter_section = soup.select('.submitter__name')
            # description
            description_section = soup.select('.submitter__description')
            # ingredients
            ingredients_section = soup.select('.recipe-ingred_txt')

            # calories
            calories_section = soup.select('.calorie-count')
            if calories_section:
                calories = calories_section[0].text.replace('cals', '').strip()

            if ingredients_section:
                for ingredient in ingredients_section:
                    ingredient_text = ingredient.text.strip()
                    if (
                        'Add all ingredients to list' not in ingredient_text
                        and ingredient_text != ''
                    ):
                        ingredients.append({'step': ingredient.text.strip()})

            if description_section:
                description = (
                    description_section[0].text.strip().replace('"', '')
                )

            if submitter_section:
                submit_by = submitter_section[0].text.strip()

            if title_section:
                title = title_section[0].text

            rec = {
                'title': title,
                'submitter': submit_by,
                'description': description,
                'calories': calories,
                'ingredients': ingredients,
            }
    except Exception as ex:
        print('Exception while parsing')
        print(str(ex))
    finally:
        return json.dumps(rec)


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Pragma': 'no-cache',
}
url = 'https://www.allrecipes.com/recipes/96/salad/'
r = requests.get(url, headers = headers)
if r.status_code == 200:
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    links = soup.select('.fixed-recipe-card__h3 a')

    for no, link in enumerate(links[:5]):
        result = parse(link['href'])
        if create_index(es, 'recipes'):
            out = store_record(es, 'recipes', result)
            print(no, 'Data indexed successfully')


@app.route('/')
def hello_world():
    return 'Hey, we have Flask with Elastic Search in a Docker container!'


@app.route('/ping')
def ping():
    global es
    if es.ping():
        return 'connected to elastic search'
    else:
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        return 'cannot connect to elastic search, reconnecting..'


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
