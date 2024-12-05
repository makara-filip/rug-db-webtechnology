import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
database_absolute_file_path = os.path.join(basedir, 'database.db')
print("Database file:", database_absolute_file_path)

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_absolute_file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SECRET_KEY"] = "qwerty"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import models, routes, api

app.register_blueprint(api.api_blueprint, url_prefix='/api')

# Create the database and the tables
with app.app_context():
    db.create_all()
