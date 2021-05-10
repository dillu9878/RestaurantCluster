import requests

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


def main():
    origin = [25.240075265448, 55.31232824462227]
    destination = [25.25018152947311, 55.29641624334061]
    print(getDistance(origin, destination))


if __name__ == '__main__':
    main()