#' traitFolders

class TraitFolders:
    @classmethod
    def get_many(cls,
            includeThirdParty=None,
            includeFoldersForAvailableFeed=None,
            dataSourceId=None):
        data = {"includeThirdParty":includeThirdParty,
                "includeFoldersForAvailableFeed":includeFoldersForAvailableFeed,
                "dataSourceId":dataSourceId}
        response = apiRequest(call="folders/traits", method="get", data=data)
        if response.status_code != 200:
            return('Error getting list of traitFolders. Adobe message: {0}'.format(response.status_code))
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
        data = {"includeSubFolders":includeSubFolders}
        response = apiRequest(call="folders/traits/{0}".format(folderId), method="get", data=data)
        if response.status_code != 200:
            return('Error getting folder. Adobe message: {0}'.format(response.status_code))
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
    def search(cls, column, type, keywords):
        df = TraitFolders.get_many()
        filtered_df = search(df, column, type, keywords)
        return(filtered_df)
