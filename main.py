from flask import Flask, jsonify
from extensions import db, jwt
from auth import auth_bp
from users import user_bp


def create_app():

    app = Flask(__name__)

    app.config.from_prefixed_env()

    db.init_app(app)
    jwt.init_app(app)
    # register auth bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")

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
