from flask import Flask, request
from werkzeug import secure_filename
import os
import pydoop.hdfs as hdfs
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()

print(hdfs.hdfs().list_directory('/user'))


@app.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!'


@app.route('/test', methods = ['POST'])
def test():
    f = request.files['file']
    f.save(
        os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
    )
    return f.filename


@app.route('/wordcount', methods = ['POST'])
def wordcount():
    f = request.files['file']
    f.save(
        os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
    )
    with open(f.filename, 'r') as fopen:
        hdfs.dump(fopen.read(), '/user/input_wordcount/text')
    os.system(
        'pydoop script -c combiner wordcount.py /user/input_wordcount /user/output_wordcount'
    )
    list_files = hdfs.hdfs().list_directory('/user/output_wordcount')
    return json.dumps(
        [
            hdfs.load(file['name'], mode = 'rt')
            for file in list_files
            if 'SUCCESS' not in file['name']
        ]
    )


@app.route('/lowercase', methods = ['POST'])
def lowercase():
    f = request.files['file']
    f.save(
        os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
    )
    with open(f.filename, 'r') as fopen:
        hdfs.dump(fopen.read(), '/user/input_lowercase/text')
    os.system(
        "pydoop script --num-reducers 0 -t '' lowercase.py /user/input_lowercase /user/output_lowercase"
    )
    list_files = hdfs.hdfs().list_directory('/user/output_lowercase')
    return json.dumps(
        [
            hdfs.load(file['name'], mode = 'rt')
            for file in list_files
            if 'SUCCESS' not in file['name']
        ]
    )


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
