import numpy as np
from pyFiles.shapes.shapesContainer import ShapesContainer
from pyFiles.shapes.sphere import Sphere
from pyFiles.scene.light import Light
from typing import NoReturn, List


def random_color() -> np.ndarray:
    np.random.seed(np.random.randint(1, 10000, dtype=np.int))
    r: np.uint8 = np.random.randint(0, 255, dtype=np.uint8)
    g: np.uint8 = np.random.randint(0, 255, dtype=np.uint8)
    b: np.uint8 = np.random.randint(0, 255, dtype=np.uint8)
    return np.array([r, g, b], dtype=np.uint8)


def cast_ray_sphere(orig: np.ndarray, direction: np.ndarray, sphere: Sphere,
                    sphere_color: np.ndarray, background_color: np.ndarray) -> np.ndarray:
    if sphere.intersect(orig, direction)[0]:
        return sphere_color
    else:
        return background_color


def cast_ray(orig: np.ndarray, direction: np.ndarray, shapes: ShapesContainer,
             sphere_color: np.ndarray, background_color: np.ndarray) -> np.ndarray:
    if shapes.intersect_any(orig, direction)[0]:
        return sphere_color
    else:
        return background_color


def cast_ray_material(orig: np.ndarray, direction: np.ndarray, shapes: ShapesContainer,
                      lights: List[Light]) -> np.ndarray:
    intersected_any, material, normal, point = shapes.intersect_any(orig, direction)
    if intersected_any:
        normal = vector_normalize(normal)
        light_intensity: float = 0
        for light in lights:
            light_dir: np.ndarray = vector_normalize(light.position() - point)
            scalar_product: float = max(0.0, np.vdot(light_dir, normal))
            light_intensity += light.intensity() * scalar_product
        return material * light_intensity
    else:
        return np.array([0, 0, 0])


def vector_normalize(vector: np.ndarray) -> np.ndarray:
    return vector / np.linalg.norm(vector)
