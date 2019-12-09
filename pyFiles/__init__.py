import numpy as np

from pyFiles.scene.sceneFuncs import create_scene, show_scene
from pyFiles.render.renderingFuncs import gradient_filling, simple_sphere_rendering, simple_shapes_rendering
from pyFiles.shapes.sphere import Sphere
from pyFiles.shapes.shapesContainer import ShapesContainer
from typing import NoReturn, Union


__all__ = [
    "stage1",
    "stage2",
    "stage3"
]


def stage1(scene_width: int, scene_height: int) -> NoReturn:
    scene: np.ndarray = create_scene(width=scene_width,
                                     height=scene_height)
    gradient_filling(scene)
    show_scene(scene, "Stage 1")
    del scene


def stage2(scene_width: int, scene_height: int,
           sphere_center: np.ndarray, sphere_radius: float,
           eye_position: np.ndarray,
           fov_degree: float,
           sphere_color: np.ndarray, background_color: np.ndarray) -> NoReturn:

    scene: np.ndarray = create_scene(width=scene_width,
                                     height=scene_height)

    sphere: Sphere = Sphere(center=sphere_center,
                            radius=sphere_radius)

    simple_sphere_rendering(scene=scene, sphere=sphere,
                            fov_degree=fov_degree, eye_position=eye_position,
                            sphere_color=sphere_color,
                            background_color=background_color)

    show_scene(scene=scene, window_title="Stage 2")

    del scene


def stage3(scene_width: int, scene_height: int,
           spheres_centers: np.ndarray, spheres_radiuses: list,
           eye_position: np.ndarray,
           fov_degree: float,
           sphere_color: np.ndarray, background_color: np.ndarray) -> NoReturn:
    scene: np.ndarray = create_scene(width=scene_width,
                                     height=scene_height)

    shapes: ShapesContainer = ShapesContainer(1000)
    for i in range(0, len(spheres_radiuses)):
        shapes.append(Sphere(center=spheres_centers[i], radius=spheres_radiuses[i]))

    simple_shapes_rendering(scene=scene, shapes=shapes,
                            fov_degree=fov_degree, eye_position=eye_position,
                            sphere_color=sphere_color,
                            background_color=background_color)

    show_scene(scene=scene, window_title="Stage 3")

    del scene
