import requests

def create_account():
    url = "http://127.0.0.1:1477/account"

    data = {"username" : "Buster",
            "password" : "poopy"}

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url,json=data,headers=headers)

    print(response)

def login():
    url = "http://127.0.0.1:1477/login"

    data = {"username" : "Buster",
            "password" : "poopy1"}

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url,json=data,headers=headers)

    json = response.json()

    print(json)

login()