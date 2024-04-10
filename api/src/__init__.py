from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "password"  # change

    from .userAPI import userAPI

    app.register_blueprint(userAPI, url_prefix="/foods")

    return app
