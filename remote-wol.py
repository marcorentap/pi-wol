from flask import Flask, session, redirect, url_for, request
from flask import render_template
from wakeonlan import send_magic_packet
from pythonping import ping
from hashlib import sha256
import sys


app = Flask(__name__)
app.secret_key = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit"

CONFIG_FILE = "config.ini"

TARGET_MAC_ADDRESS = ""
TARGET_STATIC_IP  = ""

with open(CONFIG_FILE) as f:
    TARGET_MAC_ADDRESS = f.readline()[:-1]
    TARGET_STATIC_IP = f.readline()[:-1]

passwordDigest = str(input("Enter password: "))
passwordDigest = sha256(passwordDigest.encode("utf-8")).hexdigest()

@app.route('/')
def main_page():
    print("Mac address is {}\nStatic IP is {}".format(TARGET_MAC_ADDRESS, TARGET_STATIC_IP), file=sys.stderr)
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

    if passwordDigest == hashedDigest:
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
