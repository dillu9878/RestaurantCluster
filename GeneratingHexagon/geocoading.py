import requests
from googleplaces import GooglePlaces, types, lang
API_KEY= 'AIzaSyBmKPHweP0_38gklM1cuhEzPBud1cweAEQ'


def get_geo_coading(address):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    API_KEY = 'AIzaSyBmKPHweP0_38gklM1cuhEzPBud1cweAEQ'
    params = {
        'key': API_KEY,
        'address': address,
    }
    response = requests.get(base_url, params=params).json()
    # print(response)
    # print(response['status'])
    if response['status'] == 'OK':
        geo = response['results'][0]['geometry']
        geolocation = geo['location']
        return geolocation
    else:
        return None

def get_reverse_geocode(latlng):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    api_key = 'AIzaSyBmKPHweP0_38gklM1cuhEzPBud1cweAEQ'
    params = {
        'key': api_key,
        'latlng': latlng,
    }
    response = requests.get(base_url, params=params).json()
    if response['status'] == 'OK':
        geo = response['results'][0]
        locality = None
        for i in geo.get('address_components'):
            if 'locality' in i.get('types'):
                locality = i.get('long_name')
        address = response['results'][0]['formatted_address']
        location = {
            'locality': locality,
            'address': address
        }
        return location
    else:
        return None


def get_similar_place(place='', location=''):
    if place is None or len(place) == 0:
        return []
    google_places = GooglePlaces(API_KEY)
    query_result = google_places.autocomplete(
        input = place,
        location = location
    )
    predicted_place = []

    if query_result is not None:
        size = len(query_result.raw_response['predictions'])
        for i in range(size):
            id = query_result.raw_response['predictions'][i]['place_id']
            address = query_result.raw_response['predictions'][i]['description']
            place = address.split(',')[0]
            item = {
                'id': id,
                'place': place,
                'address': address
            }
            predicted_place.append(item)
    return predicted_place


def get_latlng_place(place_id=None):
    if place_id:
        google_places = GooglePlaces(API_KEY)
        place = google_places.get_place(place_id)

        geo_loc = place.geo_location
        return geo_loc
    else:
        return {}


if __name__ == '__main__':
    ADDRESS = 'D-228, Mohali'
    geo = get_geo_coading(ADDRESS)
    print(f'Address: {ADDRESS}\nGeo-Location: {geo}')
    ADDRESS = '30.6959,76.6872975'
    print(get_reverse_geocode(ADDRESS))
    res = get_similar_place("Krish Gethin", "Mohali")
    print('similar place:', res)

    # place id search
    place_id = 'ChIJhWkseR3vDzkR-MDirgTAPp0'
    get_latlng_place(place_id)

