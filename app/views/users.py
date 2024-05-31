from flask import Blueprint, request
import app.controllers.users as users_controller

user_bp = Blueprint('users', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    return users_controller.register_user(data)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return users_controller.login_user(data)