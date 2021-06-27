from flask import Flask, request
import os
import json
from pyhive import hive

cursor = hive.connect('localhost').cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS employee ( eid int, name String, salary String, destignation String) COMMENT 'employee details' ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' STORED AS TEXTFILE"
)
cursor.execute(
    "LOAD DATA LOCAL INPATH 'sample.txt' OVERWRITE INTO TABLE employee"
)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!'


@app.route('/employee/<string:person>/')
def get(person):
    cursor.execute("SELECT * FROM employee WHERE name = '%s'" % (person))
    return json.dumps(list(cursor.fetchall()))


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
