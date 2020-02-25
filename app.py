from flask import Flask, render_template
from flask import url_for
import os
import sys
import click
from flask import request, redirect, flash

from flask_sqlalchemy import SQLAlchemy
WIN = sys.platform.startswith('win')

if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

name = 'secret'

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid inout.')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    user = User.query.first()
    movies = Movie.query.all()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit',movie_id=movie_id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item update')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>',	methods=['POST'])# 限定只接受POST请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)# 获取电影记录
    db.session.delete(movie)		# 删除对应的记录
    db.session.commit()		# 提交数据库会话
    flash('Item	deleted.')
    return redirect(url_for('index'))

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

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    db.drop_all()
    db.create_all()

    name='secret'
    movies = [{'title': 'My Neighbor Totoro', 'year': '1988'},
              {'title': 'Dead Poets	Society', 'year': '1989'},
              {'title': 'A Perfect World', 'year': '1993'},
              {'title': 'Leon', 'year': '1994'},
              {'title': 'Mahjong', 'year': '1996'},
              {'title': 'Swallowtail Butterfly', 'year': '1996'},
              {'title': 'King of Comedy', 'year': '1999'},
              {'title': 'Devils	on the Doorstep', 'year': '1999'},
              {'title': 'WALL-E', 'year': '2008'},
              {'title': 'The Pork of Music', 'year': '2012'}, ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie=Movie(title=m['title'],year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)