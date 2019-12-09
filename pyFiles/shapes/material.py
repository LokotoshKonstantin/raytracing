import numpy as np


class Material:
    def __init__(self, color: np.ndarray):
        self._m: np.ndarray = color

    def material(self) -> np.ndarray:
        return self._m
