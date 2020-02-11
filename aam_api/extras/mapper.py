import requests
import json
import base64 as base64
import pandas as pd
import xlrd

from aam_api.helpers.apiError import APIError
from aam_api.helpers.apiRequest import apiRequest
from aam_api.helpers.bytesToJson import bytesToJson
from aam_api.helpers.flattenJson import flattenJson
from aam_api.helpers.toDataFrame import toDataFrame

class Mapper:
    @classmethod
    def segmentsToDestination(cls, destinationId):
            """
            Get all segments mapped to an AAM Destination.
            Args:
                destinationId: AAM Destination ID.
            Returns:
                df with rows of each segment and columns of one destination.
            """
            data = {"destinationId":destinationId}
            response = apiRequest(call="destinations/{0}/mappings".format(destinationId), method="get", data=data)
            status = response.status_code
            if status != 200:
                raise APIError(status)
            else:
                df = pd.DataFrame(response.json())
                df = df[["sid"]]
                return df
    @classmethod
    def segmentsToDestinations(cls):
            """
            Get all segments mapped to all AAM Destinations.
            Args:
                None
            Returns:
                df with rows of each segment and columns of each destination, with a 1 if it is mapped and a 0 if it is not mapped.
            """
            segments = Segments.get_many()
            segments = segments[["sid", "name"]]
            destinations = Destinations.get_many()
            destinations = destinations[["destinationId"]]

            # Set index for df
            df = segments
            df = df.set_index(['sid', 'name'])

            # Create new col for each destinaton
            for i in range(0, len(destinations)):
                try:
                    destination = destinations.iloc[i][0]
                    mapped_segments = Mapper.segmentsToDestination(destination)
                    for index, row in mapped_segments.iterrows():
                        df.at[row[0], destination] = 1
                except:
                    # Col has no mapped segments
                    destination = destinations.iloc[i][0]
                    df[destination] = np.NaN
                    pass
            return df
