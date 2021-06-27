from flask import Flask, request
from pymongo import MongoClient
import json

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.test_database
posts = db.posts


@app.route('/')
def hello_world():
    return 'Hey, we have Flask with MongoDB in a Docker container!'


@app.route('/insert', methods = ['GET'])
def insert():
    if not request.args.get('name'):
        return 'insert name'
    posts.insert_one({'name': request.args.get('name')})
    return 'done inserted ' + request.args.get('name')


@app.route('/get', methods = ['GET'])
def get():
    if not request.args.get('name'):
        return 'insert name'
    try:
        return posts.find_one({'name': request.args.get('name')})['name']
    except:
        return 'not found'


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
