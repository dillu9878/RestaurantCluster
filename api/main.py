from findCell import findCell
from nearByRestaurants import findRestaurants


def main():
    point = {
        'lat': 25.240075265448,
        'lng': 55.31232824462227,
    }
    cell = findCell(point)
    print('Nearest Cell:', cell)
    if cell:
        restaurants = findRestaurants(cell=cell, page=1)
        for i in restaurants:
            print(i)
    else:
        print("No cell found")


if __name__ == '__main__':
    main()