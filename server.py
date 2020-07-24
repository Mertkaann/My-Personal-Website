import os

from bottle import Bottle, route, run, static_file, request, SimpleTemplate, template
from pathlib import Path
from collections import defaultdict
from repl_comments import create_hash, get_pwhash

PATH = os.getcwd()
pw_hash = get_pwhash()
total_list = defaultdict(int)
new_list = defaultdict(int)


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
    return static_file(filename, root=os.path.join(PATH, "static"))


@route('/table')
@route('/page.html')
def table():

    client_ip = request.environ.get(
        'HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    output = 'Your IP is: {}'.format(client_ip)
    new_list[client_ip] += 1

    df = gettable()
    return template('page', table_html=df, output=output)


@route('/form', method='POST')
def resetIPs():
    pw = request.forms.get('password')
    answer1 = request.forms.get('Yes')
    answer2 = request.forms.get('No')
    print("#"*100, answer1, answer2, "#"*100)
    pw_confirmation = create_hash(pw)
    output = ""
    if answer1 == "True" or answer2 == "True":
        print("&"*100)
        output = "<p>Review Sent Succesfully</p>"
    if pw_hash == pw_confirmation:
        saveIPs()
        return output + '<p>Your login information was correct.</p><a href="page.html" class="btn">Reset Page</a>'
    else:
        return output + '<p>Login failed.</p><a href="page.html" class="btn">Reset Page</a>'


def gettable():
    data = defaultdict(int)
    for ip in total_list:
        data[ip] = total_list[ip] + new_list[ip]

    for ip in new_list.keys():
        if ip not in total_list.keys():
            data[ip] = new_list[ip]

    table = '''
    <table>
        <thead>
            <tr style="text-align: right;">
                <th></th>
                <th>IP Address</th>
                <th>Count</th>
            </tr>
        </thead>
        <tbody>
            '''

    for i, (keys, values) in enumerate(zip(data.keys(), data.values())):
        table += '''
            <tr>
                <th>{}</th>
                <td>{}</td>
                <td>{}</td>
            </tr>
            '''.format(i, keys, values)

    table += '''
        </tbody>
    </table>
            '''
    return table


def loadIPs():
    with open(os.path.join(PATH, "IPadresses.txt"), "r") as f:
        line = f.readline()

        while line:
            ip, count = line.split(' ')
            try:
                total_list[ip] = int(count)
            except Exception as e:
                print(e)
            line = f.readline()


def saveIPs():
    loadIPs()
    for ip in new_list:
        total_list[ip] += new_list[ip]

    with open(os.path.join(PATH, "IPadresses.txt"), "w") as f:
        for ip in total_list:
            f.write(ip + ' ' + str(total_list[ip]) + '\n')
    total_list.clear()
    new_list.clear()


if __name__ == "__main__":
    loadIPs()
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), reloader=True)
    saveIPs()
