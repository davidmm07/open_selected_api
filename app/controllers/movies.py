from flask import jsonify
import httpx
from app import app ,db
from app.models.movies import FavoriteMovie
import asyncio
from http import HTTPStatus

async def fetch_movies(page):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{app.config['TMDB_BASE_URL']}/movie/popular",
                params={
                    'api_key': app.config['TMDB_API_KEY'],
                    'language': 'en-US',
                    'page': page
                }
            )
            response.raise_for_status()
            return response.json(), HTTPStatus.OK
    except httpx.HTTPStatusError as e:
        if e.response.status_code == HTTPStatus.NOT_FOUND:
            return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
        elif e.response.status_code == HTTPStatus.UNAUTHORIZED:
            return {"error": "Unauthorized access"}, HTTPStatus.UNAUTHORIZED
        else:
            return {"error": "An error occurred while fetching data from TMDb"}, e.response.status_code
    except httpx.RequestError as e:
        return {"error": "Request error occurred"}, HTTPStatus.BAD_REQUEST


def get_movies(user_id,page):
    data, status = asyncio.run(fetch_movies(page))
    favorite_movie_ids = {fav.movie_id for fav in FavoriteMovie.query.filter_by(user_id=user_id).all()}
    for movie in data['results']:
        movie['favorite'] = movie['id'] in favorite_movie_ids
    return jsonify(data), status





def add_favorite_movie(user_id, data):
    movie_id = data.get('movie_id')
    if not movie_id:
        return jsonify({"message": "Movie ID is required"}), HTTPStatus.BAD_REQUEST

    # Check if the movie is already favorited
    if FavoriteMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first():
        return jsonify({"message": "Movie is already in favorites"}), HTTPStatus.CONFLICT

    favorite_movie = FavoriteMovie(user_id=user_id, movie_id=movie_id)
    db.session.add(favorite_movie)
    db.session.commit()

    return jsonify({"message": "Movie added to favorites"}), HTTPStatus.CREATED
