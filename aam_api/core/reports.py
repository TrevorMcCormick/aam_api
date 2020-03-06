import requests
import json
import base64 as base64
import pandas as pd
import xlrd
import time

from aam_api.helpers.apiError import APIError
from aam_api.helpers.apiRequest import apiRequest
from aam_api.helpers.apiRequest import apiRequestUpdate
from aam_api.helpers.apiRequest import apiTraitsTrend
from aam_api.helpers.bytesToJson import bytesToJson
from aam_api.helpers.flattenJson import flattenJson
from aam_api.helpers.toDataFrame import toDataFrame
from aam_api.helpers.getUsers import getUsers
from aam_api.core.users import Users
from aam_api.helpers.traitSkeleton import traitSkeleton
from aam_api.helpers.inSegments import inSegments
from aam_api.helpers.segmentTraits import segmentTraits
from aam_api.core.segments import Segments
from aam_api.helpers.inSegments import inSegmentsBool
from aam_api.core.client import Client

class Reports:
    @classmethod
    def trait_trend(cls,traitId, startDate, endDate, breakdown="day"):
        pattern = "%Y-%m-%d"
        startDate_epoch = int(time.mktime(time.strptime(startDate, pattern)))
        endDate_epoch = int(time.mktime(time.strptime(endDate, pattern)))
        data = {"startDate":startDate_epoch,
                "endDate":endDate_epoch,
                "interval": "1D",
                "metricsType": "DEVICE"}
        response = apiReport(call="traits-trend/{0}".format(traitId), method="get", data=data)
        status = response.status_code
        if status != 200:
            raise APIError(status)
        else:
            df = pd.DataFrame(response.json())
            return df
