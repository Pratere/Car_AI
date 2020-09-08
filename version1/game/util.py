import pyglet, math

def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt(
        (point_1[0] - point_2[0]) ** 2 +
        (point_1[1] - point_2[1]) ** 2)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return 0, 0

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def make_hexagon(start_x, start_y, length):
    angle_radians = 0
    delta_rads = -math.radians(120)
    coordinates = [start_x, start_y]
    xi, yi = start_x, start_y
    for i in range(6):
        xf = xi + (-math.sin(angle_radians) * length)
        coordinates.append(xf)
        yf = yi + (-math.cos(angle_radians) * length)
        coordinates.append(xf)
        xi, yi = xf, yf
        angle_radians += delta_rads
    return coordinates


def makeCircle(numPoints, center, radius):
    verts = []
    for i in range(numPoints):
        angle = math.radians(float(i)/numPoints * 360.0)
        x = radius*math.cos(angle) + center[0]
        y = radius*math.sin(angle) + center[1]
        verts += [x,y]
    return pyglet.graphics.vertex_list(numPoints, ('v2f', verts)), verts

def return_5(x):
    return 5
