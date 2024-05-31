#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import ENV
from flask_migrate import Migrate

# create app
app = Flask(__name__)

app.config.from_object(f'config.Config{ENV}')

# create db connection
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from app.views.users import user_bp
from app.views.movies import movie_bp

# register blueprints
app.register_blueprint(user_bp, url_prefix='/')
app.register_blueprint(movie_bp, url_prefix='/movies')

from app.middleware import AuditMiddleware
AuditMiddleware(app)