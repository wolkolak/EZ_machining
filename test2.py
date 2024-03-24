import math

def rotate_around_dot(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    print(f'rotate_around_dot = {origin}|{point}|{angle}')

    ox, oy = origin
    px, py = point
    #ox = ox * -1

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

point = (3, 4)
origin = (2, 2)
print(rotate_around_dot(origin, point, math.radians(90)))