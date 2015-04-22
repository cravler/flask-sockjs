# Flask-SockJS

Simple integration of Flask and SockJS

## Installation

``` bash
pip install Flask-SockJS
```

## A Minimal Application

``` html
<!-- templates/index.html -->
<script src="//cdn.jsdelivr.net/sockjs/0.3.4/sockjs.min.js"></script>
<script>
    var sock = new SockJS('{{ ws_url_for(endpoint) }}');
    sock.onopen = function() {
        sock.send('Hello SockJS');
    };
    sock.onmessage = function(e) {
        console.log('message > ', e.data);
    };
</script>
```

``` python
# app.py
from flask import Flask, render_template
from flask.ext.twisted import Twisted
from flask.ext.sockjs import SockJS

app = Flask(__name__)
twisted = Twisted(app)
ws = SockJS(twisted)

@app.route("/")
def index():
    return render_template('index.html', endpoint='example')

example = ws.createEndpoint('example')

@example.on('data')
def ws_message(transport, message):
    transport.write(message)

if __name__ == '__main__':
    app.run()
```

## License

This software is under the MIT license. See the complete license in:

```
LICENSE
```