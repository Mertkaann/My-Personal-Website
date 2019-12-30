import os

from bottle import Bottle, route, run, static_file, request,SimpleTemplate,template
from pathlib import Path
import pandas as pd
from collections import defaultdict

PATH = os.getcwd()

Ip_list = defaultdict(int)


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
    Ip_list = loadIPs()
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    output = '\n\nYour IP is: {}\n'.format(client_ip)
    Ip_list[client_ip] += 1

    df = pd.DataFrame(list(zip(Ip_list.keys(),Ip_list.values())),columns = ["IP Address","Count"])
    df_html = df.to_html()
    return template('page',table_html=df_html,output=output)

def printIPs():
    for ip in Ip_list:
        print("IP : {}Count: {}".format(ip, Ip_list[ip]))

def loadIPs():
    with open("IPadresses.txt", "r") as f:
        line = f.readline()
        
        while line:
            ip,count = line.split(' ')
            Ip_list[ip] = int(count)
            line = f.readline()
        return Ip_list
def saveIPs():
    with open("IPadresses.txt", "w") as f:
        for ip in Ip_list:
            f.write(ip + ' ' + str(Ip_list[ip]) + '\n')


def addIP(Ip_list, client_ip):
    
    while ip in Ip_list:
        if(ip == client_ip):
            Ip_list

run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)),reloader=True)
saveIPs()
    
