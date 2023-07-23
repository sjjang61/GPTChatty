import requests

def get( url, data = {}, headers = {}):
    # headers = {'Content-Type': 'application/json; charset=utf-8'}
    response = requests.get(url=url, data=data, headers=headers)
    print("[API-GET-RES] status = %s, response = %s" % (response.status_code, response.json()))
    return response.json()

def get_text( url, data = {}, headers = {}):
    response = requests.get(url=url, data=data, headers=headers)
    print("[API-GET-RES] status = %s, response = %s" % ( response.status_code, response.text ))
    return response.text

def post( url, data, headers ):
    response = requests.post(url=url, data=data, headers=headers)
    print("[API-POST-RES] status = %s, response = %s" % ( response.status_code, response.json() ))
    return response.json()

def put( url, data, headers ):
    response = requests.put(url=url, data=data, headers=headers)
    print("[API-PUT-RES] status = %s, response = %s" % ( response.status_code, response.json() ))
    return response.json()

def delete( url, data, headers ):
    response = requests.delete(url=url, data=data, headers=headers)
    print("[API-PUT-RES] status = %s, response = %s" % ( response.status_code, response.json() ))
    return response.json()