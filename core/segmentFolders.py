#' SegmentFolders

class SegmentFolders:
    @classmethod
    def get_many(cls):
            """
                Get multiple AAM SegmentFolders.
                Args:
                    None
                Returns:
                    df of all folderIds, parentFolderIds, and paths to which the AAM API user has READ access.
            """
            data = {}
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
                Get multiple AAM SegmentFolders.
                Args:
                    folderId: (int) Folder ID.
                    includeSubFolders: (bool) Scans subfolders and returns in df.
                Returns:
                    df of one folderId, with optional subfolders, provided the AAM API user has READ access.
            """
            data = {"includeSubFolders":includeSubFolders}
            response = apiRequest(call="folders/segments/{0}/".format(folderId), method="get")
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
            """
                Advanced search through segmentfolders.
                Args:
                    search: (str) "any" matches any of the terms, "all" matches all of the terms.
                    keywords: (list or comma-separated string) Terms to search within Folder path.
                Returns:
                    df of folderIds with matching search, provided the AAM API user has READ access.
            """
            segmentFolders = SegmentFolders.get_many()
            if type(keywords) != list:
                split = keywords.split(",")
                keywords = split
            if search=="any":
                result = segmentFolders.path.apply(lambda sentence: any(keyword in sentence for keyword in keywords))
                df = segmentFolders[result]
            elif search=="all":
                result = segmentFolders.path.apply(lambda sentence: all(keyword in sentence for keyword in keywords))
                df = segmentFolders[result]
            return df
