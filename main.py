import numpy as np
import math
from pyFiles import stage1, stage2, stage3, stage4, stage5, stage6


def main():

    scene_width = 1024
    scene_height = 768

    stage1(scene_width, scene_height)

    # y, x, z
    sphere_center = np.array([42, 35, 0])
    sphere_radius = 125

    eye_position = np.array([300, 300, 1000])
    fov_degree = np.rad2deg(math.pi / 2.)

    sphere_color = np.array([255, 0, 0])
    background_color = np.array([255, 255, 255])

    stage2(scene_width, scene_height, sphere_center, sphere_radius, eye_position, fov_degree,
           sphere_color, background_color)

    spheres_centers = np.array([
        [42, 35, 0],
        [350, 42, -10],
        [112, 567, 10],
    ])
    spheres_radiuses = [125, 100, 234]
    stage3(scene_width, scene_height, spheres_centers, spheres_radiuses, eye_position, fov_degree,
           sphere_color, background_color)

    colors = np.array([
        [255, 0, 0],
        [0, 255, 0],
        [0, 0, 255]
    ], dtype=np.uint8)
    light_sources = np.array([
        [scene_height / 2, 0, 0, 1],
        [1, 1, 1, 1]
    ], dtype=int)
    stage4(scene_width, scene_height, spheres_centers, spheres_radiuses, colors, eye_position, fov_degree,
           light_sources)

    albedos = np.array([
        [0.6, 0.3, 0.1],
        [0.9, 0.1, 0.0],
        [0.5, 0.5, 0.9]
    ])
    spec_exponents = [50., 10., 2000.]
    stage5(scene_width, scene_height, spheres_centers, spheres_radiuses, colors, albedos, spec_exponents, eye_position,
           fov_degree, light_sources)

    depth_limit = 3

    stage6(scene_width, scene_height, spheres_centers, spheres_radiuses, colors, albedos, spec_exponents, eye_position,
           fov_degree, light_sources, depth_limit)


if __name__ == "__main__":
    main()
