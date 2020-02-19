import requests
import json
import base64 as base64
import pandas as pd
import xlrd
import re

from aam_api.helpers.apiRequest import apiRequest
from aam_api.helpers.apiError import APIError
from aam_api.helpers.segmentTraits import segmentTraits
from aam_api.core.segments import Segments

def inSegments(sid):
    segments = Segments.get_many()
    segments = segmentTraits(segments)
    segments_list = []
    for index, row in segments.iterrows():
        segment = segments.at[index, 'sid']
        traits = segments.at[index, 'traits']
        if str(sid) in traits:
            segments_list.append(segments.at[index, 'sid'])
    return(segments_list)

def inSegmentsBool(df, segments):
    flatten = lambda l: [item for sublist in l for item in sublist]
    flat = flatten(segments['traits'])
    flat = [ int(x) for x in flat ]
    df['inSegmentsBool'] = None
    df['inSegmentsBool'] = df['sid'].isin(flat)
    return(df)
