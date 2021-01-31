import requests
import json
from pprint import pprint

dbid = "36978354-cbaf-430d-8995-12d491564a45"
rid = "us-east1"
ksid = "e_link"
url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v1/auth"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Cassandra-Request-Id":"7d86a16e-9407-4089-9f8c-cb968e89b2cc"
}

body = {
    "username":"e_link",
    "password":"Z8f7*yFvZVoPWYsqLN8q"
}

response = requests.post(url, headers=headers, data=json.dumps(body))

auth_token = response.json()["authToken"]
print(auth_token)

def select_row_from_table(table_name, prim_key):
    url = f"https://{dbid}-{rid}.apps.astra.datastax.com/api/rest/v2/keyspaces/{ksid}/{table_name}/{prim_key}"
    headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token,
    }
    response = requests.request("GET", url, headers=headers, data=json.dumps(body))
    pprint(response.json())


print(delete_connection("a", "c"))
