
# import the module
from __future__ import print_function
import aerospike
from aerospike_helpers.operations import list_operations as listops
import json
from geopy.geocoders import Nominatim
# Configure the client
config = {
  'hosts': [ ('127.0.0.1', 3000) ]
}

# Create a client and connect it to the cluster
try:
  client = aerospike.client(config).connect()
except:
  import sys
  print("failed to connect to the cluster with", config['hosts'])
  sys.exit(1)

# Records are addressable via a tuple of (namespace, set, key)
def findAddress(point):
    geodata = Nominatim(user_agent='new').reverse(point)
    if geodata:
        locality = str(geodata).split(',')[0]
        add = {
            'locality': locality,
            'address': str(geodata)
        }
    else:
        add = {
            'locality': None,
            'address': None
        }
    return add

def upload(key,  val):
    key = ('test', 'bowlhouse', key)

    try:
      # Write a record
      # val['address'] = findAddress(val['center']),
      val['center'] = aerospike.geodata({
          'type': 'Point',
          'coordinates': val['center']
      })

      # val['inside'] = None
      client.put(key, val)
    except Exception as e:
      import sys
      print("error: {0}".format(e), file=sys.stderr)

    # Read a record
    (key, metadata, record) = client.get(key)
    print(record)

def print_result(value):
    print(value)

def query_circle(client):
    """Query for records inside a circle."""
    # client.index_list_create('test', 'bowlhouse', 'center', aerospike.INDEX_GEO2DSPHERE, 'demo_point_nidx')
    query = client.query('test','bowlhouse')

    lat = 25.240
    lng = 55.3
    predicate = aerospike.predicates.geo_within_radius('center',
                                                       lng,
                                                       lat,
                                                       50,
                                                       )
    query.where(predicate)
    # query.apply('filter_by_amenity', 'apply_filter', [ ])
    query.foreach(print_result)
    # import pdb
    # pdb.set_trace()
    # Search with UDF amenity filter
    # query.apply('filter_by_amenity', 'apply_filter', [args.amenity,])

def update(client, key, value):
    # query = client.query('test', 'bowlhouse')
    key = ('test', 'bowlhouse', key)
    key1, metadata, bins = client.get(key)
    print(key1)
    print(metadata)
    print(bins)
    print('---------------')
    restaurant = {
                "id": "XT8TgGzrJQCkYJPx",
                "profile_pic": "http://2bofficedubai.ddns.net:8000/media/restaurants/images/burger_king.jpeg",
                "name": "Burger King",
                "address": "Krish Gethin",
                "contact_person": "Krish",
                "mobile": "9878916296",
                "email": "k@gmail.com",
                "latitude": 43.6574989,
                "longitude": -116.3380162,
                "opening_time": "01:00:00",
                "closing_time": "21:00:00",
                "login_status_code": 0,
                "rating": 3,
                "active": False,
                "created_date": "2021-04-29T11:29:37.376422Z",
                "updated_date": "2021-04-29T11:29:37.376498Z"
            }
    ret = client.operate(key, [listops.list_append("restaurants", restaurant)])
    key1, metadata, bins = client.get(key)
    print(key1)
    print(metadata)
    print(bins)
    print('---------------')



def main():
    fp = open('../GeneratingHexagon/layer-0-oud_mehta_dubai.json', 'r')
    data = json.load(fp)
    for i in data:
        upload(i.get('id'), i)

# main()
query_circle(client)
# update(client, 'l-0-id-0', '')
# Close the connection to the Aerospike cluster
client.close()