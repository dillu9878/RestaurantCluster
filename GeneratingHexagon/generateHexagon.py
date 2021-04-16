import json

class GenerateHexagon():
    def __init__(self, center=(0, 0), cellsize=10, range=100):
        self.center = center # point
        self.cellsize = cellsize # in meter
        self.range = range # in meter
        self.result = {}
        self.generateHexagon()
        print(self.result)
        fp = open('result.json', 'w')
        json.dump(self.result, fp, indent=4)


    def generateHexagon(self):
        queue = [self.center]
        visited = set()
        while queue:
            p = queue.pop(0)
            if p in visited:
                continue
            if self.findDistance(self.center, p) > self.range:
                continue
            vertex_point = self.findVertexOfHexagon(p, self.cellsize)
            self.result[str(p)] = vertex_point
            visited.add(p)
            queue += self.findCenterOfNextHexagon(p, self.cellsize)

    def findDistance(self, center1, center2):
        a, b = center1
        c, d = center2
        return ((a-c)**2 + (b-d)**2) ** (0.5)

    def findVertexOfHexagon(self, center, d):
        # (a, b) is center of Hexagon
        # d is distance between center and vertex
        a, b = center
        root3by2 = (3 ** 0.5) / 2
        point = [(a + d, b), (a - d, b), (a + d / 2, b + root3by2), (a - d / 2, b - root3by2),
                 (a - d / 2, b + root3by2), (a + d / 2, b - root3by2)]
        for i in range(len(point)):
            point[i] = str(point[i])
        return point

    def findCenterOfNextHexagon(self, center, d):
        # (a, b) is center of Hexagon
        # d is distance between center and next center
        a, b = center
        root3by2 = (3 ** 0.5) / 2
        d = 2*d*root3by2
        point = [(a, b + d), (a, b + d), (a + root3by2, b + d/2), (a - root3by2, b - d/2),
                 (a - root3by2, b + d/2), (a + root3by2, b - d/2)]
        return self.round6(point)

    def round6(self, points):
        point = []
        for i in points:
            point.append((round(i[0], 2), round(i[1], 2)))

        return point


if __name__ == '__main__':
    GenerateHexagon()
