from osgeo import ogr, osr

# setup function to reproject coordinates
def convertCoords(xy, src='', targ=''):

    srcproj = osr.SpatialReference()
    srcproj.ImportFromEPSG(src)
    targproj = osr.SpatialReference()
    if isinstance(targ, str):
        targproj.ImportFromProj4(targ)
    else:
        targproj.ImportFromEPSG(targ)
    transform = osr.CoordinateTransformation(srcproj, targproj)

    pt = ogr.Geometry(ogr.wkbPoint)
    pt.AddPoint(xy[0], xy[1])
    pt.Transform(transform)

    return ([pt.GetX(), pt.GetY()])

def addDistance(latlng, a, b):
    coords = (-116.419389, 38.802610)
    albersXY = convertCoords(coords, 4326, 5070)
    albersXY[0] = albersXY[0] + 20 * 1609.344
    albersXY[1] = albersXY[1] + 20 * 1609.344
    newlonlat = convertCoords(albersXY, 5070, 4326)
    print(newlonlat)

def main():
    latlng = (25.6, 57.6)
    a = 20
    b = 20
    addDistance(latlng, a, b)