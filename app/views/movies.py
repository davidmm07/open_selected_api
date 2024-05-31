from app.decorators.auth import token_required
from flask import Blueprint, request
import app.controllers.movies as movies_controller
#from flask_jwt_extended import jwt_required, get_jwt_identity

movie_bp = Blueprint('movies', __name__)

@movie_bp.route('', methods=['GET'])
@token_required
def get(user_id):
    page = request.args.get('page', 1, type=int)
    return movies_controller.get_movies(user_id, page)


@movie_bp.route('/favorite', methods=['POST'])
@token_required
def add_favorite_movie(user_id):
    data = request.get_json()
    return movies_controller.add_favorite_movie(user_id, data)