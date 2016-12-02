"""
movie_recommendations app module
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_marshmallow import Marshmallow

# Flask app set-up

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)

import movie_recommendations.models

# Flask-Security set-up
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

import movie_recommendations.cli
import movie_recommendations.factories
import movie_recommendations.views
