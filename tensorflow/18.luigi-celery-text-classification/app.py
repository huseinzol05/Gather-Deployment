import os
from flask import Flask, jsonify, request
from werkzeug import secure_filename
from celery import Celery
import luigi
from function import Save_to_Elastic, classify_sentiment

app = Flask(__name__)
os.makedirs('upload', exist_ok = True)
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/upload'
celery = Celery(
    app.name, backend = 'rpc://', broker = 'amqp://guest:@localhost:5672//'
)
celery.conf.update(app.config)


@celery.task(bind = True)
def luigi_task(self, filename, topic):
    luigi.build(
        [Save_to_Elastic(filename = filename, summary = topic, index = topic)],
        scheduler_host = 'localhost',
        scheduler_port = 8082,
    )
    return {'status': 'Task scheluded!', 'result': 42}


@app.route('/', methods = ['GET'])
def hello():
    return jsonify('HALLO')


@app.route('/sentiment', methods = ['GET'])
def sentiment():
    return classify_sentiment(request.args.get('text'))


@app.route('/upload', methods = ['POST'])
def upload():
    f = request.files['file']
    path_file = os.path.join(
        app.config['UPLOAD_FOLDER'], secure_filename(f.filename)
    )
    f.save(path_file)
    topic = request.form['topic']
    task = luigi_task.apply_async([path_file, topic])
    return jsonify({'task_id': task.id})


@app.route('/upload_status/<task_id>')
def upload_status(task_id):
    task = luigi_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'status': task.info.get('status', '')}
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
