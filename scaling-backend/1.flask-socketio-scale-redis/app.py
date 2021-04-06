from flask import Flask
from flask_socketio import SocketIO, send, emit
import time
from flask import current_app
import json
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, message_queue = 'redis://')


@socketio.on('connect', namespace = '/live')
def test_connect():
    emit('response', {'data': 'OK'}, broadcast = True)


@socketio.on('disconnect', namespace = '/live')
def test_disconnect():
    print('Client disconnected')


@socketio.on('event', namespace = '/live')
def test_message(message):
    print('incoming from %s' % (message['id']))
    emit('event', {'data': message['id']}, broadcast = True)


application = app
