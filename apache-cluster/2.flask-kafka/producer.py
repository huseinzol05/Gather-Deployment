from time import sleep
import requests
import json
from bs4 import BeautifulSoup
from kafka import KafkaProducer


def parse(markup):
    title = '-'
    submit_by = '-'
    description = '-'
    calories = 0
    ingredients = []
    rec = {}

    try:
        soup = BeautifulSoup(markup, 'lxml')
        title_section = soup.select('.recipe-summary__h1')
        submitter_section = soup.select('.submitter__name')
        description_section = soup.select('.submitter__description')
        ingredients_section = soup.select('.recipe-ingred_txt')
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
            description = description_section[0].text.strip().replace('"', '')

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


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding = 'utf-8')
        value_bytes = bytes(value, encoding = 'utf-8')
        producer_instance.send(topic_name, key = key_bytes, value = value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(
            bootstrap_servers = ['localhost:9092'], api_version = (0, 10)
        )
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


def fetch_raw(recipe_url):
    html = None
    print('Processing..{}'.format(recipe_url))
    try:
        r = requests.get(recipe_url, headers = headers)
        if r.status_code == 200:
            html = r.text
    except Exception as ex:
        print('Exception while accessing raw html')
        print(str(ex))
    finally:
        return html.strip()


def get_recipes():
    recipies = []
    salad_url = 'https://www.allrecipes.com/recipes/96/salad/'
    url = 'https://www.allrecipes.com/recipes/96/salad/'
    print('Accessing list')

    try:
        r = requests.get(url, headers = headers)
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            links = soup.select('.fixed-recipe-card__h3 a')
            idx = 0
            for link in links:
                sleep(2)
                recipe = fetch_raw(link['href'])
                recipies.append(parse(recipe.strip()))
                idx += 1
    except Exception as ex:
        print('Exception in get_recipes')
        print(str(ex))
    finally:
        return recipies


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Pragma': 'no-cache',
    }

    all_recipes = get_recipes()
    if len(all_recipes) > 0:
        kafka_producer = connect_kafka_producer()
        for recipe in all_recipes:
            publish_message(kafka_producer, 'recipes', 'recipe', recipe)
        if kafka_producer is not None:
            kafka_producer.close()
