from passlib.hash import sha256_crypt
import requests
import json

SALT = "!LINKEDIN"

DBID = "36978354-cbaf-430d-8995-12d491564a45"
RID = "us-east1"
KSID = "e_link"

USER_TBL = "users_new"
CONN_TBL = "conn_new"

AUTH_URL = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v1/auth"
AUTH_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Cassandra-Request-Id":"7d86a16e-9407-4089-9f8c-cb968e89b2cc"
}
AUTH_BODY = {
    "username":"e_link",
    "password":"Z8f7*yFvZVoPWYsqLN8q"
}
auth_response = requests.post(AUTH_URL, headers=AUTH_HEADERS, data=json.dumps(AUTH_BODY))
auth_token = auth_response.json()["authToken"]


def _verify(r: requests.Request, code: int):
    if r.status_code == code:
        return r.json()
    return None

def email_free(email):
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{USER_TBL}/{email}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    r = requests.get(url, headers=headers)
    body = _verify(r, 200)
    if body is None:
        return None
    return body["count"] == 0

def has_account(email):
    return not email_free(email)

def make_account(email, image, name, password, website):
    password = sha256_crypt.encrypt(SALT+password+SALT)
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{USER_TBL}/"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    data = {
        "email": email,
        "image": image,
        "name": name,
        "password": password,
        "website": website
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    # special verification
    if r.status_code == 201:
        return True
    elif r.status_code == 409:  # account already exists
        return False
    else:
        return None

def check_credentials(email, password):
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{USER_TBL}/{email}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    r = requests.get(url, headers=headers)
    body = _verify(r, 200)
    if body is None:
        return None
    return sha256_crypt.verify(SALT+password+SALT, body["data"][0]["password"])

def set_image(email, image):
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{USER_TBL}/{email}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    data = {
        "image": image
    }
    r = requests.patch(url, headers=headers, data=json.dumps(data))
    body = _verify(r, 200)
    if body is None:
        return None
    return body

def get_image(email):
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{USER_TBL}/{email}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    r = requests.request("GET", url, headers=headers)
    body = _verify(r, 200)
    if body is None:
        return None
    return body["data"][0]["image"]

def set_website(email, website):
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{USER_TBL}/{email}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    data = {
        "website": website
    }
    r = requests.patch(url, headers=headers, data=json.dumps(data))
    body = _verify(r, 200)
    if body is None:
        return None
    return body

def get_website(email):
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{USER_TBL}/{email}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    r = requests.get(url, headers=headers)
    body = _verify(r, 200)
    if body is None:
        return None
    return body["data"][0]["website"]

def set_name(email, name):
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{USER_TBL}/{email}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    data = {
        "name": name
    }
    r = requests.patch(url, headers=headers, data=json.dumps(data))
    body = _verify(r, 200)
    if body is None:
        return None
    return body

def get_name(email):
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{USER_TBL}/{email}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    r = requests.get(url, headers=headers)
    body = _verify(r, 200)
    if body is None:
        return None
    return body["data"][0]["name"]

def add_connection(email1, email2):
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{CONN_TBL}/"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    data = {
        "email1": email1,
        "email2": email2
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    body = _verify(r, 201)
    if body is None:
        return None
    return True

def remove_connection(email1, email2):
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{CONN_TBL}/{email1}/{email2}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    """
    data = {
        "user1": user1,
        "user2": user2,
    }
    """
    r = requests.delete(url, headers=headers)
    body = _verify(r, 204)
    if body is None:
        return None
    return True

def get_connections(email):
    print('inside get_connections')
    url = f"https://{DBID}-{RID}.apps.astra.datastax.com/api/rest/v2/keyspaces/{KSID}/{CONN_TBL}/{email}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    r = requests.get(url, headers=headers)
    body = _verify(r, 200)
    if body is None:
        return None
    conn_list = []
    for c in body["data"]:
        conn_list.append(c['email2'])
    print(r.json())
    print(r.headers)
    return conn_list

def change_connection(email1, email2):
    if email2 not in get_connections(email1):
        print("inside here")
        r = add_connection(email1, email2)
    else:
        print("inside there")
        # WHY REMOVING CONNECTION?!?!?!?
        r = remove_connection(email1, email2)
    if r is None:
        return None
    return True
