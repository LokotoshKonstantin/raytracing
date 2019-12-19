from typing import List

import numpy as np

from render.funcs.utils import intersect_any
from render.funcs.utils import profile

DEPTH_LIMIT = 3
BACKGROUND_COLOR = np.array([0, 0, 0], dtype=np.uint8)
REFLECTION_MULT = 1.
FLARE_MULT = 1.


def raytracer(orig: np.ndarray, direction: np.ndarray, shapes: np.ndarray,
              materials: List[list],
              lights: List[np.ndarray], depth: int) -> np.ndarray:
    """
    Вычилсение всего светового влияния на пиксель
    orig - откуда смотрим, точка
    direction - куда смотрим, вектор
    shapes - описания сфер
    materials - описания материалов, кол-во соотносится с кол-вом сфер
    lights - описания источников света
    """
    if depth > DEPTH_LIMIT:
        # При калькуляции отрвженного света параметр глубины определяет
        # как много преломлений пройдет луч перед тем как упадет на объект.
        # При отражении не от зеркального объекта даст его отражение,
        # при отражении от зеркального объекта будет получено отражение отражения.
        # Чем выше значение глубины, тем более глубокой будет рекурсия отражений.
        return BACKGROUND_COLOR
    else:
        # Просчет пересечения луча обзора со всеми объектами сцены. В данном случае, шары и стены.
        # Возвращает характеристики объекта, попавшего в поле зрения: характеристики материала, нормаль к точке,
        # саму точку (близжайшую к камере - аналог Z буфера)
        intersected_any, material, normal, point = intersect_any(orig, direction, shapes, materials)

        # Если ничего не видно
        if not intersected_any:
            return BACKGROUND_COLOR

        normal = normal / np.linalg.norm(normal)
        light_intensity: float = 0  # Интенсивность основного цвета
        specular_light_intensity: float = 0  # Интенсивность света блика

        # Вычисление отраженного луча света
        reflect_dir: np.ndarray = direction - normal * 2. * np.vdot(direction, normal)
        reflect_orig: np.ndarray = point + normal * 0.001
        if np.vdot(reflect_dir, normal) < 0:
            reflect_orig = point - normal * 0.001
        if material[
            3] > 0.1:  # Небольшой чит:если материал объекта не предполагает отражение, то мы не прослеживаем путь луча
            reflect_color: np.ndarray = raytracer(reflect_orig, reflect_dir, shapes, materials, lights, depth + 1)
        else:
            reflect_color: np.ndarray = BACKGROUND_COLOR

        # Калькуляция света от всех источников
        for light in lights:

            # Вектор от света на точку
            light_dir: np.ndarray = light[:3] - point
            light_distance: float = np.linalg.norm(light_dir)
            light_dir: np.ndarray = light_dir / light_distance

            # Просчет теней: вычисляется пересечение прямой от точки в источнику света.
            # то точка считается затененной
            shadow_orig: np.ndarray = point + normal * 0.001
            if np.vdot(light_dir, normal) < 0:
                shadow_orig = point - normal * 0.001
            shadow_intersect, _, _, shadow_point = intersect_any(shadow_orig, light_dir, shapes, materials)
            if shadow_intersect and np.linalg.norm(shadow_point - shadow_orig) < light_distance:
                continue

            # освещение по Фонгу
            scalar_product: float = np.vdot(light_dir, normal)
            light_intensity += light[3] * max(0.0, scalar_product)
            power: float = light_dir - normal * 2. * scalar_product
            power = max(0., np.vdot(power, direction))
            specular_light_intensity += pow(power, material[4]) * light[3]

        color1 = material[0] * light_intensity * material[1]  # Освещенный цвет объекта
        color2 = np.array([255., 255., 255.], dtype=np.float) * specular_light_intensity * material[
            2] * FLARE_MULT  # Блик
        color3 = reflect_color * material[3] * REFLECTION_MULT  # Зеркальность
        return color1 + color2 + color3


@profile
def rendering_per_pixel(scene: np.ndarray, shapes: np.ndarray, fov_degree: float,
                        materials: list,
                        lights: List[np.ndarray],
                        eye_position: np.ndarray) -> np.ndarray:
    """
    Просчет освещения для каждого пикселя. С учетом отражений, теней и засвета.
    """
    global DEPTH_LIMIT
    h: int = scene.shape[0]
    w: int = scene.shape[1]

    # Настройки параметров отображения сцены: угол обзора, машстаб относительно угла обзора
    fov: float = np.deg2rad(fov_degree)
    scale: float = np.tan(fov * 0.5)
    imageAspectRatio: float = float(w) / float(h)

    for i in range(0, h):
        for j in range(0, w):
            # Вычисление фактических координат в рамках сцены по положению пикселя
            x: float = (2 * (i + 0.5) / float(w) - 1) * scale
            y: float = (1 - 2 * (j + 0.5) / float(h)) * scale * (1. / imageAspectRatio)

            # Направление обзора на координаты в сцене. -1 берется из направления обзора вдоль по отрицательному Z.
            direction: np.ndarray = np.array([y, x, -1.], dtype=float)
            direction = direction / np.linalg.norm(direction)
            scene[i, j] = raytracer(eye_position, direction, shapes, materials, lights, 0)

    return np.clip(scene, 0, 255).astype(np.uint8)

