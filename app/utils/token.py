import jwt
import datetime
from datetime import datetime, timedelta, timezone
from flask import current_app

def generate_jwt_token(user):
    # Set token expiration time to 20 minutes from now
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=20)
    payload = {'user_id': user.id, 'exp': expiration_time,'user_email':user.email}
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token , expiration_time


def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
