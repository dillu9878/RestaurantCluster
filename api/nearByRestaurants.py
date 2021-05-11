# import the module
from __future__ import print_function
import aerospike
import sys
from restaurant_cluster.api import findDistance

# Configure the client


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


def print_values(value):
    print(value)
    return True

def change_format(cell):
    try:
        center = cell.get('center').unwrap()
        center = center.get('coordinates')[::-1]
        data = {
            'id': cell.get('id'),
            'center': center
        }
        return data
    except:
        return cell


def get_restaurant(data, start, end):
    res = []
    for i in data[start:end+1]:
        res.append(i[1])
    return res


def findRestaurants(cell, page=None, client=None, range=2000):
    if page is None:
        page = 1
    data = []
    cell = change_format(cell)
    point = cell.get('center')
    if client is None:
        client = connect()

    predicate = aerospike.predicates.geo_within_radius('center',
                                                       point[1], #longitude
                                                       point[0], #latitude
                                                       range)
    query = client.query('test', 'bowlhouse')
    query.where(predicate)
    query.select('id', 'center', 'restaurants')
    records = query.results()
    for record in records:
        key, metadata, value = record
        # dis = {'duration': 30, 'distance': 5}  # findDistanceAPI
        if value.get('restaurants'):
            dis = findDistance.findDistance(change_format(value), change_format(cell))  # findDistanceAPI
        for id, restaurant in value.get('restaurants').items():
            dur = dis.get('duration')
            restaurant['duration'] = dur
            restaurant['distance'] = dis.get('distance')
            k = int(dur.split()[0])
            data.append((k, restaurant))
    data = sorted(data, key=lambda x:x[0] )
    total_count = len(data)
    page_max = total_count//10
    if total_count%10 != 0:
        page_max += 1
    if page <= page_max:
        start = (page-1)*10
        end = start + 10
        data = get_restaurant(data, start, end)
    else:
        data = []

    res = {
        'count': total_count,
        'restaurant': data
    }

    return res


def main():
    cell = {
        'id': 'l-0-id-1',
        'center': [25.2393563,55.3085524], # [lat, lng]
    }
    print(findRestaurants(cell=cell, page=1))


if __name__ == '__main__':
    main()

