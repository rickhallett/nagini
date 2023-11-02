from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Oh elo, Harry! Not getting up to much trouble now are yeh?</p>"
