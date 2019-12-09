import numpy as np

from pyFiles.scene.utils import create_scene, gradient_filling, show_scene
from pyFiles.shapes.sphere import Sphere
from typing import NoReturn


__all__ = [
    "stage1"
]


def stage1(scene_width: int, scene_height: int) -> NoReturn:
    scene: np.ndarray = create_scene(width=scene_width,
                                     height=scene_height)
    gradient_filling(scene)
    show_scene(scene)
