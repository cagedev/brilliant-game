from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def default():
    return "default"

if __name__ == "__main__":
    # app.run()
    socketio.run(app)
