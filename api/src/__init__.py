from flask import Flask

# from firebase_admin import credentials, initialize_app

# cred = credentials.Certificate("api/src/key.json")  # change key.json to actual one
# default_app = initialize_app(
#     cred, {"databaseURL": "https://dsci551---oogabooga-default-rtdb.firebaseio.com/"}
# )


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "password"  # change

    from .userAPI import userAPI

    app.register_blueprint(userAPI, url_prefix="/user")

    return app
