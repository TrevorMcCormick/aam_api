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
