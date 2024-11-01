from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/login')
def login():
    pass


if __name__ == '__main__':
    app.run()
