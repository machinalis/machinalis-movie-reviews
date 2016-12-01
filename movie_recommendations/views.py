"""
movie_recommendations views
"""

from flask import render_template, jsonify, abort
from flask_security import login_required, current_user

from movie_recommendations import app, db
from movie_recommendations.models import Movie


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/like/<int:movie_id>', methods=['POST'])
@login_required
def like(movie_id):
    """Updates the "like" status of a movie for a given user."""
    app.logger.debug('like. movie_id = %s', movie_id)

    movie = Movie.query.get(movie_id)

    app.logger.debug('movie = %s', movie)

    if not movie:
        app.logger.debug('Movie not found. movie_id = %s', movie_id)
        abort(404)

    if current_user in movie.likes:
        movie.likes.append(current_user)
        db.session.merge(movie)
        db.session.commit()

    return jsonify({'movie_id': movie_id, 'likes': len(movie.likes)})
