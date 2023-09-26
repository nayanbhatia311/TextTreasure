from flask import Blueprint, jsonify, request, render_template
from models import User, TokenBlockList
import models
from flask_jwt_extended import (create_access_token,
                                create_refresh_token, jwt_required,
                                get_jwt, current_user, get_jwt_identity)

auth_bp = Blueprint('auth', __name__)


@auth_bp.get('/register')
def register():
    return render_template('signup.html')


@auth_bp.post('/register')
def register_user():
    data = request.get_json()

    user = User.get_user_by_username(username=data.get("username"))

    if user:
        return jsonify({"error": "User already exist"}), 403

    new_user = User(username=data.get("username"), email=data.get("email"))
    new_user.set_password(password=data.get('password'))
    new_user.save()
    return jsonify({"message": "User created"}), 201


@auth_bp.get('/login')
def display_login_page():

    return render_template('login.html')


@auth_bp.post('/login')
def login_user():
    data = request.get_json()
    user = User.get_user_by_username(username=data.get('username'))

    if user and (user.check_password(password=data.get('password'))):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)
        response = jsonify({"message": "Logged in"})
        response.set_cookie("access_token_cookie", access_token)
        response.set_cookie("refresh_token_cookie", refresh_token)
        models.is_logged = True
        return response, 200
    return jsonify({
        "error": "Invalid password"
    }
    ), 400


@auth_bp.get('/whoami')
@jwt_required()
def whoami():

    return jsonify({
        "user_details": {
            "username": current_user.username,
            "email": current_user.email
        },

    })


@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)

    return jsonify({
        "access_token": new_access_token
    })


@auth_bp.get('/logout')
# @jwt_required(verify_type=False)
def logout_user():
    # jwt = get_jwt()
    # jti = jwt['jti']
    # token_type = jwt['type']
    # token_b = TokenBlockList(jti=jti)
    # token_b.save()

    response = jsonify(
        {"message": f"logged out succesfully."})
    models.is_logged = False
    response.delete_cookie("access_token_cookie")
    response.delete_cookie("refresh_token_cookie")
    return response, 200
