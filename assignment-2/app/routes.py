from flask import jsonify
from app import app, db
from app.models import User

@app.route('/')
def test_users():
    users = User.query.all()
    return jsonify(users)

