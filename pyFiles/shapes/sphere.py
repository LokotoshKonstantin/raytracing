import numpy as np
from typing import Tuple


class Sphere:
    def __init__(self, center: np.ndarray, radius: float):
        self._c: np.ndarray = center.copy()
        self._r: float = radius

    def ray_intersect(self, orig: np.ndarray, direction: np.ndarray) -> Tuple[bool, float]:
        l: np.ndarray = self._c - orig
        tca: float = l * direction
        d2: float = l*l - tca*tca
        if d2 > (self._r * self._r):
            return False, -1.
        thc: float = np.sqrt(self._r * self._r - d2)
        t0: float = tca - thc
        t1: float = tca + thc
        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return False, -1.
        return True, t0
