#' getTraits

class Traits:
    @classmethod
    def get_many(cls,
            limitcols=True,
            excludeRule=False,
            includeMetrics=True,
            restrictType=None,
            usesModel=None,
            permission=None,
            includePermissions=None,
            categoryId=None,
            folderId=None,
            integrationCode=None,
            dataSourceId=None,
            pid=None,
            includeTraitsForAvailableFeed=None,
            type=None,
            includeDetails=None,
            backfillStatus=None,
            currentMonthTraitsWithBackfillOnly=None
            ):
        data = {"excludeRule":excludeRule,
                "includeMetrics":includeMetrics,
                "restrictType":restrictType,
                "usesModel":usesModel,
                "permission":permission,
                "includePermissions":includePermissions,
                "categoryId":categoryId,
                "folderId":folderId,
                "integrationCode":integrationCode,
                "dataSourceId":dataSourceId,
                "pid":pid,
                "includeTraitsForAvailableFeed":includeTraitsForAvailableFeed,
                "type":type,
                "includeDetails":includeDetails,
                "backfillStatus":backfillStatus,
                "currentMonthTraitsWithBackfillOnly":currentMonthTraitsWithBackfillOnly
                }
        response = apiRequest(call="traits", method="get", data=data)
        if response.status_code != 200:
            return('Error getting list of traitIds. Adobe message: {0}'.format(response.status_code))
        else:
            df = pd.DataFrame(response.json())
            df['createTime'] = pd.to_datetime(df['createTime'], unit='ms')
            df['updateTime'] = pd.to_datetime(df['updateTime'], unit='ms')
            if limitcols:
                df = df[['name', 'description', 'traitType',
                         'sid', 'folderId', 'dataSourceId',
                         'createTime', 'updateTime']]
            return df

    @classmethod
    def get_one(cls,
                sid,
                limitCols=True,
                excludeRule=None,
                includeExprTree=None,
                includeSegmentTestGroupIds=None,
                includeMetrics=None):
        data = {"excludeRule":excludeRule,
                "includeExprTree":includeExprTree,
                "includeSegmentTestGroupIds":includeSegmentTestGroupIds,
                "includeMetrics":includeMetrics
               }
        response = apiRequest(call="traits/{0}".format(str(sid)), method="get", data=data)
        if response.status_code != 200:
            message = json.loads(response.content.decode('utf-8'))['message']
            return('Error getting traitId {0}. Adobe message: {1}'.format(sid, message))
        else:
            df = pd.DataFrame(response.json())
            df['createTime'] = pd.to_datetime(df['createTime'], unit='ms')
            df['updateTime'] = pd.to_datetime(df['updateTime'], unit='ms')
            df = df.head(1)
            if limitCols:
                df = df[['name', 'description', 'traitType',
                         'sid', 'folderId', 'dataSourceId',
                         'createTime', 'updateTime']]
            return df

    @classmethod
    def get_limits(cls):
        response = apiRequest(call="traits/limits", method="get")
        df = bytesToJson(response.content)
        return df

    @classmethod
    def create(cls,traits):
        if type(traits) != pd.core.frame.DataFrame:
            traits = toDataFrame(traits)
        if type(traits) == pd.core.frame.DataFrame:
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
                header =  {'Authorization' : 'Bearer {}'.format(token),'accept': 'application/json',"Content-Type": "application/json"}
                response = requests.post('https://api.demdex.com/v1/traits/', headers=header, data=data)
                #figure out why line below does not work
                #response = apiRequest(call="traits", method="post", data=data)
                status = response.status_code
                if status == 201:
                    print('Created trait: {0}'.format(traits.iloc[i]['name']))
                    successful_traits += 1
                elif status == 400:
                    print("Bad Request")
                elif status == 403:
                    print("Forbidden")
                elif status == 409:
                    print("Conflict")
            return('Created {0} traits.'.format(successful_traits))
        else:
            print('Wrong data type. Please insert a df or upload an excel file with the following fields to create a trait:')
            d = {"name": ["trait1", "trait2", "trait3"],
                 "traitType": ["RULE_BASED_TRAIT", "RULE_BASED_TRAIT", "RULE_BASED_TRAIT"],
                 "comments": ['comment1', 'comment2', 'comment3'],
                 "description": ['description1', 'description2', 'description3'],
                 "folderId": ['1234', '2345', '3456'],
                 "dataSourceId": ['1010', '1010', '1010'],
                 "ttl": [120, 120, 120]}
            df = pd.DataFrame(data=d)
            print(df)

    @classmethod
    def delete(cls,traits):
        if type(traits) != pd.core.frame.DataFrame:
            traits = toDataFrame(traits)
        if type(traits) == pd.core.frame.DataFrame:
            deleted_traits = 0
            for i in range(0, len(traits)):
                data = {"sid":int(traits.loc[i]['sid']),
                       "name":traits.loc[i]['name']}
                sid = data['sid']
                response = apiRequest(call="traits/{0}".format(sid), method="delete", data=data)
                status = response.status_code
                if status == 204:
                    print('Deleted trait: {0}'.format(traits.iloc[i]['name']))
                    deleted_traits += 1
                elif status == 400:
                    print("Bad Request")
                elif status == 403:
                    print("Forbidden")
                elif status == 404:
                    print("Trait not found")
            return('Deleted {0} traits.'.format(deleted_traits))
        else:
            print('Wronge data type. Please insert a df with name and sid to delete. Example:')
            d = {"name": ["trait1", "trait2", "trait3"], "sid": ["1234", "2345", "3456"]}
            df = pd.DataFrame(data=d)
            print(df)

    @classmethod
    def search(cls, column, type, keywords):
        df = Traits.get_many()
        filtered_df = search(df, column, type, keywords)
        return(filtered_df)
