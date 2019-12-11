import numpy as np
from typing import List
import render.utils as utils
from logs.log_reader import profile


@profile
def rendering_per_pixel(scene: np.ndarray, shapes: np.ndarray, fov_degree: float,
                        materials: list,
                        lights: List[np.ndarray],
                        eye_position: np.ndarray) -> np.ndarray:
    h: int = scene.shape[0]
    w: int = scene.shape[1]

    fov: float = np.deg2rad(fov_degree)
    scale: float = np.tan(fov * 0.5)
    imageAspectRatio: float = float(w) / float(h)

    for i in range(0, h):
        for j in range(0, w):
            x: float = (2 * (i + 0.5) / float(w) - 1) * scale
            y: float = (1 - 2 * (j + 0.5) / float(h)) * scale * (1. / imageAspectRatio)

            direction: np.ndarray = np.array([y, x, -1.], dtype=float)
            direction = direction / np.linalg.norm(direction)
            scene[i, j] = utils.raytracer(eye_position, direction, shapes, materials, lights, 0)

    return np.clip(scene, 0, 255).astype(np.uint8)

