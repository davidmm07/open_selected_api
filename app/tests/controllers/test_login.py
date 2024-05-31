from http import HTTPStatus
from datetime import datetime, timedelta, timezone
from app import app, db
from flask_testing import TestCase
import jwt
import json

class UserLoginTests(TestCase):

    def create_app(self):
        app.config.from_object('config.ConfigTest')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestLoginUserApi(UserLoginTests):
    def test_login_user_with_success(self):
        # Register a user first
        user_data = {
            'email': 'test_login@gmail.com',
            'password': 'Password123!'
        }
        with self.client as c:
            response = c.post('/register', data=json.dumps(user_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.CREATED)

        # Now attempt login with valid credentials
        login_data = {
            'email': 'test_login@gmail.com',
            'password': 'Password123!'
        }
        with self.client as c:
            response = c.post('/login', data=json.dumps(login_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIn('token', response.json)

    def test_login_user_with_invalid_format(self):
        # Attempt login with invalid email
        login_data = {
            'email': 'invalidemail@example.com',
            'password': 'Password123!'
        }
        with self.client as c:
            response = c.post('/login', data=json.dumps(login_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(response.json['message'], 'Validation error')

        # Attempt login with incorrect format password
        login_data = {
            'email': 'test_login@gmail.com',
            'password': 'IncorrectPassword'
        }
        with self.client as c:
            response = c.post('/login', data=json.dumps(login_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(response.json['message'], 'Validation error')

    def test_login_user_with_invalid_credentials(self):

        # Attempt login with incorrect password
        login_data = {
            'email': 'test_login@gmail.com',
            'password': 'Password1233!'
        }
        with self.client as c:
            response = c.post('/login', data=json.dumps(login_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
            self.assertEqual(response.json['message'], 'Invalid credentials')

    def test_login_user_token_expiration(self):
        # Your existing login logic here
        user_data = {
            'email': 'test_login_token@gmail.com',
            'password': 'Password123@'
        }
        with self.client as c:
            response = c.post('/register', data=json.dumps(user_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.CREATED)

        user_data = {
            'email': 'test_login_token@gmail.com',
            'password': 'Password123@'
        }
        with self.client as c:
            response = c.post('/login', data=json.dumps(user_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.OK)
            # Check if token is returned in response
            self.assertIn('token', response.json)

            # Decode and verify token
            token = response.json['token']
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            self.assertIn('user_id', decoded_token)

            # Check if token expires after 20 minutes
            expiration_time = datetime.fromtimestamp(decoded_token['exp'], timezone.utc)
            self.assertTrue(expiration_time - datetime.now(timezone.utc) < timedelta(minutes=20))

