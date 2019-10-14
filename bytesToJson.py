#' bytesToJson
def bytesToJson(response_content):
    json_response = json.loads(response_content.decode('utf-8'))
    from pandas.io.json import json_normalize
    df = json_normalize(json_response)
    return(df)
