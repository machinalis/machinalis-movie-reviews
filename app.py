from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

import settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')
