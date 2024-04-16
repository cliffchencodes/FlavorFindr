from flask import Flask, render_template

# from src import create_app
from src.userAPI_noDjango import userAPI

app = Flask(__name__, template_folder="templates")
app.register_blueprint(userAPI)

# app = create_app()


@app.route("/")
def homepage():
    return render_template("homepage.html")


if __name__ == "__main__":
    app.run(debug=True)
