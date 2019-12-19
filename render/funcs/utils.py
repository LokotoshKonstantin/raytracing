import cProfile
import os
import sys

import numpy as np

# Промежутки стен на плоскостях по X, Y, Z
X_RANGE = [0, (-550, 800)]
Y_RANGE = [1, (-390, 650)]
Z_RANGE = [2, (-250, 1000)]
# Для описаний уравнений плоскости
SHIFTS = [(-550, 0, Y_RANGE, Z_RANGE), (800, 0, Y_RANGE, Z_RANGE),
          (650, 1, X_RANGE, Z_RANGE), (-390, 1, X_RANGE, Z_RANGE),
          (-250, 2, X_RANGE, Y_RANGE)]
# Материалы стен
MATERIALS = [
    [np.array([15, 76, 129]), 0.9, 0.1, 0., 10.],
    [np.array([252, 102, 112]), 0.9, 0.1, 0., 10.],
    [np.array([3, 153, 141]), 0.9, 0.1, 0., 10.],
    [np.array([102, 2, 60]), 0.4, 0.4, 0.9, 2000.],
    [np.array([223, 230, 234]), 0.4, 0.4, 0.9, 2000.]
]
# Нормали к стенам
NORMALS = [
    np.array([1, 0, 0]),
    np.array([-1, 0, 0]),
    np.array([0, -1, 0]),
    np.array([0, 1, 0]),
    np.array([0, 0, 1])
]
# Граница обзора
VIEW_DISTANCE_BORDER = 10000


def intersect_any(orig: np.ndarray, direction: np.ndarray, spheres: np.ndarray, materials: list):
    """
    Вычисление пересечений с объектами
    orig - откуда смотрим, точка
    direction - куда смотрим, вектор
    shapes - описания сфер
    materials - описания материалов, кол-во соотносится с кол-вом сфер
    """
    distances: np.ndarray = np.zeros(shape=spheres.shape[0])
    for i in range(spheres.shape[0]):
        # В README на странице репозитория есть ссылка на статью с описанием метода нахождения пересечений.
        # Там достаточно подробно изложен подход, этот код является адаптацией кода оттуда.
        l = spheres[i, :3] - orig
        tca = np.vdot(l, direction)
        d2 = np.vdot(l, l) - tca * tca
        r2 = spheres[i, 3] * spheres[i, 3]
        if d2 > r2:
            distances[i] = float(sys.maxsize - 1)
            continue

        thc: float = np.sqrt(r2 - d2)
        t0: float = tca - thc
        t1: float = tca + thc

        if t0 > t1:
            t0, t1 = t1, t0

        if t0 < 0:
            t0 = t1
            if t0 < 0:
                distances[i] = float(sys.maxsize - 1)
                continue
        distances[i] = t0

    min_distance: float = min(distances)
    closest_shape_ind: int = np.argmin(distances)
    hit: np.ndarray = orig + direction * min_distance
    normal: np.ndarray = hit - spheres[closest_shape_ind, :3]
    material: np.ndarray = materials[closest_shape_ind]

    # Цикл в котором определяется пересечение со стенами:
    # лежит ли точка в определенных границах плоскости с определенным уравнением
    for ind, shift_info in enumerate(SHIFTS):
        # Уравнение плоскости
        d: float = -1. * (orig[shift_info[1]] - shift_info[0]) / direction[shift_info[1]]
        point: np.ndarray = orig + direction * d
        # Границы на плоскости
        if shift_info[2][1][0] < point[shift_info[2][0]] < shift_info[2][1][1]:
            if shift_info[3][1][0] < point[shift_info[3][0]] < shift_info[3][1][1]:
                if 0 < d < min_distance:
                    return d <= VIEW_DISTANCE_BORDER, MATERIALS[ind], NORMALS[ind], point
    return min_distance <= VIEW_DISTANCE_BORDER, material, normal, hit


# Вызов декоратора для логирования вычислительной нагрузки на код (кол-во вызовов, время внутри и тд).
# Результаты в папке logs
def profile(func):
    def wrapper(*args, **kwargs):
        profile_filename = os.path.join("logs", func.__name__ + ".prof")
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        return result

    return wrapper
