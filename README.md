# π-WoL

A Flask-based web application that lets you send magic packets to a target machine from the browser.

![main-page](https://i.imgur.com/yqoxMPL.png)

## Usage

### Setup target machine

Enable Wake-On-Lan.

(optional) Set a static IP address.

---

### Setup π-WoL

Edit `config.ini` and enter your the target machine's configuration.

```
<mac address. Example: ff.ff.ff.ff.ff.ff>
<local ip address. Example: 255.255.255.255>
```

Note that if the target machine does not have a static IP address, you will have to edit this file every time the machine restarts.

---

Make sure that [Python 3](https://www.python.org/) is installed.

Then install the dependencies:

```
pip install -r ./requirements.txt
```

---

Set environment variables:

Unix, Linux, MacOS, etc.

```
export FLASK_APP = remote_wol
export FLASK_ENV = production
```

Windows

```
set FLASK_APP = remote_wol
set FLASK_ENV = production
```

---

Run the server:

```
flask run --host=0.0.0.0
```

Then enter the password. You will need this password every time you want to send a magic packet.

---

You can now go to `http://[pi-wol machine's local IP]:5000` to access the web interface.

## Remote Access

You can use tunneling software like ngrok or plain ssh tunneling to allow π-WoL to be accessed remotely.
