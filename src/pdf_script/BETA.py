from __future__ import annotations

import time
import types


def class_timer(cls):
    def timer(function):
        def __wrapper(*args, **kwargs):
            start = time.time()
            returned_value = function(*args, **kwargs)
            print("Working time: " + str(time.time() - start))

            return returned_value

        return __wrapper

    for name, attr in cls.__dict__.items():
        if isinstance(attr, types.FunctionType) and name != "__init__":
            setattr(cls, name, timer(attr))

    return cls


@class_timer
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print_coord(self):
        print(self.x, self.y)

    def distance_to(self, point: Point2D):
        return ((point.x - self.x) ** 2 + (point.y - self.y) ** 2) ** 0.5


point = Point2D(1, 1)
point2 = Point2D(2, 2)
print(point.distance_to(point2))
