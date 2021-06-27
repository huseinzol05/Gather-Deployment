import os
import random
import time
from flask import Flask, jsonify
from celery import Celery

app = Flask(__name__)

celery = Celery(
    app.name, backend = 'rpc://', broker = 'amqp://guest:@localhost:5672//'
)
celery.conf.update(app.config)


@celery.task(bind = True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(
                random.choice(verb),
                random.choice(adjective),
                random.choice(noun),
            )
        self.update_state(
            state = 'PROGRESS',
            meta = {'current': i, 'total': total, 'status': message},
        )
        time.sleep(1)
    return {
        'current': 100,
        'total': 100,
        'status': 'Task completed!',
        'result': 42,
    }


@app.route('/', methods = ['GET'])
def hello():
    return jsonify('HALLO')


@app.route('/longtask', methods = ['GET'])
def longtask():
    task = long_task.apply_async()
    return jsonify({'task_id': task.id})


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...',
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', ''),
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
