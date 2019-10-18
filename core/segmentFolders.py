#' SegmentFolders

class SegmentFolders:
    @classmethod
    def get_many(cls):
        data = {}
        response = apiRequest(call="folders/traits", method="get", data=data)
        if response.status_code != 200:
            return('Error getting list of segmentFolders. Adobe message: {0}'.format(response.status_code))
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

#     @classmethod
#     def get_one(cls,
#         folderId,
#         includeSubFolders=None):
#         data = {"includeSubFolders":includeSubFolders}
#         response = apiRequest(call="folders/segments/{0}".format(folderId), method="get")
#         if response.status_code != 200:
#             return('Error getting folder. Adobe message: {0}'.format(response.status_code))
#         else:
#             if includeSubFolders == True:
#                 folders_json = response.json()
#                 folders_flat = flattenJson(folders_json)
#                 df = folders_flat
#                 folderIDs = []
#                 parentFolderIDs = []
#                 paths = []
#                 for k, v in folders_flat.items():
#                     if k.endswith("folderId") == True:
#                         folderIDs.append(v)
#                     elif k.endswith("parentFolderId"):
#                         parentFolderIDs.append(v)
#                     elif k.endswith("path"):
#                         paths.append(v)
#                 df = pd.DataFrame({'folderId':folderIDs, 'parentFolderId':parentFolderIDs, 'path':paths})
#             else:
#                 df = bytesToJson(response.content)
#         return df

    @classmethod
    def search(cls, search, keywords):
        segmentFolders = SegmentFolders.get_many()
        if search=="any":
            result = segmentFolders.path.apply(lambda sentence: any(keyword in sentence for keyword in keywords))
            df = segmentFolders[result]
        elif search=="all":
            result = segmentFolders.path.apply(lambda sentence: all(keyword in sentence for keyword in keywords))
            df = segmentFolders[result]
        return(df)
