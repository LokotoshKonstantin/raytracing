from render.funcs.rendering import rendering_per_pixel
from pyFiles.scene.sceneFuncs import create_scene
import os
import numpy as np
import cv2


def scene_render(
        shapes: np.ndarray,
        materials: list,
        lights: list,
        eye_position: np.ndarray,
        scene_width: int, scene_height: int,
        fov_degree: float, depth_limit,
):
    if not os.path.exists("./logs"):
        os.mkdir("./logs")

    scene: np.ndarray = create_scene(scene_width, scene_height)
    scene = rendering_per_pixel(scene, shapes, fov_degree, materials, lights, eye_position)
    cv2.imshow("Scene render", cv2.cvtColor(scene.astype(np.uint8), cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)


__all__ = [
    "scene_render",
]