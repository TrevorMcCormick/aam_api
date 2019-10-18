class Destinations:
    @classmethod
    def get_many(cls,
            limitCols=None,
            containsSegment=None,
            search=None,
            sortBy=None,
            descending=None,
            page=None,
            pageSize=None,
            includePermissions=None,
            pid=None,
            restrictType=None,
            includeMasterDataSourceIdType=None,
            includeMetrics=None,
            includeAddressableAudienceMetrics=None):
        data = {"containsSegment":containsSegment,
                "search":search,
                "sortBy":sortBy,
                "descending":descending,
                "page":page,
                "pageSize":pageSize,
                "includePermissions":includePermissions,
                "pid":pid,
                "restrictType":restrictType,
                "includeMasterDataSourceIdType":includeMasterDataSourceIdType,
                "includeMetrics":includeMetrics,
                "includeAddressableAudienceMetrics":includeAddressableAudienceMetrics
                }
        response = apiRequest(call="destinations", method="get", data=data)
        if response.status_code != 200:
            return('Error getting list of segments. Adobe message: {0}'.format(response.status_code))
        else:
            df = pd.DataFrame(response.json())
            df['createTime'] = pd.to_datetime(df['createTime'], unit='ms')
            df['updateTime'] = pd.to_datetime(df['updateTime'], unit='ms')
            if limitCols:
                df = df[['name', 'description', 'destinationType',
                     'sid', 'destinationId', 'dataSourceId',
                     'createTime', 'updateTime']]
            return df

    @classmethod
    def get_one(cls,
                did,
                limitCols=True,
                includeMappings=None,
                includeMetrics=None,
                includeMasterDataSourceIdType=None,
                includeAddressableAudienceMetrics=None
               ):
        data = {"includeMappings":includeMappings,
                "includeMetrics":includeMetrics,
                "includeMasterDataSourceIdType":includeMasterDataSourceIdType,
                "includeAddressableAudienceMetrics":includeAddressableAudienceMetrics
               }
        response = apiRequest(call="destinations/{0}".format(str(did)), method="get", data=data)
        if response.status_code != 200:
            message = json.loads(response.content.decode('utf-8'))['message']
            return('Error getting traitId {0}. Adobe message: {1}'.format(sid, message))
        else:
            response_json = response.json()
            response_json.pop('batchConfiguration')
            response_json.pop('dataExportLabels')
            response_json.pop('permissions')
            df = pd.DataFrame(response_json, index=[0])
            df['createTime'] = pd.to_datetime(df['createTime'], unit='ms')
            df['updateTime'] = pd.to_datetime(df['updateTime'], unit='ms')
            if limitCols:
                df = df[['name', 'description', 'destinationType',
                         'destinationId', 'dataSourceId',
                         'createTime', 'updateTime']]
            return df
