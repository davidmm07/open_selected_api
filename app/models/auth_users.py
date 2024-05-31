#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from app import db

class AuthUser(db.Model):
    __tablename__ = 'auth_users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, token, expiration_time):
        self.user_id = user_id
        self.token = token
        self.expiration_time = expiration_time
