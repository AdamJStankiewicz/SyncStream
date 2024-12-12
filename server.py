from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import uuid
from flask_cors import CORS

import sqlite3
import os
import json
import hashlib
import random

app = Flask(__name__)
CORS(app)

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


class Account:

    sessions = {}

    def create_account(data):
        id = str(uuid.uuid1())
        password = Account.encrypt_password(data["password"])
        Database.insert_user(id, data["username"], password)
        return str("Account created. " + " Username: " + data["username"] + " Password: " + data["password"])
    
    def encrypt_password(password):
        encoded_string = password.encode()
        sha256_hash = hashlib.sha256()
        sha256_hash.update(encoded_string)
        result = str(sha256_hash.hexdigest())
        
        return result

    def login(request):
        if not Account.verify_account(request["username"], request["password"]):
            return {"ERROR" : "Incorrect account info"}
        id = Database.get_id_by_username(request["username"])
        return Account.create_session(id)

    def create_session(id):
        sessionID = str(uuid.uuid1())
        Account.sessions[sessionID] = id
        response = {"id": id,
                    "sessionID": sessionID}
        return response

    def confirm_session(id, sessionID):
        return Account.sessions[sessionID] == id

    def verify_account(username, password):
        dbPassword = Database.get_password_by_username(username)
        return Account.encrypt_password(password) == dbPassword

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

    def insert_user(id,username,password):
        cursor.execute("INSERT INTO emp VALUES (?, ?, ?)", (id, username, password))
        print("New account added to database!")
        connection.commit()

    def print_db():
        cursor.execute("SELECT * FROM emp")
        ans = cursor.fetchall()
        res = {}
        for row in ans:
            res[row[0]] = {"UUID": row[1], "username": row[2], "password": row[3]}
        return res

    def exists(id="",username=""):
        cursor.execute("""SELECT UUID
                            ,username
                    FROM emp
                    WHERE UUID=?
                        OR username=?""",
                    (id, username))
        
        
        result = cursor.fetchone()
        return result

    def get_id_by_username(username):
        cursor.execute("SELECT UUID FROM emp WHERE username = ?",(username,))
        
        result = cursor.fetchone()
        if result:
            res = result[0]
            return res
        return None

    def get_password_by_username(username):
        cursor.execute("SELECT password FROM emp WHERE username = ?",(username,))
        
        result = cursor.fetchone()
        if result:
            res = result[0]
            return res
        return None
    
    def get_username_by_userid(id):
        cursor.execute("SELECT username FROM emp WHERE UUID = ?",(id,))
        
        result = cursor.fetchone()
        if result:
            res = result[0]
            return res
        return None

    
#Class for each user
class User:
    def __init__(self, user_id, username, is_host=False):
        self.user_id = user_id
        self.username = username
        self.is_host = is_host

    def set_host(self, is_host):
        self.is_host = is_host

#Class for functions in the lobby
class Lobby:
    def __init__(self, lobbyId, host, lobbyCode):
        self.lobbyId = lobbyId

        self.host = host
        self.lobbyCode = lobbyCode
        self.videoQueue = []
        self.currentVideo = None
        self.participants = {host.user_id: host}
        self.isActive = True
        self.userTimes = {}

    def addVideoToQueue(self, videoUrl):
        self.videoQueue.append(videoUrl)

    def remVideoFromQueue(self, videoUrl):
        if videoUrl in self.videoQueue:
            self.videoQueue.remove(videoUrl)
        else:
            raise ValueError(f"Video '{videoUrl}' not found in the queue")

    def getVideoQueue(self):
        return self.videoQueue

    def playNextVideo(self):
        if self.videoQueue:
            self.currentVideo = self.videoQueue.pop(0)
        else:
            print("Error: no videos in the queue to play.")


    def join(self, user):
        if user.user_id not in self.participants:
            self.participants[user.user_id] = user
        else:
            print(f"Error: User with sessionId {user.user_id} is already in the lobby.")

    def disconnect(self, userID):
        if userID in self.participants:

            removed_user = self.participants.pop(userID)
            if removed_user.is_host:

                self.isActive = False
                print(f"Host {userID} left, lobby deactivated.")


    def timeStorage(self, user_id, currentTime):
        self.userTimes[user_id] = currentTime


#Class for setting up a lobby
class LobbySystem:
    def __init__(self):
        self.lobbies = {}
        #self.lobbyCodes = {}

    def createLobby(self, host):
        lobbyId = str(uuid.uuid4())
        lobbyCode = self.generate_lobby_code()

        while lobbyCode in self.lobbies:
            lobbyCode = self.generate_lobby_code()

        newLobby = Lobby(lobbyId, host, lobbyCode)
        self.lobbies[lobbyCode] = newLobby
        return newLobby

    def generate_lobby_code(self):
        return("123")

    def getLobby(self, lobbyCode):
        return self.lobbies.get(lobbyCode)

    def deleteLobby(self, lobbyCode):
        if lobbyCode in self.lobbies:
            del self.lobbies[lobbyCode]

    def getAllLobbies(self):
        serialized_lobbies = serializeLobbySystem(self)
        return serialized_lobbies

def serializeLobbySystem(lobbySystem):
    lobbiesData = {}
    for lobbyId, lobby in lobbySystem.lobbies.items():
        lobbiesData[lobbyId] = {
            "host": lobby.host.user_id,  # Only userId here
            "videoQueue": lobby.videoQueue,
            "currentVideo": lobby.currentVideo,
            "participants": [user.user_id for user in lobby.participants.values()],  # Only userId here
            "isActive": lobby.isActive
        }
    
    return lobbiesData
    

