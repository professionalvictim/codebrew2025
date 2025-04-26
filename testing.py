import json
from requests import post

CLIENT_ID = "d71f5a9c01194c12b5b65f43032a0ea5"
CLIENT_SECRET = "17839d41b7f94d85829e78b9e2a66abb"

def get_token(CLIENT_ID, CLIENT_SECRET):
    # auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    # auth_bytes = auth_string.encode("utf-8")
    # auth_base64 = str(base64.b64decode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type" : "client_credentials",
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET
    }

    result = post(url, headers=headers, data=data)

    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


