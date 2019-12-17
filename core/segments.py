#' segments

class Segments:
    @classmethod
    def get_many(cls,
            limitCols=None,
            containsTrait=None,
            folderId=None,
            includePermissions=None,
            permission=None,
            integrationCode=None,
            updatedSince=None,
            dataSourceId=None,
            mergeRuleDataSourceId=None,
            pid=None,
            includeTraitDataSourceIds=None,
            includeMetrics=None):
            """
                Get multiple AAM Segments.
                Args:
                    limitCols: (bool) List of df columns to subset.
                    containsTrait: (int) Trait ID.
                    folderId: (int) Limit segments returned to Folder ID.
                    includePermissions: (bool) includes Permissions column.
                    permission: (str) Filters by permission type; ex: "READ".
                    integrationCode: (str) Filters by integrationCode.
                    updatedSince: (int) Filters by updateTime, by UNIX timestamp.
                    dataSourceId: (int) Filters by Data Source ID.
                    mergeRuleDataSourceId: (int) Filters by mergeRuleDataSourceId.
                    pid: (int) Your AAM enterprise ID.
                    includeTraitDataSourceIds: (bool) Includes includeTraitDataSourceIds column.
                    includeMetrics: (bool) Includes many metrics columns by segment.
                Returns:
                    df of all segments to which the AAM API user has READ access.
            """
            data = {"containsTrait":containsTrait,
                "folderId":folderId,
                "includePermissions":includePermissions,
                "permission":permission,
                "integrationCode":integrationCode,
                "updatedSince":updatedSince,
                "dataSourceId":dataSourceId,
                "mergeRuleDataSourceId":mergeRuleDataSourceId,
                "pid":pid,
                "includeTraitDataSourceIds":includeTraitDataSourceIds,
                "type":type,
                "includeMetrics":includeMetrics
                }
            response = apiRequest(call="segments", method="get", data=data)
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                df = pd.DataFrame(response.json())
                df['createTime'] = pd.to_datetime(df['createTime'], unit='ms')
                df['updateTime'] = pd.to_datetime(df['updateTime'], unit='ms')
                if limitCols:
                    df = df[['name', 'description',
                         'sid', 'folderId', 'dataSourceId',
                         'createTime', 'updateTime']]
                return df

    @classmethod
    def get_one(cls,
                sid,
                limitCols=None,
                includeMetrics=None,
                includeExprTree=None,
                includeTraitDataSourceIds=None,
                includeInUseStatus=None
               ):
            """
               Get multiple AAM Segments.
               Args:
                   sid: (int) Segment ID.
                   limitCols: (bool) List of df columns to subset.
                   includeMetrics: (bool) Includes many metrics columns by segment.
                   includeExprTree: (bool) Includes traits, mappableTraits, codeViewOnly, and expressionTree columns.
                   includeTraitDataSourceIds: (bool) Includes includeTraitDataSourceIds column.
                   includeInUseStatus: (bool) Includes inUse column.
               Returns:
                   Transposed df of one segment to which the AAM API user has READ access.
            """
            data = {"includeMetrics":includeMetrics,
                "includeExprTree":includeExprTree,
                "includeTraitDataSourceIds":includeTraitDataSourceIds,
                "includeInUseStatus":includeInUseStatus
               }
            response = apiRequest(call="segments/{0}".format(str(sid)), method="get", data=data)
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                df = pd.DataFrame.from_dict(response.json(), orient='index')
                df.transpose()
                df.at['createTime', 0] = pd.to_datetime(df.at['createTime', 0], unit='ms')
                df.at['updateTime', 0] = pd.to_datetime(df.at['updateTime', 0], unit='ms')
                if limitCols:
                    df = df.loc[ ['name', 'description', 'sid',
                             'folderId', 'dataSourceId',
                             'createTime', 'updateTime'] , : ]
                return df

### 415 Error
#     @classmethod
#     def create_one(cls,segments):
#         try:
#             segments = toDataFrame(segments)
#         except:
#             print("Failed to transform segments to dataframe.")
#             raise
#         try:
#             req_cols = [
#             'dataSourceId',
#             'integrationCode',
#             'mergeRuleDataSourceId',
#             'name',
#             'description',
#             'segmentRule',
#             'folderId'
#             ]
#             if req_cols != list(segments):
#                 raise ValueError('Segments column names are incorrect')
#         except (ValueError):
#             raise
#         for i in range(0, len(segments)):
#             data = {"dataSourceId": segments.loc[i]['dataSourceId'],
#                    "integrationCode": segments.loc[i]['integrationCode'],
#                    "mergeRuleDataSourceId": segments.loc[i]['mergeRuleDataSourceId'],
#                    "name": segments.loc[i]['name'],
#                    "description": segments.loc[i]['description'],
#                    "segmentRule": segments.loc[i]['segmentRule'],
#                    "folderId": segments.loc[i]['folderId']
#                 }
#             response = apiRequest(call="segments", method="post", data=data)
#             status = response.status_code
#             if status != 201:
#                 raise APIError(status)
#             elif status == 201:
#                 print('Created segment: {0}'.format(segments.iloc[i]['name']))


    @classmethod
    def get_limits(cls):
            """
               Get AAM segments limit.
               Args:
                   None
               Returns:
                   Max number of segments you can create in AAM.
            """
            response = apiRequest(call="segments/limits", method="get")
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                df = bytesToJson(response.content)
                return df.transpose()

    @classmethod
    def delete(cls,segments):
            """
               Delete an AAM segment or segments.
               Args:
                   segments: Excel or csv of segments to delete
               Returns:
                   String indicating which and how many segments were deleted.
            """
            try:
                segments = toDataFrame(segments)
            except:
                print("Failed to transform segments to dataframe.")
                raise
            try:
                req_cols = ['sid', 'name']
                if req_cols != list(segments):
                    raise ValueError("Segment column names are incorrect.")
            except (ValueError):
                raise
            deleted_segments = 0
            for i in range(0, len(segments)):
                data = {"sid":int(segments.loc[i]['sid'])}
                sid = data['sid']
                response = apiRequest(call="segments/{0}/".format(sid), method="delete", data=data)
                status = response.status_code
                if status != 204:
                    raise APIError(status)
                elif status == 204:
                    print('Deleted segments: {0}'.format(segments.iloc[i]['name']))
                    deleted_segments += 1
            return('Deleted {0} segments.'.format(deleted_segments))

    @classmethod
    def search(cls, search, keywords):
            """
                Advanced search through segments.
                Args:
                    search: (str) "any" matches any of the terms, "all" matches all of the terms.
                    keywords: (list or comma-separated string) Terms to search within Folder path.
                Returns:
                    df of segments with matching search, provided the AAM API user has READ access.
            """
            segments = Segments.get_many()
            if type(keywords) != list:
                split = keywords.split(",")
                keywords = split
            if search=="any":
                result = segments.name.apply(lambda sentence: any(keyword in sentence for keyword in keywords))
                df = segments[result]
            elif search=="all":
                result = segments.name.apply(lambda sentence: all(keyword in sentence for keyword in keywords))
                df = segments[result]
            return df
