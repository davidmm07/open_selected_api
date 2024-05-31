from http import HTTPStatus
from app.utils.token import generate_jwt_token
from flask_testing import TestCase
from app import app, db
from app.models.users import Users
from app.models.movies import FavoriteMovie

class MovieControllerTests(TestCase):

    def create_app(self):
        app.config.from_object('config.ConfigTest')
        return app

    def setUp(self):
        db.create_all()
        self.user = Users(email='test@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()
        self.token , _ = generate_jwt_token(self.user)
        self.movie_id = 823464
        self.favorite_movie = FavoriteMovie(user_id=self.user.id, movie_id=self.movie_id)
        db.session.add(self.favorite_movie)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_movies_with_favorite_flag(self):

        with self.client as c:
            response = c.get("/movies?page=1", headers={'Authorization': self.token})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = response.json
            self.assertIn('results', data)
            for movie in data['results']:
                if movie['id'] == self.movie_id :
                    self.assertTrue(movie['favorite'])
                else:
                    self.assertFalse(movie.get('favorite', False))