from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import settings

app = Flask("Разработ")
app.config['SQLALCHEMY_DATABASE_URI'] = settings.db_url
db = SQLAlchemy(app)