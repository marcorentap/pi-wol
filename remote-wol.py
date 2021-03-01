from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def show_main_page(inputStatus = None):
    status = "UNKNOWN" 
    if (inputStatus != None):
        status = inputStatus
    return render_template('index.html', status=status)

@app.route('/ping')
def send_ping():
    return "Ping sent!"

@app.route('/wake')
def wake_target():
    return "Magic packet sent"


# def send_ping():
    
# def send_magic_packet()