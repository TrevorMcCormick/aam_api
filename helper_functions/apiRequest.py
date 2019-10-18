#' apiRequest

def apiRequest(call, method, data=""):
    url= "https://api.demdex.com/v1/{}/".format(call)
    header =  {'Authorization' : 'Bearer '+token,'accept': 'application/json'}
    response = requests.request(method, url, headers=header,params=data)
    return(response)
