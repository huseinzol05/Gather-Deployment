from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import redis
import json

app = Flask(__name__)
api = Api(app)
r = redis.StrictRedis(host = 'localhost', port = 6379, db = 0)
publishers = {'first-channel': r.pubsub(), 'second-channel': r.pubsub()}
publishers['first-channel'].subscribe('first-channel')
publishers['second-channel'].subscribe('second-channel')


@app.route('/')
def hello_world():
    return 'Hey, we have Flask with Redis in a Docker container!'


@app.route('/insert', methods = ['GET'])
def insert():
    dictionary = request.args.to_dict()
    filtered_dictionary = {
        i: dictionary[i] for i in dictionary.keys() if i not in ['name']
    }
    r.set(dictionary['name'], json.dumps(filtered_dictionary))
    return 'inserted into redis'


@app.route('/get', methods = ['GET'])
def get():
    try:
        return r.get(request.args.get('name')).decode('utf-8')
    except:
        return 'not found'


class Publishers(Resource):
    def get(self, id):
        try:
            return publishers[id].get_message()['data'].decode('utf-8')
        except:
            return publishers[id].get_message()['data']

    def put(self, id):
        r.publish(id, request.form['data'])
        return request.form['data']

    def post(self, id):
        publishers[id] = r.pubsub()
        publishers[id].subscribe(id)
        return id, 201


api.add_resource(Publishers, '/<string:id>')

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
