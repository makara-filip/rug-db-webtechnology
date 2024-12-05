import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app import db
from app.models import User
from app.api.errors import error_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = User.get_user_by_username(username)
    if user and user.check_password(password):
        return user
    return None

@token_auth.verify_token
def verify_token(token):
    if token:
        user = User.get_user_by_token(token)
        return user
    return None

@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)