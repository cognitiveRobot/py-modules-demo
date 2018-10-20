from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from time import sleep
from threading import Thread


app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = 'secret'

thread = Thread()

@app.route('/')
def index():
    return render_template('index.html')

test_message_run = 0

# class ReadSensor(Thread):
#     def __init__(self):
#         self.delay = 1
#         super(ReadSensor, self).__init__()
#
#     def run(self):
#         global test_message_run
#         test_message_run += 1
#         print(test_message_run)
#         socketio.emit('newnumber', {'number': test_message_run}, namespace='/test')
#
#
# socketio = SocketIO(app)
#
# @socketio.on('connect', namespace='/test')
# def test_connect():
#
#     global thread
#     print('Client Connected')
#
#     if not thread.isAlive():
#         print("Starting Thread")
#         thread = ReadSensor()
#         thread.Timer(1, loop).start()


if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app)
