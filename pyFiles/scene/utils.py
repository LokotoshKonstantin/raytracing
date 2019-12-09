import numpy as np
import cv2
from typing import NoReturn


def create_scene(width: int, height: int) -> np.ndarray:
    """

    :param width:
    :param height:
    :return:
    """
    return np.zeros(shape=(height, width, 3), dtype=np.uint8)


def show_scene(scene: np.ndarray) -> NoReturn:
    """

    :param scene:
    :return:
    """
    cv2.imshow("Rendering window", scene)
    cv2.waitKey(0)


def gradient_filling(scene: np.ndarray) -> NoReturn:
    """

    :param scene:
    :return:
    """
    h: int = scene.shape[0]
    w: int = scene.shape[1]
    for i in range(0, scene.shape[0]):
        for j in range(0, scene.shape[1]):
            scene[i, j] = np.array([round((i / float(h)) * 255),
                                    round((j / float(w)) * 255),
                                    0],
                                   dtype=np.uint8)
