from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!'


@app.route('/members')
def members():
    return 'you can put anything after /members/'


@app.route('/members/<string:name>/')
def getMember(name):
    return name


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
