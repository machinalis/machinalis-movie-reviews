"""
movie_recommendations views
"""

import requests

from flask import render_template, jsonify, redirect, url_for
from flask_security import login_required, current_user

from movie_recommendations import app, db
from movie_recommendations.models import Movie, User, movies_schema
from movie_recommendations.recommendation_engines import get_recommendations


@app.route('/')
@login_required
def index():
    limit = app.config.get('RECOMMENDATIONS_LIMIT', 6)
    context = {
        "recommendations": get_recommendations(current_user, limit),
        "likes": list(current_user.likes),
        "most_viewed": Movie.query.order_by('imdb_score DESC').limit(limit)
    }
    return render_template('index.html', **context)


@app.route('/profile')
@app.route('/profile/<string:username>')
@login_required
def profile(username=None):
    user = User.query.filter(User.username == username).first() or current_user
    is_self_profile = user.id == current_user.id
    is_following = False
    if not is_self_profile:
        is_following = user.id in [x.id for x in current_user.follows]

    context = {
        "user": user,
        "is_self_profile": is_self_profile,
        "is_following": is_following
    }
    return render_template('profile.html', **context)


@app.route('/like/<int:movie_id>', methods=['POST'])
@login_required
def like(movie_id):
    """Updates the "like" status of a movie for a given user."""
    app.logger.debug('like. movie_id = %s', movie_id)

    movie = Movie.query.get(movie_id)

    app.logger.debug('movie = %s', movie)

    if not movie:
        app.logger.debug('Movie not found. movie_id = %s', movie_id)
        return jsonify({'error': 'Movie not found: {}'.format(movie_id)}), 404

    if current_user in movie.likes:
        movie.likes.remove(current_user)
    else:
        movie.likes.append(current_user)

    db.session.merge(movie)
    db.session.commit()

    return jsonify({'movie_id': movie_id, 'likes': len(movie.likes)})


@app.route('/follow/<int:followed_id>', methods=['POST'])
@login_required
def follow(followed_id):
    """Updates the "follow" status of a user for a given user."""
    app.logger.debug('follow. followed_id = %s', followed_id)

    if followed_id == current_user.id:
        return jsonify({'error': 'Cannot follow self'}), 400

    followed = User.query.get(followed_id)

    app.logger.debug('followed = %s', followed)

    if not followed:
        app.logger.debug('User not found. followed = %s', followed)
        return jsonify({'error': 'User not found: {}'.format(followed_id)}), 404

    if followed in current_user.follows:
        current_user.follows.remove(followed)
    else:
        current_user.follows.append(followed)

    db.session.merge(current_user)
    db.session.commit()

    return jsonify(
        {'user_id': current_user.id, 'followed_id': followed_id,
         'follows': len(current_user.follows)})


@app.route('/recommendations')
@login_required
def recommendations():
    """Returns a list of movie recommendations for the logged-in user."""
    app.logger.debug('recommendations')

    recommendations = get_recommendations(current_user, app.config.get('RECOMMENDATIONS_LIMIT', 5))
    recommendations_json = movies_schema.dump(recommendations).data

    return jsonify(recommendations_json)


@app.route('/poster/<int:movie_id>')
def poster(movie_id):
    movie = Movie.query.get(movie_id)
    url = "http://www.omdbapi.com/?t={}&y=&plot=short&r=json".format(movie.movie_title)
    data = requests.get(url).json()
    return redirect(data.get("Poster", url_for("static", filename="imgs/default_poster.png")))
