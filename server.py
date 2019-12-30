import os

from bottle import Bottle, route, run, static_file, request,SimpleTemplate,template
from pathlib import Path
import pandas as pd
from collections import defaultdict
from repl_comments import create_hash,get_pwhash


PATH = os.getcwd()
pw_hash = get_pwhash()
total_list = defaultdict(int)
new_list = defaultdict(int)


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


@route('/')
@route('/table')
@route('/page.html')
def table():
    
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    output = '\n\nYour IP is: {}\n'.format(client_ip)
    new_list[client_ip] += 1

    df = gettable()
    df_html = df.to_html()
    return template('page',table_html=df_html,output=output)

@route('/form', method='POST')
def resetIPs():
    pw = request.forms.get('password')
    pw_confirmation = create_hash(pw)
    if pw_hash == pw_confirmation:
        saveIPs()
        return '<p>Your login information was correct.</p><a href="page.html" class="btn">Reset Page</a>'
    else:
        return '<p>Login failed.</p><a href="page.html" class="btn">Reset Page</a>'
def gettable():
    data = defaultdict(int)
    for ip in total_list:
        data[ip] = total_list[ip] + new_list[ip]

    for ip in new_list.keys():
        if ip not in total_list.keys():
            data[ip] = new_list[ip]
    
    df = pd.DataFrame(list(zip(data.keys(),data.values())),columns = ["IP Address","Count"])
    return df

def printIPs():
    for ip in Ip_list:
        print("IP : {}Count: {}".format(ip, Ip_list[ip]))

def loadIPs():
    with open("IPadresses.txt", "r") as f:
        line = f.readline()
        
        while line:
            ip,count = line.split(' ')
            try:
                total_list[ip] = int(count)
            except Exception as e: 
                print(e)
            line = f.readline()
def saveIPs():
    loadIPs()
    for ip1 in new_list:
        total_list[ip1] += new_list[ip1]

    with open("IPadresses.txt", "w") as f:
        for ip in total_list:
            f.write(ip + ' ' + str(total_list[ip]) + '\n')
    total_list.clear()
    new_list.clear()


    
if __name__ == "__main__":
    loadIPs()
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)),reloader=True)
    saveIPs()