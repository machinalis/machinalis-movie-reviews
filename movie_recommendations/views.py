"""
movie_recommendations views
"""

from flask import render_template
from flask_security import login_required

from movie_recommendations import app


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
