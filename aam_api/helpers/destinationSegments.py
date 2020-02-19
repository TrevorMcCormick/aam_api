import requests
import json
import base64 as base64
import pandas as pd
import xlrd

from aam_api.helpers.apiRequest import apiRequest
from aam_api.helpers.apiError import APIError

def segmentsMappedToDestination(destinationId):
        """
        Get all segments mapped to an AAM Destination.
        Args:
            destinationId: AAM Destination ID.
        Returns:
            df with rows of each segment and columns of one destination.
        """
        data = {"destinationId":destinationId}
        response = apiRequest(call="destinations/{0}/mappings".format(destinationId), method="get", data=data)
        status = response.status_code
        if status != 200:
            if status == 404:
                lst = None
            else:
                raise APIError(status)
        else:
            df = pd.DataFrame(response.json())
            try:
                df = df[["sid"]].values.tolist()
                lst = [y for x in df for y in x]
            except:
                lst = None
            return lst
