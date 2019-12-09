import numpy as np
from pyFiles.shapes.sphere import Sphere
from typing import NoReturn


def random_color() -> np.ndarray:
    np.random.seed(np.random.randint(1, 10000, dtype=np.int))
    r: np.uint8 = np.random.randint(0, 255, dtype=np.uint8)
    g: np.uint8 = np.random.randint(0, 255, dtype=np.uint8)
    b: np.uint8 = np.random.randint(0, 255, dtype=np.uint8)
    return np.array([r, g, b], dtype=np.uint8)


def cast_ray(orig: np.ndarray, direction: np.ndarray, sphere: Sphere,
             sphere_color: np.ndarray, background_color: np.ndarray) -> np.ndarray:
    if sphere.ray_intersect(orig, direction)[0]:
        return sphere_color
    else:
        return background_color


def vector_normalize(vector: np.ndarray) -> np.ndarray:
    return vector / np.linalg.norm(vector)
