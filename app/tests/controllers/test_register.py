from http import HTTPStatus
from app.models.users import Users
from flask_testing import TestCase
from app import app, db
from datetime import datetime, timedelta, timezone
import json


class UserRegisterTests(TestCase):

    def create_app(self):
        app.config.from_object('config.ConfigTest')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestRegisterUserApi(UserRegisterTests):
    def test_register_user_with_success(self):
        user_data = {
            'email': 'test@gmail.com',
            'password': 'Password123!'
        }

        with self.client as c:
            response = c.post(
                '/register', data=json.dumps(user_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.CREATED)
            self.assertEqual(
                response.json['message'], 'User registered successfully.')

    def test_register_user_with_existing_email(self):
        user = Users(email='test@gmail.com')
        user.set_password("Password123!")
        db.session.add(user)
        db.session.commit()

        user_data = {
            'email': 'test@gmail.com',
            'password': 'Password123!'
        }

        with self.client as c:
            response = c.post(
                '/register', data=json.dumps(user_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertEqual(
                response.json['message'], 'Email is already registered.')

    def test_register_user_with_invalid_email(self):
        user_data = {
            'email': 'test@example.com',
            'password': 'Password123!'
        }

        with self.client as c:
            response = c.post(
                '/register', data=json.dumps(user_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertIn('Invalid email address.', response.json['email'])

    def test_register_user_with_weak_password(self):
        user_data = {
            'email': 'test2@gmail.com',
            'password': 'weak'
        }

        with self.client as c:
            response = c.post(
                '/register', data=json.dumps(user_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertIn(
                'Password must be at least 10 characters long.', response.json['password'])

    def test_register_user_with_not_uppercase_password(self):
        user_data = {
            'email': 'test2@gmail.com',
            'password': 'zassword123s'
        }

        with self.client as c:
            response = c.post(
                '/register', data=json.dumps(user_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertIn(
                'Password must contain at least one uppercase letter.', response.json['password'])

    def test_register_user_with_not_lowercase_password(self):
        user_data = {
            'email': 'test2@gmail.com',
            'password': 'Z213721376123?!'
        }

        with self.client as c:
            response = c.post(
                '/register', data=json.dumps(user_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertIn(
                'Password must contain at least one lowercase letter.', response.json['password'])

    def test_register_user_with_not_special_character_password(self):
        user_data = {
            'email': 'test2@gmail.com',
            'password': 'Zfahsfga2j1OLdhshdGS'
        }

        with self.client as c:
            response = c.post(
                '/register', data=json.dumps(user_data), content_type='application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertIn(
                'Password must contain at least one special character: !, @, #, or ?', response.json['password'])
