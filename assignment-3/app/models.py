import datetime
import secrets

from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_login import UserMixin
import sqlalchemy as sa

from app import db, login_manager

class PaginatedApiMixin(object):
    @staticmethod
    def to_collection_dictionary(query, page, page_size, endpoint, **kwargs):
        resources = db.paginate(query, page=page, per_page=page_size, error_out=False)
        
        data = {
            'data': [item.to_dictionary() for item in resources.items],
            'meta': {
                'page': page,
                'page_size': page_size,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            'links': {
                'self': url_for(endpoint, page=page,     page_size=page_size, **kwargs),
                'next': url_for(endpoint, page=page+1, page_size=page_size, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page-1, page_size=page_size, **kwargs) if resources.has_prev else None
            }
        }
        return data


class Movie(PaginatedApiMixin, db.Model):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    awards = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String, nullable=True)

    def to_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "year": self.year,
            "awards": self.awards
        }
    
    @staticmethod
    def get_direct_fields():
        return ["name", "year", "awards"]
    @staticmethod
    def get_required_fields():
        return ["name", "year", "awards"]
    @staticmethod
    def get_editable_fields():
        return ["name", "year", "awards"]

    
    def from_dict(self, data):
        for field in self.get_direct_fields():
            if field in data:
                setattr(self, field, data[field])

class User(PaginatedApiMixin, UserMixin, db.Model):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    auth_token = db.Column(db.String(32), nullable=True, unique=True)
    auth_token_expiration = db.Column(db.DateTime, nullable=True)
    
    # password- and auth-related methods:
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_auth_token(self):
        now = datetime.datetime.now()
        if self.auth_token and self.auth_token_expiration > now + datetime.timedelta(minutes=1):
            # there is at least 1 minute of token validity
            return self.auth_token
        
        TOKEN_VALIDITY_TIME_SPAN = datetime.timedelta(hours=24)
        self.auth_token = secrets.token_hex(16)
        self.auth_token_expiration = now + TOKEN_VALIDITY_TIME_SPAN
        db.session.add(self)
        return self.auth_token

    def revoke_auth_token(self):
        now = datetime.datetime.now()
        self.auth_token_expiration = now - datetime.timedelta(hours=1)
        db.session.add(self)

    # api-related methods:
    def to_dictionary(self):
        data = {
            "id": self.id,
            "username": self.username,
        }
        return data
    
    @staticmethod
    def get_direct_fields():
        return ["username"]
    @staticmethod
    def get_editable_fields():
        return ["username"]

    def from_dict(self, data, creating_new_user=False):
        for field in self.get_direct_fields():
            if field in data:
                setattr(self, field, data[field])
        if creating_new_user:
            if "password" in data: 
                self.set_password(data["password"])

    @staticmethod
    def get_user_by_username(username):
        return db.session.scalar(sa.select(User).where(User.username == username))
    
    @staticmethod
    def get_user_by_token(token):
        user = db.session.scalar(sa.select(User).where(User.auth_token == token))
        if user is None: return None
        if user.auth_token_expiration < datetime.datetime.now(): return None
        return user


@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))
