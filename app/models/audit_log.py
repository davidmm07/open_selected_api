#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from app import db
from datetime import datetime, timezone

class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, nullable=True)
    request_method = db.Column(db.String(10))
    request_path = db.Column(db.String(255))
    request_headers = db.Column(db.Text)
    request_body = db.Column(db.Text)
    response_status = db.Column(db.Integer)
    response_body = db.Column(db.Text)

    def __repr__(self):
        return f'<AuditLog {self.id}>'
