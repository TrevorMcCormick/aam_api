import requests
import json
import base64 as base64
import pandas as pd
import xlrd

from aam_api.helpers.apiRequest import apiRequest
from aam_api.helpers.apiError import APIError
from aam_api.core.users import Users

def getUsers(df):
    users = Users.get_many()
    df = pd.merge(df,users.drop('pid', axis=1),left_on="crUID", right_on="uid")
    df.rename(columns={'firstName': 'create_firstName',
                           'lastName': 'create_lastName',
                           'email': 'create_email'}, inplace=True)
    df = df.drop('uid', axis=1)
    df = pd.merge(df,users.drop('pid', axis=1),left_on="upUID", right_on="uid")
    df.rename(columns={'firstName': 'update_firstName',
                           'lastName': 'update_lastName',
                           'email': 'update_email'}, inplace=True)
    df = df.drop('uid', axis=1)
    return(df)
