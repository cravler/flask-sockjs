# -*- coding: utf-8 -*-

# Flask
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', endpoint='echo')

# Twisted
from flask.ext.twisted import Twisted
twisted = Twisted(app)

# SockJS
from flask.ext.sockjs import SockJS
ws = SockJS(twisted)
echo = ws.createEndpoint('echo')

@echo.on('data')
def ws_message(transport, message):
    transport.write(message)

# Main
if __name__ == '__main__':
    app.run()
