import os

from bottle import Bottle
from pathlib import Path

def home_page():
    return Path("index.html").read_text()
def education_page():
    return Path("education.html").read_text()
def extras_page():
    return Path("extras.html").read_text()

def create_app():
    app = Bottle()
    app.route("/", "GET", home_page)
    app.route("/index.html", "GET", home_page)
    app.route("/education.html", "GET", education_page)
    app.route("/extras.html", "GET", extras_page)
    return app


application = create_app()
application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
