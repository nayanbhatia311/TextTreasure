from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv
from models import User, TokenBlockList
from extensions import db, jwt
from auth import auth_bp
from users import user_bp
from home import home_bp


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_prefixed_env()

    # secret for signing jwt
    app.config['JWT_SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")

    # check cookies for jwt token
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

    # set to true so cookies will only be sent by browser over https
    app.config["JWT_COOKIE_SECURE"] = False

    # prevent CSRF attacks
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["JWT_CSRF_IN_COOKIES"] = False
    app.config["JWT_CSRF_CHECK_FORM"] = True

    db.init_app(app)
    jwt.init_app(app)
    # register auth bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(home_bp, url_prefix="/")

    # load user

    @jwt.user_lookup_loader
    def user_loopup_callback(_jwt_headers, jwt_data,):
        username = jwt_data.get('sub')
        return User.query.filter_by(username=username).one_or_none()
    # jwt error handler

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({
            "message": "Token expired",
            "error": "token_expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "message": "signature invalid",
            "error": error

        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return render_template('login.html')

    @jwt.additional_claims_loader
    def make_addtional_claims(identity):
        if identity == "admin":
            return {"is_staff": True}
        return {"is_staff": False}

    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data['jti']
        token = db.session.query(TokenBlockList).filter(
            TokenBlockList.jti == jti).scalar()

        return token is not None

    return app


if __name__ == '__main__':
    create_app().run(debug=True, port=5001)
