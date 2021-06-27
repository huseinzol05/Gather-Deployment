from flask import Flask, request
import pymysql
import json
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

required = ['username', 'first_name', 'last_name', 'password']
connection = pymysql.connect(
    host = 'localhost', user = 'root', password = 'husein', db = 'testdb'
)
cursor = connection.cursor()


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message = "Todo {} doesn't exist".format(todo_id))


class Mysql(Resource):
    def get(self):
        sql = 'SELECT * FROM user_details WHERE username=%s'
        cursor.execute(sql, (request.form['username']))
        result = cursor.fetchone()
        return json.dumps(result)

    def put(self):
        to_dict = request.form.to_dict()
        keys = ['`%s`' % (i) for i in to_dict.keys()]
        if sum([i in required for i in to_dict.keys()]) != len(required):
            return 'not enough parameters'
        sql = (
            'INSERT INTO user_details ('
            + ','.join(keys)
            + ') VALUES ('
            + ','.join(['%s'] * len(keys))
            + ')'
        )
        cursor.execute(sql, tuple([to_dict[i] for i in to_dict.keys()]))
        connection.commit()
        return 'success ' + json.dumps(to_dict)


api.add_resource(Mysql, '/')

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
