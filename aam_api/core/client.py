import requests
import json
import base64 as base64

class Client:
    DEFAULT_ENDPOINT = "https://api.demdex.com/v1/"

    def __init__(self, username, password, clientID, clientSecret, endpoint=DEFAULT_ENDPOINT):
        self.username = username
        self.password = password
        self.clientID = clientID
        self.clientSecret = clientSecret
        self.endpoint = endpoint
        self.oauthUrl = "https://api.demdex.com/oauth/token"
        clientDetails = "{}:{}".format(clientID, clientSecret)
        encodeDetails = base64.b64encode(clientDetails.encode())
        decodeDetails = encodeDetails.decode()
        self.header = {
            "Authorization": "Basic {}".format(decodeDetails),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.body = {"grant_type": "password",
            "username": self.username,
            "password": self.password
        }
        self.response = requests.post(self.oauthUrl,headers=self.header,data=self.body)

    @classmethod
    def from_json(cls, file_path):
        with open(file_path, mode="r") as json_file:
            credentials = json.load(json_file)
        return cls(credentials["username"],
                   credentials["password"],
                   credentials["clientID"],
                   credentials["clientSecret"])

    def __repr__(self):
        if self.response.status_code == 200:
            status = "Login Success. Token granted."
            token = self.response.json()['access_token']
        else:
            status = self.response.content
        return "User: {0} | Endpoint: {1} | Status: {2} ".format(self.username, self.endpoint, status)
