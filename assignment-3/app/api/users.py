from flask import request, url_for, redirect

from app.api import api_blueprint
from app.api.errors import not_found_response, bad_request
from app.api.utils import get_pagination_data
from app.api.auth import token_auth
from app.models import User
from app import db

@api_blueprint.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    user: User | None = User.query.get(id)
    if not user:
        return not_found_response("User with specified ID not found.")
    return user.to_dictionary()

@api_blueprint.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page_index, page_size = get_pagination_data()
    return User.to_collection_dictionary(User.query, page_index, page_size, 'api.get_users')

@api_blueprint.route('/users', methods=['POST'])
def create_user():
    # semantically equivalent to user registration

    data = request.get_json()
    if not ("username" in data and "password" in data and "password2" in data):
        return bad_request("Data must include username, password and password2 fields.")

    username = data["username"]
    password = data["password"]
    password2 = data["password2"]
    
    if not (username and password and password2):
        return bad_request("Data must include username, password and password2 fields.")
    if password != password:
        return bad_request("Passwords must match.")
    if User.get_user_by_username(username) != None:
        return bad_request("Username already taken.")
    
    user = User()
    user.from_dict(data, creating_new_user=True)
    db.session.add(user)
    db.session.commit()
    
    return user.to_dictionary(), 201, {"Location": url_for("api.get_user", id=user.id) }


@api_blueprint.route('/users', methods=['PUT'])
@token_auth.login_required
def update_user():
    # a user can modify only their data, not edit other users
    user: User = token_auth.current_user()
    if user is None: return not_found_response()
    data = request.get_json()

    for key in data.keys():
        if key not in User.get_editable_fields():
            return bad_request(f"Field ${key} cannot be edited!")
        
    user.from_dict(data)
    db.session.add(user)
    db.session.commit()
    return user.to_dictionary(), 204, {"Location": url_for("api.get_user", id=user.id) }

