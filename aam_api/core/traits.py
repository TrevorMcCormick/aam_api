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
from aam_api.helpers.traitSkeleton import traitSkeleton
from aam_api.helpers.inSegments import inSegments
from aam_api.helpers.segmentTraits import segmentTraits
from aam_api.core.segments import Segments
from aam_api.helpers.inSegments import inSegmentsBool

class Traits:
    @classmethod
    def get_many(cls,
            limitcols=None,
            includeMetrics=None,
            restrictType=None,
            usesModel=None,
            permission=None,
            includePermissions=None,
            categoryId=None,
            folderId=None,
            integrationCode=None,
            dataSourceId=None,
            pid=None,
            type=None,
            includeDetails=None,
            includeUsers=None,
            includeTraitSkeleton=None,
            includeSegmentsBool=None
            ):
            """
                Get AAM Traits
                Args:
                    limitCols: (bool) List of df columns to subset.
                    includeMetrics: (bool) Includes many metrics columns by trait.
                    restrictType: (str) Filter by one or more trait type values.
                    usesModel: (int) Filter by algorithmic model ID.
                    permission: (str) Filter by permission type.
                    includePermissions: (bool) Include permissions column.
                    categoryId: (int) Filter by trait categories; ex: Automotive.
                    folderId: (int) Filter by Folder ID.
                    integrationCode: (str) Filter by integration code.
                    dataSourceId: (id) Filter by data source ID.
                    pid: (int) Your AAM enterprise ID.
                    type: (int) Filter by specific trait type value.
                    includeDetails: (bool) Includes various detail columns such as ttl and traitRule.
                    includeUsers: (bool) Translates UIDs to firstname, lastname, and email address.
                    includeTraitSkeleton: (bool) Includes list of trait IDs that make up a trait.
                    includeSegmentsBool: (bool) Includes column indicating if trait is part of a segment.
                Returns:
                    df of traits to which the AAM API user has READ access.
            """
            data = {"includeMetrics":includeMetrics,
                    "restrictType":restrictType,
                    "usesModel":usesModel,
                    "permission":permission,
                    "includePermissions":includePermissions,
                    "categoryId":categoryId,
                    "folderId":folderId,
                    "integrationCode":integrationCode,
                    "dataSourceId":dataSourceId,
                    "pid":pid,
                    "type":type,
                    "includeDetails":includeDetails,
                    "includeUsers": includeUsers
                    }
            response = apiRequest(call="traits", method="get", data=data)
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                df = pd.DataFrame(response.json())
                df['createTime'] = pd.to_datetime(df['createTime'], unit='ms')
                df['updateTime'] = pd.to_datetime(df['updateTime'], unit='ms')
                if includeUsers:
                    df = getUsers(df)
                if includeTraitSkeleton:
                    df = traitSkeleton(df)
                if includeSegmentsBool:
                    segments = Segments.get_many()
                    segments = segmentTraits(segments)
                    df = inSegmentsBool(df, segments)
                if limitcols:
                    df = df[['name', 'description', 'traitType',
                             'sid', 'folderId', 'dataSourceId',
                             'createTime', 'updateTime']]
                return df

    @classmethod
    def get_one(cls,
                sid,
                limitCols=None,
                includeExprTree=None,
                includeMetrics=None,
                includeUsers=None,
                includeTraitSkeleton=None,
                includeInSegments=None):
            """
                Get AAM Traits
                Args:
                    limitCols: (bool) List of df columns to subset.
                    includeExprTree: (bool) Includes traits, mappableTraits, codeViewOnly, and expressionTree columns.
                    includeMetrics: (bool) Includes many metrics columns by trait.
                    includeUsers: (bool) Translates UIDs to firstname, lastname, and email address.
                    includeTraitSkeleton: (bool) Includes list of trait IDs that make up a trait.
                    includeInSegments: (bool) Includes segments trait ID is included in.
                Returns:
                    Transposed df of one trait to which the AAM API user has READ access.
            """
            data = {"includeExprTree":includeExprTree,
                "includeMetrics":includeMetrics
               }
            response = apiRequest(call="traits/{0}".format(str(sid)), method="get", data=data)
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                df = pd.DataFrame.from_dict(response.json(), orient='index')
                df.transpose()
                df.at['createTime', 0] = pd.to_datetime(df.at['createTime', 0], unit='ms')
                df.at['updateTime', 0] = pd.to_datetime(df.at['updateTime', 0], unit='ms')
                if includeUsers:
                    df = getUsers(df)
                if includeTraitSkeleton:
                    df = traitSkeleton(df)
                if includeInSegments:
                    df['inSegments'] = None
                    for index, row in df.iterrows():
                        df.at[index, "inSegments"] = inSegments(df['sid'])
                if limitCols:
                    df = df.loc[ ['name', 'description', 'sid',
                             'folderId', 'dataSourceId',
                             'createTime', 'updateTime'] , : ]
                return df

    @classmethod
    def get_limits(cls):
            """
               Get AAM traits limit.
               Args:
                   None
               Returns:
                   Max number of traits you can create in AAM.
            """
            response = apiRequest(call="traits/limits", method="get")
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                df = bytesToJson(response.content)
                return df.transpose()

    @classmethod
    def create(cls,traits):
            """
               Creates AAM Trait.
               Args:
                   traits: (Excel or csv) List of traits to create.
               Returns:
                   String with trait create success and # of traits created.
            """
            try:
                traits = toDataFrame(traits)
            except:
                print("Failed to transform traits to dataframe.")
                raise
            try:
                req_cols = [
                    'name',
                    'traitType',
                    'dataSourceId',
                    'traitRule',
                    'folderId',
                    'ttl',
                    'description',
                    'comments'
                ]
                if req_cols != list(traits):
                    raise ValueError('Traits column names are incorrect')
            except (ValueError):
                raise
            successful_traits = 0
            for i in range(0, len(traits)):
                try:
                    comments = traits.loc[i]['comments']
                except:
                    comments = None
                try:
                    description = traits.loc[i]['description']
                except:
                    description = None
                try:
                    ttl = int(traits.loc[i]['ttl'])
                except:
                    ttl = 120
                data = {"comments":comments,
                        "description":description,
                        "ttl":ttl,
                        "folderId":int(traits.loc[i]['folderId']),
                        "traitRule":traits.loc[i]['traitRule'],
                        "dataSourceId":int(traits.loc[i]['dataSourceId']),
                        "traitType":traits.loc[i]['traitType'],
                        "name":traits.loc[i]['name']}
                data = json.dumps(data)
                #quick fix for line 193
                ########
                global token
                try:
                    token = Client.from_json("aam_credentials.json").response.json()['access_token']
                except:
                    path = input("Path to aam credentials:  ")
                    try:
                        token = Client.from_json(path).response.json()['access_token']
                    except:
                        raise InputError("Invalid Path", "Credentials are invalid")
                #######
                header =  {'Authorization' : 'Bearer {}'.format(token),'accept': 'application/json',"Content-Type": "application/json"}
                response = requests.post('https://api.demdex.com/v1/traits/', headers=header, data=data)
                #figure out why line below does not work
                #response = apiRequest(call="traits", method="post", data=data)
                status = response.status_code
                if status != 201:
                    raise APIError(status)
                elif status == 201:
                    print('Created trait: {0}'.format(traits.iloc[i]['name']))
                    successful_traits += 1
            return('Created {0} traits.'.format(successful_traits))

    @classmethod
    def delete(cls,traits):
            """
               Deletes AAM Trait.
               Args:
                   traits: (Excel or csv) List of traits to delete.
               Returns:
                   String with trait create success and # of traits created.
            """
            try:
                traits = toDataFrame(traits)
            except:
                print("Failed to transform traits to dataframe.")
                raise
            try:
                req_cols = ['sid', 'name']
                if req_cols != list(traits):
                    raise ValueError("Trait column names are incorrect.")
            except (ValueError):
                raise
            deleted_traits = 0
            for i in range(0, len(traits)):
                data = {"sid":int(traits.loc[i]['sid'])}
                sid = data['sid']
                response = apiRequest(call="traits/{0}".format(sid), method="delete", data=data)
                status = response.status_code
                if status != 204:
                    raise APIError(status)
                elif status == 204:
                    deleted_traits += 1
            return('Deleted {0} traits.'.format(deleted_traits))

    @classmethod
    def search(cls, search, keywords):
            """
                Advanced search through traits.
                Args:
                    search: (str) "any" matches any of the terms, "all" matches all of the terms.
                    keywords: (list or comma-separated string) Terms to search within Folder path.
                Returns:
                    df of traits with matching search, provided the AAM API user has READ access.
            """
            traits = Traits.get_many()
            if type(keywords) != list:
                split = keywords.split(",")
                keywords = split
            if search=="any":
                result = traits.name.apply(lambda sentence: any(keyword in sentence for keyword in keywords))
                df = segments[result]
            elif search=="all":
                result = traits.name.apply(lambda sentence: all(keyword in sentence for keyword in keywords))
                df = traits[result]
            return df
    @classmethod
    def update(cls,traits):
            """
               Updates AAM Trait.
               Args:
                   traits: (Excel or csv) List of traits to update.
               Returns:
                   String with trait update success and # of traits updated.
            """
            try:
                traits = toDataFrame(traits)
            except:
                print("Failed to transform traits to dataframe.")
                raise
            if 'sid' not in list(traits):
                raise ValueError('Traits column names are incorrect')
            updates = traits.drop('sid', 1)
            successful_traits = 0
            for i in range(0, len(updates)):
                data = updates.iloc[i].to_dict()
                data = json.dumps(data)
                sid = traits.iloc[i]['sid']
                response = apiRequest(call="traits/{}".format(sid), method="put", data=data)
                status = response.status_code
                if status != 200:
                    raise APIError(status)
                elif status == 200:
                    print('Updated trait: {0}'.format(sid))
                    successful_traits += 1
            return('Updated {0} traits.'.format(successful_traits))
