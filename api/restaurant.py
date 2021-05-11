# import the module
from __future__ import print_function
import aerospike
import sys
from aerospike_helpers.operations import map_operations


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


def addRestaurant(restaurant, client=None):
    try:
        if client is None:
            client = connect()

        key = ('test', 'bowlhouse', restaurant.get('cell_id'))
        ret = client.operate(key, [map_operations.map_put("restaurants", restaurant.get('id'), restaurant)])
        # print(ret)
        if ret:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def updateRestaurant(restaurant, client=None):
    try:
        if client is None:
            client = connect()

        key = ('test', 'bowlhouse', restaurant.get('cell_id'))
        ret = client.operate(key, [map_operations.map_put("restaurants", restaurant.get('id'), restaurant)])
        if ret:
            return True
        else:
            return False
    except:
        return False


def deleteRestaurant(cell_id, restaurant_id, client=None):
    try:
        if client is None:
            client = connect()

        key = ('test', 'bowlhouse', cell_id)
        ret = client.operate(key, [map_operations.map_remove_by_key("restaurants", restaurant_id, aerospike.MAP_RETURN_KEY_VALUE)])
        # print(ret)
        if ret:
            return True
        else:
            return False
    except Exception as e:
        print(e)
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
        "cell_id": 'l-0-id-3'
    }
    print(addRestaurant(restaurant))
    print(deleteRestaurant(restaurant.get('cell_id'), restaurant.get('id')))


if __name__ == '__main__':
    main()

