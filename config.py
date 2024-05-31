#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ENV = 'run' to run the app or 'test' to run the tests
ENV = os.getenv('FLASK_ENV', 'Dev')


class ConfigStg:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}
    SECRET_KEY = 'SuperSecretKey' #TODO Change for ENV
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    TMDB_API_KEY = "056b9fd1ab560e7b9e19491008a49c42"

class ConfigDev:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}
    SECRET_KEY = 'SuperSecretKey' #TODO Change for ENV
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    TMDB_API_KEY = "056b9fd1ab560e7b9e19491008a49c42"

class ConfigTest:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SECRET_KEY = 'SuperSecretKey' #TODO Change for ENV
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    TMDB_API_KEY = "056b9fd1ab560e7b9e19491008a49c42"