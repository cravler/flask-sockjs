# -*- coding: utf-8 -*-

# Flask
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', endpoint='auth')

# Twisted
from flask.ext.twisted import Twisted
twisted = Twisted(app)

# SockJS
import json
from flask.ext.sockjs import SockJS, broadcast
ws = SockJS(twisted)
auth = ws.createEndpoint('auth')

def authenticated():
    return [transport for transport in auth.transports() if transport.authenticated is True]

@auth.on('connection')
def ws_connection(transport):
    transport.authenticated = False
    transport.write(json.dumps({'cmd': 'AUTHENTICATION_REQUIRED'}))

@auth.on('data')
def ws_message(transport, message):
    if transport.authenticated:
        transport.write(message)
    else:
        data = {}
        try:
            data = json.loads(message)
        except ValueError:
            pass

        if 'cmd' in data and data['cmd'] == 'AUTHENTICATE':
            if 'key' in data and data['key'] == 'auth-key':
                transport.authenticated = True
                transport.write(json.dumps({'cmd': 'AUTHENTICATED'}))
                broadcast(json.dumps({'connections': len(authenticated())}), authenticated())
            else:
                transport.write(json.dumps({'cmd': 'AUTHENTICATION_FAILED', 'reason': 'Wrong key'}))
        else:
            transport.write(json.dumps({'cmd': 'AUTHENTICATION_REQUIRED'}))

@auth.on('close')
def ws_close(transport, reason):
    broadcast(json.dumps({'connections': len(authenticated())}), authenticated())

# Main
if __name__ == '__main__':
    app.run()
