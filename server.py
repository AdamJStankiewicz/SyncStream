from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import uuid

import sqlite3
import os
import json

app = Flask(__name__)
socketio = SocketIO(app)

connection = sqlite3.connect('syncstream.db', check_same_thread=False)
cursor = connection.cursor()

def init():
    server_info = {"DB_INIT" : 0}

    s = Storage('server_info.json', server_info)
    db = Database(cursor)

    s.initiate_storage

    if s.get_data("DB_INIT") == 1:
        print("Database already initialized")
    else:
        db.initiate_db()
        s.store({"DB_INIT": 1})



        
class Storage:

    def __init__(self, server_info_path, server_info):
        self.server_info_path = server_info_path
        self.server_info = server_info
        self.initiate_storage()

    def initiate_storage(self):
        if os.path.exists(self.server_info_path):
            with open(self.server_info_path, 'r') as f:
                self.server_info = json.load(f)
        with open(self.server_info_path, 'w') as f:
            json.dump(self.server_info, f)

    def store(self, data):
        with open(self.server_info_path, 'w') as f:
            json.dump(data, f)

    def get_data(self, key):
        with open(self.server_info_path, 'r') as f:
            data = json.load(f)
        return data[key]

class Database:
    def __init__(self, cursor):
        self.cursor = cursor

    def initiate_db(self):
        sql_command = """CREATE TABLE emp (
        UUID VARCHAR(36),
        username VARCHAR(50),
        password VARCHAR(50)
        );"""
        self.cursor.execute(sql_command)
        print("DATABASE INITIATED")

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

init()

socketio.run(app,host='0.0.0.0',port=1477, allow_unsafe_werkzeug=True, debug=False)