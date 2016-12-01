"""
movie_recommendations views
"""

from flask import render_template, jsonify
from flask_security import login_required, current_user

from movie_recommendations import app, db
from movie_recommendations.models import Movie, User, movies_schema
from movie_recommendations.recommendation_engines import get_recommendations


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
