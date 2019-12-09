import numpy as np
import math
from pyFiles import stage1, stage2


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


if __name__ == "__main__":
    main()