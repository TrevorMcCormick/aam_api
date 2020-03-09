import requests
import json
import base64 as base64
import pandas as pd
import xlrd
import time
from datetime import datetime, timedelta

from aam_api.helpers.apiError import APIError
from aam_api.helpers.apiRequest import apiRequest
from aam_api.helpers.apiRequest import apiRequestUpdate
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
    def traits_trend(cls,traitId, startDate, endDate, breakdown="day"):
        pattern = "%Y-%m-%d"
        startDate = datetime.strptime(startDate, pattern)
        startDate = int(startDate.timestamp()*1000)
        endDate = datetime.strptime(endDate, pattern)
        endDate = int(endDate.timestamp()*1000)
        data = {"startDate":startDate,
                "endDate":endDate,
                "interval": "1D",
                "metricsType": "DEVICE"}
        response = apiRequest(call="reports/traits-trend/{0}".format(traitId), method="get", data=data)
        status = response.status_code
        if status != 200:
            raise APIError(status)
        else:
            df = pd.DataFrame(response.json())
            df = pd.DataFrame.from_records(df['metrics'])
            count = 0
            for index, row in df.iterrows():
                date = data['startDate'] / 1000
                date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
                date = datetime.strptime(date, "%Y-%m-%d")
                modified_date = str(date + timedelta(days=count))[:-9]
                df.at[index, 'date'] = modified_date
                count += 1
                df = df[["date", "uniques", "populationUniques"]]
            return df
    @classmethod
    def traits_trend_history(cls,traitId,breakdown="day"):
        now = datetime.now()
        pattern = "%Y-%m-%d"
        startDate = Traits.get_one(traitId).at['createTime', 0].strftime("%Y-%m-%d")
        startDate = datetime.strptime(startDate, pattern)
        startDate = int(startDate.timestamp()*1000)
        endDate = now.strftime("%Y-%m=%d")
        endDate = datetime.strptime(endDate, pattern)
        endDate = int(endDate.timestamp()*1000)
        data = {"startDate":startDate,
                "endDate":endDate,
                "interval": "1D",
                "metricsType": "DEVICE"}
        response = apiRequest(call="reports/traits-trend/{0}".format(traitId), method="get", data=data)
        status = response.status_code
        if status != 200:
            raise APIError(status)
        else:
            df = pd.DataFrame(response.json())
            df = pd.DataFrame.from_records(df['metrics'])
            count = 0
            for index, row in df.iterrows():
                date = data['startDate'] / 1000
                date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
                date = datetime.strptime(date, "%Y-%m-%d")
                modified_date = str(date + timedelta(days=count))[:-9]
                df.at[index, 'date'] = modified_date
                count += 1
                df = df[["date", "uniques", "populationUniques"]]
            return df
