from flask import Flask
from flask import url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@ app.route('/home')
def home():
    return 'welcome to My Watchlist!'

@app.route('/user/<name>')
def user_page(name):
    return '{0}s page'.format(name)

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('home'))
    return 'Test page'