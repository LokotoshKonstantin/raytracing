from pyFiles.shapes.interface import IShape
import numpy as np
from typing import List, NoReturn
import sys


class ShapesContainer:
    def __init__(self, distance_border: float, *shapes: IShape):
        self._container: List[IShape] = []
        self._min_distance: float = float(sys.maxsize - 1)
        self._distance_border: float = distance_border
        for shape in shapes:
            self._container.append(shape)

    def _reinit_distance(self) -> NoReturn:
        self._min_distance: float = float(sys.maxsize - 1)

    def intersect_any(self, orig: np.ndarray, direction: np.ndarray) -> NoReturn:
        self._reinit_distance()
        for shape in self._container:
            is_intersected, current_distance = shape.intersect(orig, direction)
            if is_intersected and (current_distance < self._min_distance):
                self._min_distance = current_distance
        return self._min_distance < self._distance_border

    def append(self, *shapes: IShape):
        for shape in shapes:
            self._container.append(shape)