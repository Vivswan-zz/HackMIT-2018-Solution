import constants
import requests
import uuid

def get_route(route, data=None, json=True):
    endpoint = "%s/u/%s/tracker/%s" % (
        constants.NODE_SERVER,
        constants.USERNAME,
        route
    )
    
    r = requests.post(endpoint, data=data)

    if json:
        return r.json()
    else:
        # Raw
        return r.text

def gen_uuid():
    return str(uuid.uuid4()).replace('-', '')
