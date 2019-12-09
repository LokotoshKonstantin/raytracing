from typing import Tuple
import numpy as np


class IShape:
    def intersect(self, orig: np.ndarray, direction: np.ndarray) -> Tuple[bool, float]:
        raise NotImplementedError("IShape.intersect() not implemented")
