from pyFiles.shapes.interface import IShape
from pyFiles.shapes.material import Material
import numpy as np
from typing import List, NoReturn, Tuple
import sys


class ShapesContainer:
    def __init__(self, distance_border: float, *shapes: IShape):
        self._container: List[IShape] = []
        self._min_distance: float = float(sys.maxsize - 1)
        self._distance_border: float = distance_border
        for shape in shapes:
            self._container.append(shape)

    def _reinit(self) -> NoReturn:
        self._min_distance: float = float(sys.maxsize - 1)

    def intersect_any(self, orig: np.ndarray, direction: np.ndarray) -> Tuple[bool, np.ndarray, np.ndarray, np.ndarray]:
        self._reinit()
        material: np.ndarray = np.zeros(shape=(3,), dtype=np.uint8)
        normal: np.ndarray = np.zeros(shape=(3,), dtype=np.float)
        hit: np.ndarray = np.zeros(shape=(3,), dtype=np.float)

        for shape in self._container:
            is_intersected, current_distance = shape.intersect(orig, direction)

            if is_intersected and (current_distance < self._min_distance):
                self._min_distance = current_distance
                hit = orig + direction * current_distance
                normal = hit - shape.center()
                material = shape.material()

        return self._min_distance < self._distance_border, material, normal, hit

    def append(self, *shapes: IShape):
        for shape in shapes:
            self._container.append(shape)