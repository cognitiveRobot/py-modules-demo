from flask import Flask, render_template
from flask_sockets import Sockets
from geventwebsocket.handler import WebSocketHandler
import gevent import pywsgi
import datetime


app = Flask(__name__)
app.debug = True
sockets = Sockets(app)


@sockets.route('/time')
def time_socket(ws):
    """ Handler for websocket connections that constantly pushes
        the current time.
    """
    while True:
        gevent.sleep(3)
        ws.send(datetime.datetime.now().isoformat())


@app.route('/')
def hello():
    """ Render our default template
    """
    return render_template('index.html')

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
