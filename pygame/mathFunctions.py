import math

def getAngle(x1, y1, x2, y2):
    """Gets the angle from object 1 to object 2

    Args:
        x1 (int): X position of object 1
        y1 (int): Y position of object 1
        x2 (int): X position of object 2
        y2 (int): Y position of object 2
    """
    xDistance = x1-x2
    yDistance = y1-y2

    if yDistance == 0:
        return 90 if xDistance > 0 else 270

    angle = math.atan(xDistance/yDistance) * 180 / math.pi

    if yDistance < 0:
        angle += 180

    return angle
