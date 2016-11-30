"""
movie_recommendations app module
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

import movie_recommendations.cli
import movie_recommendations.factories
import movie_recommendations.models
import movie_recommendations.views
