from flask import Flask, render_template

# from src import create_app
from src.userAPI_noDjango import userAPI

app = Flask(__name__, template_folder="templates")
app.register_blueprint(userAPI)

# app = create_app()


@app.route("/")
def homepage():
    return render_template("landingPage.html")


@app.route("/help")
def help():
    return render_template("huh.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/user")
def user():
    return render_template("user.html")


if __name__ == "__main__":
    app.run(debug=True)
