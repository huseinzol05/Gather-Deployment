from celery import Celery
from flask import Flask, request
from werkzeug import secure_filename
import numpy as np
import subprocess
import shlex
import json
import os
import logging
import sys
import random
import time

logging.basicConfig(level = logging.DEBUG)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/upload'
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
celery = Celery(app.name, broker = app.config['CELERY_BROKER_URL'])
dfs_location = '/user/input_text'
output_dfs_location = '/user/output_classification'
celery.conf.update(app.config)


@celery.task(bind = True)
def classify_text(self):
    script = (
        '/opt/hadoop/bin/hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.1.jar -file classification.py -file dictionary-test.json -file frozen_model.pb -mapper classification.py -file reducer.py -reducer reducer.py -input %s/* -output %s'
        % (dfs_location, output_dfs_location)
    )
    subprocess.Popen(shlex.split(script), stdout = subprocess.PIPE)
    subprocess.Popen(
        shlex.split(
            '/opt/hadoop/bin/hadoop fs -get /user/output_classification'
        ),
        stdout = subprocess.PIPE,
    )
    self.update_state(
        state = 'PROGRESS', meta = {'status': 'uploaded to local'}
    )
    return {'status': 'classification completed!', 'result': 42}


@celery.task(bind = True)
def upload_files_dfs(self, file_location, split_size):
    with open(file_location) as fopen:
        texts = list(filter(None, fopen.read().split('\n')))
    splitted_list = np.array_split(texts, split_size)
    for no, split in enumerate(splitted_list):
        filename = '%d-%s' % (no, file_location)
        joined = '\n'.join(split.tolist())
        script = '/opt/hadoop/bin/hdfs dfs -put %s %s/%s' % (
            filename,
            dfs_location,
            filename,
        )
        print('%d: uploading %s/%s' % (no, dfs_location, filename))
        print('%d: %s' % (no, script))
        with open(filename, 'w') as fopen:
            fopen.write(joined)
        process = subprocess.Popen(
            shlex.split(script), stdout = subprocess.PIPE
        )
        self.update_state(
            state = 'PROGRESS',
            meta = {'status': 'uploaded %s/%s' % (dfs_location, filename)},
        )
    return {'status': 'upload completed!', 'result': 42}


@app.route('/upload', methods = ['POST'])
def upload():
    f = request.files['file']
    f.save(
        os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
    )
    split_size = int(request.form['split_size'])
    task = upload_files_dfs.apply_async([f.filename, split_size])
    return json.dumps({'id': task.id, 'filename': f.filename})


@app.route('/process', methods = ['GET'])
def process():
    task = classify_text.apply_async()
    return json.dumps({'id': task.id})


@app.route('/upload_status/<task_id>')
def upload_status(task_id):
    task = upload_files_dfs.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'status': task.info.get('status', '')}
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return json.dumps(response)


@app.route('/classify_text_status/<task_id>')
def classify_text_status(task_id):
    task = classify_text.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'status': task.info.get('status', '')}
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return json.dumps(response)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
