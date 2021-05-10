import requests
import aerospike
import sys
import json


def connect():
    config = {
      'hosts': [('127.0.0.1', 3000)]
    }

    # Create a client and connect it to the cluster
    try:
        client = aerospike.client(config).connect()
    except Exception as e:
        print("failed to connect to the cluster with", config['hosts'], 'error: ', str(e))
        sys.exit(1)
    return client


def getDistance(origin, destination):
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    api_key = 'AIzaSyBmKPHweP0_38gklM1cuhEzPBud1cweAEQ'
    data = None
    params = {
        'origins': ','.join(list(map(str, origin))),
        'destinations': ','.join(list(map(str, destination))) ,
        'key': api_key
    }
    response = requests.get(base_url, params=params).json()
    if response.get('status') == 'OK':
        obj = response['rows'][0].get('elements')
        if obj:
            obj = obj[0]
            if obj.get('status') == 'OK':
                data = {
                    'distance': obj.get('distance').get('text'),
                    'duration': obj.get('duration').get('text')
                }
    return data


def findDistance(origin_cell, destination_cell, client = None):
    if client is None:
        client = connect()
    origin_cell_id = origin_cell.get('id')
    destination_cell_id = destination_cell.get('id')
    origin_cell_center = origin_cell.get('center')[::-1] # converting [lng, lat] -->> [lat, lng]
    destination_cell_center = destination_cell.get('center')[::-1]
    key_hash = hash((origin_cell_id, destination_cell_id))
    key = ('test', 'bowlhouse', key_hash)
    key, metadata = client.exists(key)
    if metadata is None:
        data = getDistance(origin_cell_center, destination_cell_center)
        if data:
            client.put(key, data)
    key, metadata, data = client.get(key)
    return data


def main():
    origin_cell = {
        'id': 'l-0-id-0',
        'center': [55.31232824462227, 25.240075265448, ]
    }
    destination_cell = {
        'id': 'l-0-id-1',
        'center': [55.29641624334061, 25.25018152947311]
    }
    print(findDistance(origin_cell, destination_cell))


if __name__ == '__main__':
    main()