# import the module
from __future__ import print_function
import aerospike
import sys
import math

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


def findDistance(center1, center2):
    a, b = center1.coordinates
    c, d = center2.coordinates
    R = 6378

    lat1 = math.radians(a)
    lon1 = math.radians(b)
    lat2 = math.radians(c)
    lon2 = math.radians(d)

    dlon = lon2 - lon1

    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    # Haversine
    # formula

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


def nearestCell(records, point):
    res = None
    min_d = sys.maxsize
    for i in records:
        key, metadata, data = i
        k = findDistance(data.get('center'), point)
        if k < min_d:
            res = (i, data[i])
            min_d = k
    return res


def findCell(point, client=None, range=51):
    if client is None:
        client = connect()

    predicate = aerospike.predicates.geo_within_radius('center',
                                                       point.get('lng'),
                                                       point.get('lat'),
                                                       range) # here 51 is cell size
    query = client.query('test', 'bowlhouse')
    query.where(predicate)
    query.select('id', 'center', 'address')
    records = query.results()
    if records:
        key, metadata, data = records[0]
        return data
    else:
        return None


def main():
    point = {
        'lat': 25.240,
        'lng': 55.3,
    }
    print(findCell(point))


if __name__ == '__main__':
    main()

