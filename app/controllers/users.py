from app.utils.token import generate_jwt_token
from flask import jsonify
from app import db
from app.schemas.users import UserSchema
from app.models.users import Users
from app.models.auth_users import AuthUser
from marshmallow import ValidationError
import os


def register_user(data):
    try:
        user_schema = UserSchema()

        try:
            validated_data = user_schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        print(os.environ.get('DATABASE_URL'))
        email = validated_data['email']
        password = validated_data['password']
        if Users.query.filter_by(email=email).first():
            return jsonify({"message": "Email is already registered."}), 400
        new_user = Users(email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully."}), 201
    
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


def login_user(data):
    # Get request dat

    # Validate request data
    errors = UserSchema().validate(data)
    if errors:
        return jsonify({'message': 'Validation error', 'errors': errors}), 400

    # Check if user exists
    user = Users.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    # Check if password is correct
    if not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Generate authentication token (you can use JWT for this)
    token, expiration_time = generate_jwt_token(user)
    auth_user = AuthUser(user_id=user.id, token=token, expiration_time=expiration_time)
    db.session.add(auth_user)
    # Store token expiration time
    #user.token_expiration = token_expiration
    db.session.commit()

    return jsonify({'message': 'Login successful', 'token': token}), 200

