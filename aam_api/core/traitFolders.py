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

class TraitFolders:
    @classmethod
    def get_many(cls,
            includeThirdParty=None,
            dataSourceId=None):
            """
                Get multiple AAM TraitFolders.
                Args:
                    includeThirdParty: (bool) Includes 3rd Party TraitFolders (defaults True).
                    dataSourceId: (int) Filter TraitFolders by Data Source ID.
                Returns:
                    df of all folderIds, parentFolderIds, and paths to which the AAM API user has READ access.
            """
            data = {"includeThirdParty":includeThirdParty,
                "dataSourceId":dataSourceId}
            response = apiRequest(call="folders/traits", method="get", data=data)
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                folders_json = response.json()
                folders_flat = flattenJson(folders_json)
                df = folders_flat
                folderIDs = []
                parentFolderIDs = []
                paths = []
                for k, v in folders_flat.items():
                    if k.endswith("folderId") == True:
                        folderIDs.append(v)
                    elif k.endswith("parentFolderId"):
                        parentFolderIDs.append(v)
                    elif k.endswith("path"):
                        paths.append(v)
                df = pd.DataFrame({'folderId':folderIDs, 'parentFolderId':parentFolderIDs, 'path':paths})
                return df

    @classmethod
    def get_one(cls,
        folderId,
        includeSubFolders=None):
            """
                Get one AAM TraitFolder.
                Args:
                    includeSubFolders: (bool) Scans subfolders and returns in df.
                Returns:
                    df of one folderId, with optional subfolders, provided the AAM API user has READ access.
            """
            data = {"includeSubFolders":includeSubFolders}
            response = apiRequest(call="folders/traits/{0}".format(folderId), method="get", data=data)
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                if includeSubFolders == True:
                    folders_json = response.json()
                    folders_flat = flattenJson(folders_json)
                    df = folders_flat
                    folderIDs = []
                    parentFolderIDs = []
                    paths = []
                    for k, v in folders_flat.items():
                        if k.endswith("folderId") == True:
                            folderIDs.append(v)
                        elif k.endswith("parentFolderId"):
                            parentFolderIDs.append(v)
                        elif k.endswith("path"):
                            paths.append(v)
                    df = pd.DataFrame({'folderId':folderIDs, 'parentFolderId':parentFolderIDs, 'path':paths})
                else:
                    df = bytesToJson(response.content)
            return df

    @classmethod
    def search(cls, search, keywords):
        traitFolders = TraitFolders.get_many()
        if type(keywords) != list:
            split = keywords.split(",")
            keywords = split
        if search=="any":
            result = traitFolders.path.apply(lambda sentence: any(keyword in sentence for keyword in keywords))
            df = traitFolders[result]
        elif search=="all":
            result = traitFolders.path.apply(lambda sentence: all(keyword in sentence for keyword in keywords))
            df = traitFolders[result]
        return df
