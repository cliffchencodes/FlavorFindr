from src import create_app

app = create_app()


@app.route("/")
def index():
    return "Welcome to our homepage"


if __name__ == "__main__":
    app.run(debug=True)
