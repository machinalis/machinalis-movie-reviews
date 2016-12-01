import sys

from sqlalchemy import or_
from sqlalchemy.sql.expression import func


from movie_recommendations import app, db, models


def random_choice(user):
    """Picks a random set of movies"""
    return models.Movie.query.order_by(func.random())


def facebook_recommendations(user):
    """Picks movies based on Facebook likes"""
    return models.Movie.query.order_by(models.Movie.movie_facebook_likes)


def recommend_by_likes(user):
    """Picks movies based on how many likes it has"""
    return db.session.query(models.Movie, func.count(models.likes.c.user_id).label('total_likes'))\
        .join(models.likes).group_by(models.Movie).order_by('total_likes DESC')


def recommend_by_follows(user):
    """Picks movies based on the movies liked by users followed by the current user"""
    return db.session.query(models.Movie).join(models.likes).join(models.User)\
        .filter(models.likes.c.user_id == models.User.id)\
        .join(models.follows, models.follows.c.followed_id == models.likes.c.user_id)\
        .filter(models.follows.c.user_id == user.id)\
        .filter(models.likes.c.user_id != user.id)


def recommend_by_imdb_score(user):
    """Recommends movies based on their IMDB score"""
    return models.Movie.query.order_by('imdb_score DESC')


def only_the_best(user):
    """All Robert De Niro, All the time"""
    return models.Movie.query.filter(or_(
        models.Movie.actor_1_name.like('%De Niro'), models.Movie.actor_2_name.like('%De Niro'),
        models.Movie.actor_3_name.like('%De Niro'))).order_by(func.random())


def get_recommendations(user, limit=10):
    """
    Entry point for the recommendations engine. It returns a list of movies based on the
    recommendation engine defined by the RECOMMENDATIONS_ENGINE config key.
    """
    recommendations_engine = getattr(sys.modules[__name__],
                                     app.config['RECOMMENDATIONS_ENGINE'], only_the_best)
    return recommendations_engine(user).limit(limit)
