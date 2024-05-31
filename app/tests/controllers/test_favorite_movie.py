from flask_testing import TestCase
from http import HTTPStatus
from app import app, db
from app.models.users import Users
from app.models.movies import FavoriteMovie
from app.utils.token import generate_jwt_token

class FavoriteMovieControllerTests(TestCase):

    def create_app(self):
        app.config.from_object('config.ConfigTest')
        return app

    def setUp(self):
        db.create_all()
        self.user = Users(email='test_fav_movie@gmail.com')
        self.user.set_password('PasswordTestFav123!')
        db.session.add(self.user)
        db.session.commit()
        self.token , _ = generate_jwt_token(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_favorite_movie_with_success(self):
        with self.client as c:
            response = c.post('/movies/favorite', 
                              headers={'Authorization': self.token},
                              json={'movie_id': 1})
            self.assertEqual(response.status_code, HTTPStatus.CREATED)
            self.assertEqual(response.json['message'], 'Movie added to favorites')

    def test_add_favorite_movie_without_movie_id(self):
        with self.client as c:
            response = c.post('/movies/favorite', 
                              headers={'Authorization': self.token},
                              json={})
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(response.json['message'], 'Movie ID is required')

    def test_add_favorite_movie_already_favorited(self):
        favorite_movie = FavoriteMovie(user_id=self.user.id, movie_id=1)
        db.session.add(favorite_movie)
        db.session.commit()

        with self.client as c:
            response = c.post('/movies/favorite', 
                              headers={'Authorization': self.token},
                              json={'movie_id': 1})
            self.assertEqual(response.status_code, HTTPStatus.CONFLICT)
            self.assertEqual(response.json['message'], 'Movie is already in favorites')