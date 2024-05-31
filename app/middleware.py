from flask import request, g, jsonify
from app.models.audit_log import AuditLog
from app import db
import json
from datetime import datetime
from app.utils.token import decode_token

class AuditMiddleware:
    def __init__(self, app):
        self.app = app
        app.before_request(self.log_request)
        app.after_request(self.log_response)

    def valid_audit_path(self):
        return False if request.path == "/register" or request.path == "/login" else True
    def log_request(self):
        user_id = None
        token = request.headers.get('Authorization')
        if token:
            user_id = decode_token(token)
        g.audit_data = {
            'timestamp': datetime.utcnow(),
            'user_id': user_id,
            'request_method': request.method,
            'request_path': request.path,
            'request_headers': json.dumps(dict(request.headers)),
            'request_body': request.get_data(as_text=True) if self.valid_audit_path() else request.get_json()['email'],
            'response_status': None,
            'response_body': None
        }

    def log_response(self, response):
        audit_data = g.audit_data
        audit_data['response_status'] = response.status_code
        audit_data['response_body'] = response.get_data(as_text=True)

        audit_log = AuditLog(**audit_data)
        db.session.add(audit_log)
        db.session.commit()

        return response
