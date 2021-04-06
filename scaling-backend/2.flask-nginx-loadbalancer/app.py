from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host = 'redis', port = 6379)


@app.route('/')
def hello():
    count = redis.incr('hits')
    return 'Hello World! I have been seen {} times.\n'.format(count)
