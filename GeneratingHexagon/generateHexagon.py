class GenerateHexagon():
    def __init__(self, center=(0, 0), radius=100, range=1000):
        self.center = center
        self.radius = radius
        self.range = range

    def findVertexOfHexagon(self, a, b, d):
        # (a, b) is center of Hexagon
        # d is distance between center and vertex
        root3by2 = (3 ** 0.5) / 2
        point = [(a + d, b), (a - d, b), (a + d / 2, b + root3by2), (a - d / 2, b - root3by2),
                 (a - d / 2, b + root3by2), (a + d / 2, b - root3by2)]
        return point
