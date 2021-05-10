import json
import sys


def readJsonData():
    fp = open('layer-0.json', 'r')
    data = json.load(fp)
    print(data)
    return data


def findDistance(center1, center2):
    a, b = center1
    c, d = center2
    return ((a-c)**2 + (b-d)**2) ** (0.5)


def findCell(data, point):
    res = None
    min_d = sys.maxsize
    for i in data:
        k = findDistance(data[i].get('center'), point)
        if k < min_d:
            res = (i, data[i])
            min_d = k
    return res


def main():
    data = readJsonData()
    while 1:
        lat = float(input())
        lng = float(input())
        cell = findCell(data, [lat, lng])
        print(cell)


if __name__ == '__main__':
    main()

'''
[25.199, 55.2773], 'vertex': [[75.199, 55.2773], [-24.801, 55.2773], [50.199, 56.1423], [0.19900000000000162, 54.412299999999995], [0.19900000000000162, 56.1423], [50.199, 54.412299999999995]],
'''