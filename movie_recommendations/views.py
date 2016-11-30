"""
movie_recommendations views
"""

from flask import render_template

from movie_recommendations import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')
