from flask import request, url_for

from app.api import api_blueprint
from app.api.errors import not_found_response, bad_request
from app.api.utils import get_pagination_data
from app.api.auth import token_auth
from app.models import Movie
from app import db

@api_blueprint.route('/movies/<int:id>', methods=['GET'])
@token_auth.login_required
def get_movie(id):
    movie: Movie | None = Movie.query.get(id)
    if movie is None: return not_found_response("Movie not found.")
    return movie.to_dictionary()

@api_blueprint.route('/movies', methods=['GET'])
@token_auth.login_required
def get_movies():
    page_index, page_size = get_pagination_data()
    return Movie.to_collection_dictionary(Movie.query, page_index, page_size, 'api.get_movies')

@api_blueprint.route('/movies', methods=['POST'])
@token_auth.login_required
def create_movie():
    data = request.get_json()
    for field_name in Movie.get_required_fields():
        if field_name not in data:
            return bad_request(f"Data must include field '${field_name}'.")

    movie = Movie()
    movie.from_dict(data)
    db.session.add(movie)
    db.session.commit()
    
    return movie.to_dictionary(), 201, {"Location": url_for("api.get_movie", id=movie.id) }


@api_blueprint.route('/movies/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_movie(id):
    movie: Movie | None = Movie.query.get(id)
    if movie is None: return not_found_response("Movie not found.")
    data = request.get_json()

    for key in data.keys():
        if key not in Movie.get_editable_fields():
            return bad_request(f"Field ${key} cannot be edited!")
        
    movie.from_dict(data)
    db.session.add(movie)
    db.session.commit()
    return movie.to_dictionary(), 204, {"Location": url_for("api.get_movie", id=movie.id) }