lobby_system = LobbySystem()

@app.route('/', methods=['GET'])
def main():
    print("Hello")
    print(Database.exists("","Gwizz"))
    return "SyncStream Online"

@app.route('/get_userID/<username>')
def get_userID(username):
    return Database.get_id_by_username(username)

@app.route('/account', methods=['GET', 'POST'])
def create_account():
    return Account.create_account(request.json)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return Account.login(request.json)

#Route for when user creates a lobby
@app.route('/lobby/create', methods=['GET', 'POST'])
def create_lobby():
    user_id = request.json["userId"]
    username = Database.get_username_by_userid(user_id)

    user = User(user_id, username, is_host=True)

    new_lobby = lobby_system.createLobby(user)

    return {
        'lobbyId': new_lobby.lobbyId,
        'lobbyCode': new_lobby.lobbyCode,
        'host': {
            'userId': new_lobby.host.user_id
        },
        'participants': [
            {
                'userId': participant.user_id,
                'isHost': participant.is_host
            } for participant in new_lobby.participants.values()
        ],
        'videoQueue': new_lobby.videoQueue,
        'currentVideo': new_lobby.currentVideo,
        'isActive': new_lobby.isActive}
    
#Route for when user joins a lobby
@app.route('/lobby/join', methods=['GET', 'POST'])
def join_lobby():
    user_id = request.json["userId"]
    lobby_code = request.json["lobbyCode"]
    username = Database.get_username_by_userid(user_id)

    lobby = lobby_system.getLobby(lobby_code)

    user = User(user_id, username, is_host=False)
    lobby.join(user)

    return {
        'lobbyId': lobby.lobbyId,
        'lobbyCode': lobby.lobbyCode,
        'host': {
            'userId': lobby.host.user_id
        },
        'participants': [
            {
                'userId': participant.user_id,
                'isHost': participant.is_host
            } for participant in lobby.participants.values()
        ],
        'videoQueue': lobby.videoQueue,
        'currentVideo': lobby.currentVideo,
        'isActive': lobby.isActive
    }

#Route for each lobby
@app.route('/lobby/<lobbyCode>', methods=['POST'])
def get_lobby_state(lobbyCode):
    lobby = lobby_system.getLobby(lobbyCode)

    if lobby:
        return {
            'lobbyId': lobby.lobbyId,
            'lobbyCode': lobby.lobbyCode,
            'host': {
                'userId': lobby.host.user_id
            },
            'participants': [
                {
                    'userId': participant.user_id,
                    'isHost': participant.is_host,
                    'username': Database.get_username_by_userid(participant.user_id)

                } for participant in lobby.participants.values()
            ],
            'videoQueue': lobby.videoQueue,
            'currentVideo': lobby.currentVideo,
            'isActive': lobby.isActive
        }
    else:
        return {"error": "Lobby not found"}, 404


#Route to get the host current youtube time
@app.route('/lobby/<lobbyCode>/get_host_time', methods=['POST'])
def get_host_time(lobbyCode):    
    user_id = request.json["userId"]
    host_time = request.json["hostTime"]

    lobby = lobby_system.getLobby(lobbyCode)

    lobby.timeStorage(user_id, host_time)

    return {
        'hostId': user_id,
        'currentTime': host_time
    }


#Route to send the user the host current youtube time
@app.route('/lobby/<lobbyCode>/send_host_time', methods=['POST'])
def update_time(lobbyCode):
    lobby = lobby_system.getLobby(lobbyCode)

    host_id = lobby.host.user_id
    
    host_time = lobby.userTimes.get(host_id)

    return {
        'hostTime': host_time
    }

@app.route('/lobby/<lobbyCode>/add_to_queue', methods=['POST'])
def add_to_queue(lobbyCode):
    lobby = lobby_system.getLobby(lobbyCode)
    video = request.json["video"]


    lobby.addVideoToQueue(video)


    print("Video added to queue: " + video)



    return {
        'lobbyQueue' : lobby.getVideoQueue()
    }



@app.route('/lobby/<lobbyCode>/remove_from_queue', methods=['POST'])
def rem_from_queue(lobbyCode):
    try:
        lobby = lobby_system.getLobby(lobbyCode)
        if not lobby:
            return {"error": "Lobby not found"}, 404

        # Safely get video from request body or default to None
        video = request.json.get("video", None)

        # If no video is provided, remove the first video in the queue
        if video is None:
            if lobby.getVideoQueue():
                video = lobby.getVideoQueue()[0]
            else:
                return {"error": "Queue is empty"}, 400

        # Attempt to remove the video
        try:
            lobby.remVideoFromQueue(video)
        except ValueError:
            return {"error": f"Video '{video}' not found in the queue"}, 404

        print("Video removed from queue: " + video)
        return {"lobbyQueue": lobby.getVideoQueue()}, 200
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {"error": "Internal server error"}, 500

@app.route('/lobby/<lobbyCode>/disconnect_user', methods=['POST'])
def disconnect_user(lobbyCode):
    lobby = lobby_system.getLobby(lobbyCode)
    userID = request.json["userId"]

    lobby.disconnect(userID)
    print("User: " + userID + " disconnected")
    return {
        'user_removed' : userID
    }


init()

socketio.run(app,host='0.0.0.0',port=1477, allow_unsafe_werkzeug=True, debug=False)



