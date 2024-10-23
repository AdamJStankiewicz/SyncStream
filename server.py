from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def main():
    print("Hello")
    return "SyncStream Online"

socketio.run(app,host='0.0.0.0',port=1477, allow_unsafe_werkzeug=True, debug=False)