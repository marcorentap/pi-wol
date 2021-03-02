from flask import Flask, session, redirect, url_for, request
from flask import render_template
from wakeonlan import send_magic_packet
from pythonping import ping
from hashlib import sha256
import sys

app = Flask(__name__)
app.secret_key = "13370x0539"

TARGET_MAC_ADDRESS = "02:10:5C:6E:C6:70"
TARGET_STATIC_IP  = "172.26.112.1"
PASSWORD_FILE = "pass.txt"

@app.route('/')
def main_page():
    wol_status = ""
    status = ""

    if send_ping():
        status = "ONLINE"
    else:
        status = "OFFLINE"

    if  'wol_status' in session:
        wol_status = session['wol_status']
    else:
        session['wol_status'] = ""

    page = render_template('index.html', status=status, wol_status=wol_status)
    session.pop('status')
    session.pop('wol_status')

    return page

@app.route('/wake', methods=['GET', 'POST'])
def wake_target():
    if request.method == 'POST':
        if authenticate_user(request.form['password']):
            send_magic_packet(TARGET_MAC_ADDRESS)
            session['wol_status'] = 'success'
        else:
            session['wol_status'] = 'fail'

        return redirect(url_for('main_page'))
    else:
        return redirect(url_for('auth_form'))

@app.route('/auth')
def auth_form():
    return render_template('auth.html')

def authenticate_user(inputPassword):
    inputPassword = inputPassword.encode("utf-8")
    hashedInput = sha256(inputPassword)
    hashedDigest = hashedInput.hexdigest()

    storedDigest = ""
    with open(PASSWORD_FILE) as file:
        storedDigest = file.read()

    print("Input: {}\nStored: {}".format(hashedDigest, storedDigest), file=sys.stderr)
    if storedDigest == hashedDigest:
        return True
    else:
        return False

def send_ping():
    pingResponses = ping(TARGET_STATIC_IP, verbose=True, out=sys.stderr)
    ping_status = pingResponses.success()
    print("Ping Status: {}".format(ping_status), file=sys.stderr)
    if ping_status:
        session['status'] = 'ONLINE'
        session['ping_status'] = 'success'
    else:
        session['status'] = 'OFFLINE'
        session['ping_status'] = 'fail'
    return ping_status 
