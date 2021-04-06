from .calculation import cal_step_by_one, cal_square, cal_minus_one
from flask import request, Flask
import json

app = Flask(__name__)

@app.route('/plus_one')
def plus_one():
    x = int(request.args.get("x",1))
    return json.dumps({'x':cal_step_by_one(x)})

@app.route('/square')
def square():
    x = int(request.args.get("x",1))
    return json.dumps({'x':cal_square(x)})

@app.route('/minus_one')
def minus_one():
    x = int(request.args.get("x",1))
    return json.dumps({'x':cal_minus_one(x)})
