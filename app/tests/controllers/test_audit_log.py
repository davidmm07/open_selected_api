import unittest
from flask_testing import TestCase
from app import app, db
from app.models.audit_log import AuditLog
from app.models.users import Users
from app.utils.token import generate_jwt_token

class AuditLogTests(TestCase):

    def create_app(self):
        app.config.from_object('config.ConfigTest')
        return app

    def setUp(self):
        db.create_all()
        self.user = Users(email='test@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()
        self.token, _ = generate_jwt_token(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_audit_log_creation(self):
        with self.client as c:
            response = c.get('/movies', headers={'Authorization': self.token})
            self.assertEqual(response.status_code, 200)
            
            audit_log = AuditLog.query.order_by(AuditLog.id.desc()).first()
            self.assertIsNotNone(audit_log)
            self.assertEqual(audit_log.request_path, '/movies')
            self.assertEqual(audit_log.response_status, 200)
            self.assertEqual(audit_log.user_id, self.user.id)

