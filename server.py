import os

from bottle import Bottle, route, run, static_file
from pathlib import Path

PATH = os.getcwd()
print(PATH+"/static")
@route('/')
@route('/index.html')
def home_page():
    return Path("index.html").read_text()


@route('/login')
def login():
    return "<h1>On Login Page </h1>"
@route('/education.html')
def education_page():
    return Path("education.html").read_text()

@route('/extras.html', methods=('GET'))
def extras_page():
    return Path("extras.html").read_text()

@route('/static/<filename:path>')
def send_static(filename):
    print("path is: ",PATH)
    return static_file(filename, root= os.path.join(PATH,"static"))

run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))