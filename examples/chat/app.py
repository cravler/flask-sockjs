# -*- coding: utf-8 -*-

# Flask
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', endpoint='chat')

# Twisted
from flask.ext.twisted import Twisted
twisted = Twisted(app)

# SockJS
from flask.ext.sockjs import SockJS, broadcast
ws = SockJS(twisted)
chat = ws.createEndpoint('chat')

@chat.on('data')
def ws_message(transport, message):
    broadcast(message, chat.transports())

# Main
if __name__ == '__main__':
    app.run()
