from passlib.hash import sha256_crypt
import requests
import json

salt = "!LINKEDIN"
default_website = "https://cuhack.it/"

dbid = "36978354-cbaf-430d-8995-12d491564a45"
rid = "us-east1"
ksid = "e_link"

auth_url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v1/auth"
auth_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Cassandra-Request-Id":"7d86a16e-9407-4089-9f8c-cb968e89b2cc"
}
auth_body = {
    "username":"e_link",
    "password":"Z8f7*yFvZVoPWYsqLN8q"
}
auth_response = requests.post(auth_url, headers=auth_headers, data=json.dumps(auth_body))
auth_token = auth_response.json()["authToken"]


def username_free(username):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/users/{username}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    response = requests.request("GET", url, headers=headers)
    print(response.json())
    return response.json()["count"] == 0

def has_account(username):
    return not username_free(username)

def make_account(username, password, email, website, image):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/users/"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    data = {
        "username": username,
        "password": password,
        "email": email,
        "website": website,
        "image": image
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    return True

def check_credentials(username, password):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/users/{username}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    response = requests.request("GET", url, headers=headers)
    return sha256_crypt.verify(salt+password+salt, response.json()["data"][0]["password"])

def set_image(username, image):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/users/{username}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    data = {
        "image": image
    }
    response = requests.request("PATCH", url, headers=headers, data=json.dumps(data))
    return response.json()

def get_image(username):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/users/{username}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()["data"][0]["image"]

def set_website(username, website):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/users/{username}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    data = {
        "website": website
    }
    response = requests.request("PATCH", url, headers=headers, data=json.dumps(data))
    return response.json()

def get_website(username):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/users/{username}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()["data"][0]["website"]

def set_email(username, email):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/users/{username}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    data = {
        "email": email
    }
    response = requests.request("PATCH", url, headers=headers, data=json.dumps(data))
    return response.json()

def get_email(username):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/users/{username}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()["data"][0]["email"]

def add_connection(user1, user2):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/connections/"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    data = {
        "user1": user1,
        "user2": user2,
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    return True

def remove_connection(user1, user2):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/connections/{user1}/{user2}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    data = {
        "user1": user1,
        "user2": user2,
    }
    response = requests.request("DELETE", url, headers=headers, data=json.dumps(data))
    return True

def get_connections(username):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/connections/{user}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    response = requests.request("GET", url, headers=headers)
    return [x['user2'] for x in response.json()["data"]]

def change_connection(username1, username2):
    if username2 not in get_connections(username1):
        add_connection(username1, username2)
    else:
        remove_connection(username1, username2)
    return True
