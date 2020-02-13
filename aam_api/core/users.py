import requests
import json
import base64 as base64
import pandas as pd
import xlrd

from aam_api.helpers.apiError import APIError
from aam_api.helpers.apiRequest import apiRequest
from aam_api.helpers.bytesToJson import bytesToJson
from aam_api.helpers.flattenJson import flattenJson
from aam_api.helpers.toDataFrame import toDataFrame

class Users:
    @classmethod
    def get_many(cls,
            ):
            """
                Get AAM Users
                Args:
                Returns:
                    df of pid, uid, firstname, lastname, and email address
            """
            data = {}
            response = apiRequest(call="users", method="get", data=data)
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                df = pd.DataFrame(response.json())
            return df
