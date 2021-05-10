import json
import sys

from geocoading import get_reverse_geocode
import time
import math
from geopy.geocoders import Nominatim


class GenerateHexagon():
    def __init__(self, center=(25.199, 55.2773), cellsize=10, range=10000):
        self.center = center # point
        self.cellsize = cellsize # in meter
        self.range = range # in meter
        self.result = {}
        self.generateHexagon()

        print(self.result)
        print('total no of cell:', len(self.result))

    def generateHexagon(self):
        queue = [self.center]
        visited = set()
        key_prefix = 'l-0-id-'
        count = 0
        while queue:
            p = queue.pop(0)
            if self.check(visited, p, self.cellsize):
                continue
            if self.findDistance(self.center, p) > self.range:
                continue
            # vertex_point = self.findVertexOfHexagon(p, self.cellsize)
            visited.add(p)
            next_center = self.findCenterOfNextHexagon(p, self.cellsize)
            queue += next_center

            key = key_prefix + str(count)
            self.result[key] = (p, next_center)
            print(f'key: {key}; point: {p}; Surrounded Center: {next_center}')
            count += 1

    def check(self, visited, center, cellsize):
        for i in visited:
            if self.findDistance(i, center) < cellsize/2:
                return True
        return False

    def findDistance(self, center1, center2):
        a, b = center1
        c, d = center2
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

        # print(distance)

        return distance

    def findVertexOfHexagon(self, center, d):
        # (a, b) is center of Hexagon
        # d is distance between center and vertex
        a, b = center
        root3by2 = (3 ** 0.5) / 2
        # root3by2 = (1.73) / 2
        # point = [(a + d, b), (a - d, b), (a + d / 2, b + root3by2), (a - d / 2, b - root3by2),
        #          (a - d / 2, b + root3by2), (a + d / 2, b - root3by2)]
        point = [
            self.addDinLatLng(a, b, d, 0),
            self.addDinLatLng(a, b, -d, 0),
            self.addDinLatLng(a, b, d/2, root3by2*d),
            self.addDinLatLng(a, b, -d/2, -root3by2*d),
            self.addDinLatLng(a, b, -d/2, root3by2*d),
            self.addDinLatLng(a, b, +d/2, -root3by2*d),
        ]
        return point

    def findCenterOfNextHexagon(self, center, d):
        # (a, b) is center of Hexagon
        # d is distance between center and next center
        a, b = center
        root3by2 = (3 ** 0.5) / 2
        # root3by2 = (1.73) / 2
        d = 2*d*root3by2
        # point = [(a, b + d), (a, b + d), (a + root3by2, b + d/2), (a - root3by2, b - d/2),
        #          (a - root3by2, b + d/2), (a + root3by2, b - d/2)]
        point = [
            self.addDinLatLng(a, b, 0, d),
            self.addDinLatLng(a, b, 0, -d),
            self.addDinLatLng(a, b, root3by2*d, d/2),
            self.addDinLatLng(a, b, -root3by2*d, -d/2),
            self.addDinLatLng(a, b, -root3by2*d, +d/2),
            self.addDinLatLng(a, b, +root3by2*d, -d/2),
        ]
        return point

    def addDinLatLng(self, latitude, longitude, x, y):
        pi = math.pi
        cos = math.cos
        r_earth = 6378
        new_latitude = latitude + (x / r_earth) * (180 / pi)
        new_longitude = longitude + (y / r_earth) * (180 / pi) / cos(latitude * pi / 180)
        return (new_latitude, new_longitude)

    def findNextCenterId(self, centers):
        cells = []
        for i in centers:
            k = self.findNearestCell(i)
            if k:
                cells.append(k)
        return cells

    def findNearestCell(self, point):
        m = sys.maxsize
        res = None
        for i in self.result:
            dis = self.findDistance(point, self.result[i][0])
            if  dis< m:
                res = i
                m = dis
        return res

    def findAddress(self, point):
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

    def saveInDB(self):
        print('Total no Of cell:', len(self.result))
        res = []
        c = 0
        for i in self.result:
            cell = {
                'id': i,
                'center': self.result[i][0],
                # 'next_center': self.findNextCenterId(self.result[i][1]),
                # 'address': get_reverse_geocode(','.join(map(str, i))),
                'address': self.findAddress(self.result[i][0][::-1]),
                # 'address': None,
                'restaurants': []
            }
            res.append(cell)
            # time.sleep(2)
            print(f'Saving cell: {cell}')
            # input()
            if c>100:
                # time.sleep(120)
                c = 0
            c+=1
        fp = open('layer-0-oud_mehta_dubai.json', 'w')
        json.dump(res, fp, indent=4)





def main():
    # layer - 0

    # center from where we start generation of our hexagon cell
    center = (55.31232824462227,25.240075265448)
    # cell-size distance from center to hexagon vertex in meter
    cellsize = 50 # in meter
    cellsize = cellsize/1000 # km

    # range: radius of area we want to cover in meter
    range = 2 # km


    G = GenerateHexagon(center=center, cellsize=cellsize, range=range)
    G.saveInDB()

if __name__ == '__main__':
    main()
