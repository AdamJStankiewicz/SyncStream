from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import uuid

app = Flask(__name__)
socketio = SocketIO(app)


class User:
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

class Lobby:
    def __init__(self, lobbyId, host):
        self.lobbyId = lobbyId
        self.host = host
        self.videoQueue = []
        self.currentVideo = None
        self.participants = [host]
        self.isActive = True

    def addVideoToQueue(self, user, videoUrl):
        if user == self.host:
            self.videoQueue.append(videoUrl)
        else:
            print("Error: " + user.username + " is not allowed to add videos to the queue.")

    def playNextVideo(self):
        if self.videoQueue:
            self.currentVideo = self.videoQueue.pop(0)
        else:
            print("Error: no videos in the queue to play.")

    def join(self, user):
        if user not in self.participants:
            self.participants.append(user)
        else:
            print("Error: " + user.username + " is already in the lobby.")

    def leave(self, user):
        if user in self.participants:
            self.participants.remove(user)
            if user == self.host:
                self.isActive = False

class LobbySystem:
    def __init__(self):
        self.lobbies = {}

    def createLobby(self, host):
        lobbyId = str(uuid.uuid4())
        newLobby = Lobby(lobbyId, host)
        self.lobbies[lobbyId] = newLobby
        return newLobby

    def getLobby(self, lobbyId):
        return self.lobbies.get(lobbyId)

    def deleteLobby(self, lobbyId):
        if lobbyId in self.lobbies:
            del self.lobbies[lobbyId]

def serializeLobbySystem(lobbySystem):
    lobbiesData = {}
    for lobbyId, lobby in lobbySystem.lobbies.items():
        lobbiesData[lobbyId] = {
            "host": lobby.host.username,
            "videoQueue": lobby.videoQueue,
            "currentVideo": lobby.currentVideo,
            "participants": [user.username for user in lobby.participants],
            "isActive": lobby.isActive
        }
    
    return lobbiesData


@app.route('/', methods=['GET'])
def main():
    print("Hello")
    return "SyncStream Online"

socketio.run(app,host='0.0.0.0',port=1477, allow_unsafe_werkzeug=True, debug=False)