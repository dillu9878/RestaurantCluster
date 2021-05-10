import json


class GenerateHexagon():
    def __init__(self, center=(25.199, 55.2773), cellsize=10, range=10000):
        self.center = center # point
        self.cellsize = cellsize # in meter
        self.range = range # in meter
        self.result = {}
        self.generateHexagon()
        print(self.result)
        import pdb
        pdb.set_trace()
        # fp = open('result.json', 'w')
        # json.dump(self.result, fp, indent=4)


    def generateHexagon(self):
        queue = [self.center]
        visited = set()
        while queue:
            p = queue.pop(0)
            if self.check(visited, p, self.cellsize):
                continue
            if self.findDistance(self.center, p) > self.range:
                continue
            vertex_point = self.findVertexOfHexagon(p, self.cellsize)
            self.result[p] = vertex_point
            # print(f'point: {p}; Vertex: {vertex_point}')
            visited.add(p)
            queue += self.findCenterOfNextHexagon(p, self.cellsize)

    def check(self, visited, center, cellsize):
        for i in visited:
            if self.findDistance(i, center) < cellsize/2:
                return True
        return False

    def findDistance(self, center1, center2):
        a, b = center1
        c, d = center2
        return ((a-c)**2 + (b-d)**2) ** (0.5)

    def findVertexOfHexagon(self, center, d):
        # (a, b) is center of Hexagon
        # d is distance between center and vertex
        a, b = center
        # root3by2 = (3 ** 0.5) / 2
        root3by2 = (1.73) / 2
        point = [(a + d, b), (a - d, b), (a + d / 2, b + root3by2), (a - d / 2, b - root3by2),
                 (a - d / 2, b + root3by2), (a + d / 2, b - root3by2)]
        return point


    def findCenterOfNextHexagon(self, center, d):
        # (a, b) is center of Hexagon
        # d is distance between center and next center
        a, b = center
        # root3by2 = (3 ** 0.5) / 2
        root3by2 = (1.73) / 2
        d = 2*d*root3by2
        point = [(a, b + d), (a, b + d), (a + root3by2, b + d/2), (a - root3by2, b - d/2),
                 (a - root3by2, b + d/2), (a + root3by2, b - d/2)]
        return point


if __name__ == '__main__':
    GenerateHexagon()
