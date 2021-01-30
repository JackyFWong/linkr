from passlib.hash import sha256_crypt

salt = "!LINKEDIN"
default_website = "https://www.google.com"

data = {} # volatile!
websites = {}
connections = {}

def username_free(username):
    return username not in data

def has_account(username):
    return not username_free(username)

def make_account(username, password):
    assert username not in data, "ERROR! username in data"
    data[username] = sha256_crypt.encrypt(salt+password+salt)
    websites[username] = default_website
    return True

def check_credentials(username, password):
    enc_pass = data.get(username, "")
    return sha256_crypt.verify(salt+password+salt, enc_pass)

def set_website(username, website):
    websites[username] = website

def get_website(username):
    return websites.get(username, default_website)

def add_connection(username1, username2):
    if username2 not in connections.get(username1, []):
        connections[username1] = connections.get(username1, []).append(username2)
        return True
    return False

def remove_connection(username1, username2):
    if username2 in connections.get(username1, []):
        connections[username1].remove(username2)

def get_connections(username):
    return connections.get(username, [])

def change_connection(username1, username2):
    if username2 not in get_connections(username1):
        add_connection(username1, username2)
    else:
        remove_connection(username1, username2)
    return True
