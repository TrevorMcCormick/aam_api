import requests
from aam_api.core.client import Client

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

global token
try:
    token = Client.from_json("aam_credentials.json").response.json()['access_token']
except:
    path = input("Path to aam credentials:  ")
    try:
        token = Client.from_json(path).response.json()['access_token']
    except:
        raise InputError("Invalid Path", "Credentials are invalid")

def apiRequest(call, method, data=""):
    url = "https://api.demdex.com/v1/{}/".format(call)
    header =  {'Authorization' : 'Bearer {}'.format(token),'accept': 'application/json',"Content-Type": "application/json"}
    response = requests.request(method, url, headers=header,params=data)
    return(response)

def apiRequestUpdate(call, method, data=""):
    url = "https://bank.demdex.com/v1/{}/".format(call)
    header =  {'Authorization' : 'Bearer {}'.format(token),'accept': 'application/json',"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request(method, url, headers=header,params=data)
    return(response)

def apiTraitsTrend(call, method, data=""):
    url = "https://api.demdex.com/v1/reports/traits-trend".format(call)
    header =  {'Authorization' : 'Bearer {}'.format(token),'accept': '*/*',"Content-Type": "application/json", 'accept-encoding':"Accept-Encoding: gzip, deflate, br"}
    response = requests.request(method, url, headers=header,params=data)
    return(response)
