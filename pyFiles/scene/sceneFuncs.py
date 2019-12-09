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


def show_scene(scene: np.ndarray, window_title: str) -> NoReturn:
    """

    :param scene:
    :param window_title:
    :return:
    """
    cv2.imshow(window_title, cv2.cvtColor(scene.astype(np.uint8), cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)

