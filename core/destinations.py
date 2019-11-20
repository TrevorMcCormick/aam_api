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

    @classmethod
    def create_one(cls,destinations):
        if type(destinations) != pd.core.frame.DataFrame:
            destinations = toDataFrame(destinations)
        if type(destinations) == pd.core.frame.DataFrame:
            successful_destinations = 0
        for i in range(0, len(segments)):
            data = {"mappingAutoFiller": segments.loc[i]['name'],
                   "endDate": segments.loc[i]['name'],
                   "mapAllSegments": segments.loc[i]['name'],
                   "description": segments.loc[i]['name'],
                   "devicePlatform": segments.loc[i]['name'],
                   "destinationId": segments.loc[i]['name'],
                   "dataExportLabels": segments.loc[i]['name'],
                   "maxMappings": segments.loc[i]['name']0,
                   "mappings": segments.loc[i]['name'],
                   "dataSourceId": segments.loc[i]['name'],
                   "name": segments.loc[i]['name'],
                   "destinationType": segments.loc[i]['name'],
                   "startDate": segments.loc[i]['name']
                }
            response = apiRequest(call="destinations", method="post", data=data)
            status = response.status_code
            if status == 201:
                print('Created segment: {0}'.format(destinations.iloc[i]['name']))
                successful_destinations += 1
            elif status == 400:
                print("Bad Request")
            elif status == 403:
                print("Forbidden")
            elif status == 409:
                print("Conflict")
            else:
                print(status)
            return('Created {0} destinations.'.format(successful_destinations))
        # else:
        #     print('Wrong data type. Please insert a df or upload an excel file with the following fields to create a destinations:')
        #     d = {"name": ["segment1", "segment2", "segment3"],
        #         "description": ['description1', 'description2', 'description3'],
        #         "folderId": ['1234', '2345', '3456'],
        #         "integrationCode": ['seg-abcd', 'seg-abcde', 'seg-123'],
        #         "segmentRule": ["(123T AND 456T)", "(234T AND 456T)", "(345T AND 456T)"],
        #          "dataSourceId": ['1010', '1010', '1010']}
        #     df = pd.DataFrame(data=d)
        #     print(df)
