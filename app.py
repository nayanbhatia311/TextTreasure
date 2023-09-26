from flask import Flask, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv

from extensions import db, jwt
from auth import auth_bp
from users import user_bp
from home import home_bp


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    db.init_app(app)
    jwt.init_app(app)
    # register auth bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(home_bp, url_prefix="/")

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
            "error": "invalid_token"
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "message": "Token i nvalid",
            "error": "authorized_error"
        }), 401

    return app


if __name__ == '__main__':
    create_app().run(debug=True, port=5001)
