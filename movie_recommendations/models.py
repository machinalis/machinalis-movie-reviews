"""
movie_recommendations models
"""

from movie_recommendations import db


# A table to track follows
follows = db.Table('follows',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), index=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
    db.UniqueConstraint('user_id', 'followed_id', name='unique_follows')
)


class User(db.Model):
    """A user of the movie_recommendations site"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    follows = db.relationship('User', secondary=follows, primaryjoin=id == follows.c.user_id,
                              secondaryjoin=id == follows.c.followed_id,
                              backref=db.backref('followers', lazy='dynamic'))

    def __init__(self, username, email, password=None):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User(id={id}, username={username}, email={email}>)'.format(id=self.id,
                                                                            username=self.username,
                                                                            email=self.email)


# A table to track movie likes
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), index=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), index=True),
    db.UniqueConstraint('user_id', 'movie_id', name='unique_likes')
)


class Movie(db.Model):
    """An IMDB listed movie"""
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.SmallInteger)
    director_name = db.Column(db.String(255))
    actor_1_name = db.Column(db.String(255))
    actor_2_name = db.Column(db.String(255))
    actor_3_name = db.Column(db.String(255))
    genres = db.Column(db.String(255))
    movie_imdb_link = db.Column(db.String(255))
    language = db.Column(db.String(63))
    country = db.Column(db.String(63))
    content_rating = db.Column(db.String(15))
    title_year = db.Column(db.String(4))
    imdb_score = db.Column(db.Float)
    movie_facebook_likes = db.Column(db.BigInteger)
    likes = db.relationship('User', secondary=likes, backref=db.backref('likes', lazy='dynamic'))

    def __init__(self, movie_title, duration=None, director_name=None, actor_1_name=None,
                 actor_2_name=None, actor_3_name=None, genres=None, movie_imdb_link=None,
                 language=None, country=None, content_rating=None, title_year=None,
                 imdb_score=None, movie_facebook_likes=None):
        self.movie_title = movie_title
        self.duration = duration
        self.director_name = director_name
        self.actor_1_name = actor_1_name
        self.actor_2_name = actor_2_name
        self.actor_3_name = actor_3_name
        self.genres = genres
        self.movie_imdb_link = movie_imdb_link
        self.language = language
        self.country = country
        self.content_rating = content_rating
        self.title_year = title_year
        self.imdb_score = imdb_score
        self.movie_facebook_likes = movie_facebook_likes

    def __repr__(self):
        return ('<Movie('
                'id={id}, '
                'movie_title={movie_title}, '
                'duration={duration}, '
                'director_name={director_name}, '
                'actor_1_name={actor_1_name}, '
                'actor_2_name={actor_2_name}, '
                'actor_3_name={actor_3_name}, '
                'genres={genres}, '
                'movie_imdb_link={movie_imdb_link}, '
                'language={language}, '
                'country={country}, '
                'title_year={title_year}, '
                'imdb_score={imdb_score}, '
                'movie_facebook_likes={movie_facebook_likes}'
                ')>').format(id=self.id, movie_title=self.movie_title, duration=self.duration,
                             director_name=self.director_name, actor_1_name=self.actor_1_name,
                             actor_2_name=self.actor_2_name, actor_3_name=self.actor_3_name,
                             genres=self.genres, movie_imdb_link=self.movie_imdb_link,
                             language=self.language, country=self.country,
                             title_year=self.title_year, imdb_score=self.imdb_score,
                             movie_facebook_likes=self.movie_facebook_likes)
