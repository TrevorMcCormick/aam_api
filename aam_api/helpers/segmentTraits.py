import requests
import json
import base64 as base64
import pandas as pd
import xlrd
import re

from aam_api.helpers.apiRequest import apiRequest
from aam_api.helpers.apiError import APIError

def segmentTraits(df):
    df['traits'] = None
    for index, row in df.iterrows():
        traits = [m.split() for m in re.findall(r"\w+T(?:\s+\w+T)*", row['segmentRule'])]
        traits = [y[:-1] for x in traits for y in x]
        traits = [ x for x in traits if x.isdigit() ]
        df.at[index, 'traits'] = traits
    return(df)
