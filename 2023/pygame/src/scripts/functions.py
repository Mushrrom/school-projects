import math
from typing import Union

def getAngle(x1: Union[int, float], y1: Union[int, float], x2: Union[int, float], y2: Union[int, float]):
    """Gets the angle from object 1 to object 2

    Args:
        x1 (int, float): X position of object 1
        y1 (int, float): Y position of object 1
        x2 (int, float): X position of object 2
        y2 (int, float): Y position of object 2

    Returns:
        int: The angle from object 1 to object 2
    """
    xDistance = x1-x2
    yDistance = y1-y2

    if yDistance == 0:
        return 90 if xDistance > 0 else 270

    angle = math.atan(xDistance/yDistance) * 180 / math.pi

    if yDistance < 0:
        angle += 180

    return angle
