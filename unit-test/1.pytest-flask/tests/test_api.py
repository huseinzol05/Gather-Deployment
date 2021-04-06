from urllib.parse import urlencode
import json


def call(client, path, params):
    url = path + '?' + urlencode(params)
    response = client.get(url)
    return json.loads(response.data.decode('utf-8'))


def test_plus_one(client):
    result = call(client, '/plus_one', {'x': 2})
    assert result['x'] == 3


def test_square(client):
    result = call(client, '/square', {'x': 2})
    assert result['x'] == 4
