import requests

def create_account():
    url = "http://127.0.0.1:1477/account"

    data = {"username" : "r",
            "password" : "l"}

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url,json=data,headers=headers)

    print(response)

def login():
    url = "http://127.0.0.1:1477/login"

    data = {"username" : "r",
            "password" : "l"}

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url,json=data,headers=headers)

    json = response.json()

    print(json)

def createLobby():
    url = "http://127.0.0.1:1477/lobby/create"
    
    data = {"userId": "ff123a8b-b449-11ef-82a9-28d0ea7d6477"}
    
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url,json=data,headers=headers)

    
    json = response.json()

    print(json)

def joinLobby():
    url = "http://127.0.0.1:1477/lobby/join"
    
    data = {"userId": "9ce91712-b031-11ef-bb0b-086ac515207e",
            "lobbyCode": "123"}
    
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url,json=data,headers=headers)

    
    json = response.json()

    print(json)

def lobby():
    url = "http://127.0.0.1:1477/lobby/123"
    
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    
    json = response.json()

    print(json)



def getHostTime():
    url = "http://127.0.0.1:1477/lobby/123/get_host_time"
    
    data = {"userId": "9dd02531-af61-11ef-8b66-086ac515207e",
            "hostTime": 80}
    
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url,json=data,headers=headers)

    
    json = response.json()

    print(json)

def sendHostTime():
    url = "http://127.0.0.1:1477/lobby/123/send_host_time"
    
    
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    
    json = response.json()

    print(json)


def addVideoToQueue():
    url = "http://127.0.0.1:1477/lobby/123/add_to_queue"

    data = {"video": "YGcoiRkei4s"}

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url,json=data,headers=headers)
    json = response.json()

    print(json)

#createLobby()
#create_account()

addVideoToQueue()

#8a9b7061-af52-11ef-92c9-086ac515207e


#9dd02531-af61-11ef-8b66-086ac515207e

#9ce91712-b031-11ef-bb0b-086ac515207e