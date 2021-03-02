from flask import Flask, session, redirect, url_for
from flask import render_template

app = Flask(__name__)
app.secret_key = "13370x0539"

@app.route('/')
def main_page():
    status = ""
    ping_status = ""

    if 'status' in session:
        status = session['status']
    else:
        session['status'] = ""
    if  'ping_status' in session:
        ping_status = session['ping_status']
    else:
        session['ping_status'] = ""

    page = render_template('index.html', status=status, ping_status=ping_status)
    session.pop('status')
    session.pop('ping_status')
    return page

@app.route('/ping')
def send_ping():
    session['status'] = 'UNKNOWN'
    session['ping_status'] = 'fail'
    return redirect(url_for('main_page'))
    # return "Ping sent!"

@app.route('/wake')
def wake_target():
    session['status'] = 'OFFLINE'
    session['ping_status'] = 'success'
    return redirect(url_for('main_page'))
    # return "Magic packet sent"


# def send_ping():
    
# def send_magic_packet()