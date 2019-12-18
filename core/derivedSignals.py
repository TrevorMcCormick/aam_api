#' derivedSignals

class DerivedSignals:
    @classmethod
    def get_many(cls,
            limitcols=None,
            search=None,
            sortBy=None,
            descending=None
            ):
            """
                Get AAM Derived Signals
                Args:
                    limitCols: (bool) List of df columns to subset.
                    search: (str) Search any column.
                    sortBy: (str) Sort asc by column name.
                    descending: (int) sortBy column desc.
                Returns:
                    df of derived signals to which the AAM API user has READ access.
            """
            data = {"search":search,
                    "sortBy":sortBy,
                    "descending":descending
                    }
            response = apiRequest(call="signals/derived", method="get", data=data)
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                df = pd.DataFrame(response.json())
                df['createTime'] = pd.to_datetime(df['createTime'], unit='ms')
                df['updateTime'] = pd.to_datetime(df['updateTime'], unit='ms')
                if limitcols:
                    df = df[['derivedSignalId', 'sourceKey', 'sourceValue',
                             'targetKey', 'targetValue',
                             'createTime', 'updateTime']]
                return df

    @classmethod
    def create(cls,derivedSignals):
            """
               Creates AAM Derived Signal.
               Args:
                   derivedSignals: (Excel or csv) List of Derived Signals to create.
               Returns:
                   String with derived signals create success and # of derived signals created.
            """
            try:
                derivedSignals = toDataFrame(derivedSignals)
            except:
                print("Failed to transform derived signals to dataframe.")
                raise
            try:
                req_cols = [
                    'sourceKey',
                    'sourceValue',
                    'targetKey',
                    'targetValue'
                ]
                if req_cols != list(derivedSignals):
                    raise ValueError('Derived Signals column names are incorrect')
            except (ValueError):
                raise
            successful_signals = 0
            for i in range(0, len(derivedSignals)):
                data = {
                        "sourceKey":derivedSignals.loc[i]['sourceKey']),
                        "sourceValue":derivedSignals.loc[i]['sourceValue'],
                        "targetKey":derivedSignals.loc[i]['targetKey']),
                        "targetValue":derivedSignals.loc[i]['targetValue']
                        }
                data = json.dumps(data)
                response = apiRequest(call="signals/derived", method="post", data=data)
                status = response.status_code
                if status != 201:
                    raise APIError(status)
                elif status == 201:
                    successful_signals += 1
            return('Created {0} derived signals.'.format(successful_signals))
