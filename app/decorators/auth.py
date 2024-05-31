from functools import wraps
from flask import request, jsonify
from app.utils.token import decode_token
from http import HTTPStatus

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return jsonify({"message": "Token is missing."}), HTTPStatus.UNAUTHORIZED
        user_id = decode_token(token)
        if user_id is None:
            return jsonify({"message": "Token is invalid or expired."}), HTTPStatus.UNAUTHORIZED
        return f(user_id, *args, **kwargs)
    return decorated_function