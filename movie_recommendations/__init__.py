"""
movie_recommendations app module
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore

# Flask app set-up

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import movie_recommendations.models

# Flask-Security set-up
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

import movie_recommendations.cli
import movie_recommendations.factories
import movie_recommendations.views
