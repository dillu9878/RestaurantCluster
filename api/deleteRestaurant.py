# import the module
from __future__ import print_function
import aerospike
import sys
import math
from aerospike_helpers.operations import list_operations as listops
import json
from geopy.geocoders import Nominatim
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


def deleteRestaurant(restaurant, client=None):
    try:
        if client is None:
            client = connect()

        key = ('test', 'bowlhouse', restaurant.get('cell_id'))
        # ret = client.operate(key, [listops.list_append("restaurants", restaurant)])
        ret = client.operate(key, [listops.list_remove_by_value("restaurants", restaurant, aerospike.LIST_RETURN_COUNT)])
        print(ret)
        if ret:
            return True
        else:
            return False
    except:
        return False




def main():
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
        "updated_date": "2021-04-29T11:29:37.376498Z",
        "cell_id": 'l-0-id-2'
    }
    print(deleteRestaurant(restaurant))


if __name__ == '__main__':
    main()

