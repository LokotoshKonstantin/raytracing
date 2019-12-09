from pyFiles.shapes.material import Material
from typing import Tuple
import numpy as np


class IShape:
    def __init__(self, m: Material, center: np.ndarray):
        self._material: Material = m
        self._c: np.ndarray = center.copy()

    def intersect(self, orig: np.ndarray, direction: np.ndarray) -> Tuple[bool, float]:
        raise NotImplementedError("IShape.intersect() not implemented")

    def material(self) -> np.ndarray:
        return self._material.material()

    def center(self) -> np.ndarray:
        return self._c
