#' segments

class Segments:
    @classmethod
    def get_many(cls,
            limitCols=None,
            containsTrait=None,
            # below parameter does not work; results in 404
            #containsTraitFromDataSource=True,
            folderId=None,
            includePermissions=None,
            permission=None,
            integrationCode=None,
            includeInUseStatus=None,
            updatedSince=None,
            status=None,
            dataSourceId=None,
            mergeRuleDataSourceId=None,
            pid=None,
            includeTraitDataSourceIds=None,
            includeMetrics=None,
            includeAddressableAudienceMetrics=None):
        data = {"containsTrait":containsTrait,
                #"containsTraitFromDataSource":containsTraitFromDataSource,
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
                "includeMetrics":includeMetrics,
                "includeAddressableAudienceMetrics":includeAddressableAudienceMetrics
                }
        response = apiRequest(call="segments", method="get", data=data)
        if response.status_code != 200:
            return('Error getting list of segments. Adobe message: {0}'.format(response.status_code))
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
                limitCols=True,
                includeMetrics=None,
                includeTraitMetrics=None,
                includeAddressableAudienceMetrics=None,
                includeSegmentTestGroupIds=None,
                includeExprTree=None,
                includeTraitDataSourceIds=None,
                #includeInUseStatus=None
               ):
        data = {"includeMetrics":includeMetrics,
                "includeTraitMetrics":includeTraitMetrics,
                "includeAddressableAudienceMetrics":includeAddressableAudienceMetrics,
                "includeSegmentTestGroupIds":includeSegmentTestGroupIds,
                "includeExprTree":includeExprTree,
                "includeTraitDataSourceIds":includeTraitDataSourceIds,
                #"includeInUseStatus":includeInUseStatus
               }
        response = apiRequest(call="segments/{0}".format(str(sid)), method="get", data=data)
        if response.status_code != 200:
            message = json.loads(response.content.decode('utf-8'))['message']
            return('Error getting traitId {0}. Adobe message: {1}'.format(sid, message))
        else:
            df = pd.DataFrame(response.json())
            df['createTime'] = pd.to_datetime(df['createTime'], unit='ms')
            df['updateTime'] = pd.to_datetime(df['updateTime'], unit='ms')
            df = df.head(1)
            if limitCols:
                df = df[['name', 'description',
                         'sid', 'folderId', 'dataSourceId',
                         'createTime', 'updateTime']]
            return df

    @classmethod
    def get_one_destinations(cls,
                             sid,
                             includeInUseStatus=True):
        data = {
                "includeInUseStatus":includeInUseStatus
               }
        response = apiRequest(call="segments/{0}".format(str(sid)), method="get", data=data)
        response_json = json.loads(response.content.decode('utf-8'))
        if response.status_code != 200:
            message = json.loads(response.content.decode('utf-8'))['message']
            return('Error getting segmentId {0}. Adobe message: {1}'.format(sid, message))
        else:
            destinations = response_json['mappedEntities']['destinations']
            destinations_dfs = []
            for i in destinations:
                destination_info = Destinations.get_one(i)
                destinations_dfs.append(destination_info)
            result = pd.concat(destinations_dfs)
            return result

# create class getting 415 error
#     @classmethod
#     def create(cls,segments):
#         if type(segments) != pd.core.frame.DataFrame:
#             segments = toDataFrame(segments)
#         if type(segments) == pd.core.frame.DataFrame:
#             successful_segments = 0
#             for i in range(0, len(segments)):
#                 data = {"name":segments.loc[i]['name'],
#                         "description":segments.loc[i]['description'],
#                         "folderId":int(segments.loc[i]['folderId']),
#                         #"integrationCode":segments.loc[i]['integrationCode'],
#                         #"mergeRuleDataSourceId": int(segments.loc[i]['mergeRuleDataSourceId']),
#                         "segmentRule":segments.loc[i]['segmentRule'],
#                         "dataSourceId":int(segments.loc[i]['dataSourceId'])
#                         }
#                 response = apiRequest(call="segments", method="post", data=data)
#                 status = response.status_code
#                 if status == 201:
#                     print('Created segment: {0}'.format(traits.iloc[i]['name']))
#                     successful_segments += 1
#                 elif status == 400:
#                     print("Bad Request")
#                 elif status == 403:
#                     print("Forbidden")
#                 elif status == 409:
#                     print("Conflict")
#                 else:
#                     print(status)
#             return('Created {0} segments.'.format(successful_segments))
#         else:
#             print('Wrong data type. Please insert a df or upload an excel file with the following fields to create a segment:')
#             d = {"name": ["segment1", "segment2", "segment3"],
#                 "description": ['description1', 'description2', 'description3'],
#                 "folderId": ['1234', '2345', '3456'],
#                 "integrationCode": ['seg-abcd', 'seg-abcde', 'seg-123'],
#                 "segmentRule": ["(123T AND 456T)", "(234T AND 456T)", "(345T AND 456T)"],
#                  "dataSourceId": ['1010', '1010', '1010']}
#             df = pd.DataFrame(data=d)
#             print(df)

    @classmethod
    def get_limits(cls):
        response = apiRequest(call="segments/limits", method="get")
        df = bytesToJson(response.content)
        return df

    @classmethod
    def delete(cls,segments):
        if type(segments) != pd.core.frame.DataFrame:
            segments = toDataFrame(segments)
        if type(segments) == pd.core.frame.DataFrame:
            deleted_segments = 0
            for i in range(0, len(segments)):
                data = {"sid":int(segments.loc[i]['sid']),
                       "name":segments.loc[i]['name']}
                sid = data['sid']
                response = apiRequest(call="segments/{0}".format(sid), method="delete", data=data)
                status = response.status_code
                if status == 204:
                    print('Deleted segments: {0}'.format(segments.iloc[i]['name']))
                    deleted_segments += 1
                elif status == 400:
                    print("Bad Request")
                elif status == 403:
                    print("Forbidden")
                elif status == 404:
                    print("Trait not found")
            return('Deleted {0} traits.'.format(deleted_segments))
        else:
            print('Wronge data type. Please insert a df with name and sid to delete. Example:')
            d = {"name": ["segment1", "segment2", "segment3"], "sid": ["1234", "2345", "3456"]}
            df = pd.DataFrame(data=d)
            print(df)

    @classmethod
    def search(cls, search, keywords):
        segments = Segments.get_many()
        if search=="any":
            result = segments['name'].apply(lambda sentence: any(keyword in sentence for keyword in keywords))
            df = segments[result]
        elif search=="all":
            result = segments['name'].apply(lambda sentence: all(keyword in sentence for keyword in keywords))
            df = segments[result]
        return(df)
