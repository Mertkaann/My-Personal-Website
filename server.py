import os

from bottle import Bottle, route, run, static_file, request,SimpleTemplate,template
from pathlib import Path
import pandas as pd

PATH = os.getcwd()


@route('/')
@route('/index.html')
def home_page():
    return Path("index.html").read_text()

@route('/education.html')
def education_page():
    return Path("education.html").read_text()

@route('/extras.html', methods=('GET'))
def extras_page():
    return Path("extras.html").read_text()

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root= os.path.join(PATH,"static"))


@route('/table')
@route('/page.html')
def table():
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    output = 'Your IP is: {}\n'.format(client_ip)
    # do something to create a pandas datatable
    df = pd.DataFrame(data=[[1,2],[3,4]],columns = ["IP Address","Count"])
    df_html = df.to_html()  # use pandas method to auto generate html
    return template('page',table_html=df_html,output=output)


run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)),reloader=True)