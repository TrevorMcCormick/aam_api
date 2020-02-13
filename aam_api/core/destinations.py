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
from aam_api.helpers.getUsers import getUsers
from aam_api.core.users import Users
from aam_api.helpers.destinationSegments import segmentsMappedToDestination

class Destinations:
    @classmethod
    def get_many(cls,
            limitCols=None,
            containsSegment=None,
            search=None,
            sortBy=None,
            descending=None,
            includePermissions=None,
            pid=None,
            restrictType=None,
            includeMasterDataSourceIdType=None,
            includeMetrics=None,
            includeUsers=None,
            includeMappings=None):
            """
                Get multiple AAM Destinations.
                Args:
                    limitCols: (bool) List of df columns to subset.
                    containsSegment: (int) Segment ID.
                    search: (str) Search name & description.
                    sortBy: (str) Sort asc by column name.
                    descending: (bool) sortBy column desc.
                    includePermissions: (bool) includes Permissions column.
                    pid: (int) Your AAM enterprise ID.
                    restrictType: (str) Filter by destinationType column.
                    includeMasterDataSourceIdType: (bool) True includes masterDataSource columns.
                    includeMetrics: (bool) Includes includes AddressableAudienceMetrics column.
                    includeMappings: (bool) Includes segment mappings to destinationId.
                Returns:
                    df of all destinations to which the AAM API user has READ access.
            """
            data = {"containsSegment":containsSegment,
                "search":search,
                "sortBy":sortBy,
                "descending":descending,
                "includePermissions":includePermissions,
                "pid":pid,
                "restrictType":restrictType,
                "includeMasterDataSourceIdType":includeMasterDataSourceIdType,
                "includeMetrics":includeMetrics
                }
            response = apiRequest(call="destinations", method="get", data=data)
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                df = pd.DataFrame(response.json())
                df['createTime'] = pd.to_datetime(df['createTime'], unit='ms')
                df['updateTime'] = pd.to_datetime(df['updateTime'], unit='ms')
                if includeMappings:
                    df['segmentMappings'] = None
                    try:
                        for d in range(0, len(df)):
                            df.iloc[d]['segmentMappings'] = segmentsMappedToDestination(df.iloc[d]['destinationId'])
                    except:
                        pass
                if includeUsers:
                    df = getUsers(df)
                if limitCols:
                    df = df[['name', 'description', 'destinationType',
                         'sid', 'destinationId', 'dataSourceId',
                         'createTime', 'updateTime']]
                return df

    @classmethod
    def get_one(cls,
                destinationId,
                limitCols=None,
                includeMappings=None,
                includeMetrics=None,
                includeMasterDataSourceIdType=None,
                includeUsers=None
               ):
            """
                Get one AAM Destination.
                Args:
                    destinationId: (int) Destination ID.
                    limitCols: (bool) List of df columns to subset.
                    includeMappings: (bool) includes mappings column.
                    includeMetrics: (bool) includes includes AddressableAudienceMetrics column.
                    includeMasterDataSourceIdType: (bool) includes masterDataSource columns.
                Returns:
                    Transposed df of one destination, provided the AAM API user has READ access to it.
            """
            data = {"includeMappings":includeMappings,
                "includeMetrics":includeMetrics,
                "includeMasterDataSourceIdType":includeMasterDataSourceIdType,
               }
            response = apiRequest(call="destinations/{0}".format(str(destinationId)), method="get", data=data)
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                df = pd.DataFrame.from_dict(response.json(), orient='index')
                df.transpose()
                df.at['createTime', 0] = pd.to_datetime(df.at['createTime', 0], unit='ms')
                df.at['updateTime', 0] = pd.to_datetime(df.at['updateTime', 0], unit='ms')
                if includeMappings:
                    df['segmentMappings'] = None
                    try:
                        for d in len(0, range(df)):
                            df.iloc[d]['segmentMappings'] = segmentsMappedToDestination(df.iloc[d]['destinationId'])
                    except:
                        pass
                if includeUsers:
                    df = getUsers(df)
                if limitCols:
                    df = df.loc[ ['name', 'description', 'destinationType',
                             'destinationId', 'dataSourceId',
                             'createTime', 'updateTime'] , : ]
                return df

    @classmethod
    def create(cls,destinations):
            """
                Create many AAM Destinations.
                Args:
                    destinations: (Excel or csv) List of destinations to create.
                Returns:
                    String with segment create success.
            """
            try:
                destinations = toDataFrame(destinations)
            except:
                print("Failed to transform destinations to dataframe.")
                raise
            try:
                req_cols = [
                'name',
                'description',
                'destinationType',
                #'mapAllSegments',
                #'mappingAutoFiller',
                #'dataExportLabels',
                #'devicePlatform',
                #'urlFormatString',
                #'secureUrlFormatString'
                ]
                if req_cols != list(destinations):
                    raise ValueError('Destinations column names are incorrect')
            except (ValueError):
                raise
            for i in range(0, len(destinations)):
                data = {
                       "name": destinations.loc[i]['name'],
                       "description": destinations.loc[i]['description'],
                       "destinationType": destinations.loc[i]['destinationType'],
                       #"mapAllSegments": destinations.loc[i]['mapAllSegments'],
                       #"mappingAutoFiller": destinations.loc[i]['mappingAutoFiller'],
                       #"dataExportLabels": destinations.loc[i]['dataExportLabels'],
                       #"devicePlatform": destinations.loc[i]['devicePlatform'],
                       #"serializationEnabled": destinations.loc[i]['serializationEnabled']
                    }
                data = json.dumps(data)
                header =  {'Authorization' : 'Bearer {}'.format(token),'accept': 'application/json',"Content-Type": "application/json"}
                response = requests.post('https://api.demdex.com/v1/destinations/', headers=header, data=data)
                status = response.status_code
                if status != 201:
                    raise APIError(status)
                elif status == 201:
                    print('Created destination: {0}'.format(destinations.iloc[i]['name']))
