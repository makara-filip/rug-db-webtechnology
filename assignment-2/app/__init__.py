import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
database_absolute_file_path = os.path.join(basedir, 'database.db')
print("Database file:", database_absolute_file_path)

app = Flask(__name__)
login_manager = LoginManager(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_absolute_file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SECRET_KEY"] = "qwerty"

db = SQLAlchemy(app)

from app import models, routes

# Create the database and the tables
with app.app_context():
    db.create_all()
