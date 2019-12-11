# cython: language_level=3
cimport numpy as np
import sys
import math
import numpy as np

cdef list X_RANGE = [0, (-550, 800)]
cdef list Y_RANGE = [1, (-390, 650)]
cdef list Z_RANGE = [2, (-250, 1000)]
cdef list SHIFTS = [(-550, 0, Y_RANGE, Z_RANGE), (800, 0, Y_RANGE, Z_RANGE),
          (650, 1, X_RANGE, Z_RANGE), (-390, 1, X_RANGE, Z_RANGE),
          (-250, 2, X_RANGE, Y_RANGE)]
cdef list MATERIALS = [
    [np.array([15, 76, 129]), 0.9, 0.1, 0., 10.],
    [np.array([252, 102, 112]), 0.9, 0.1, 0., 10.],
    [np.array([3, 153, 141]), 0.9, 0.1, 0.1, 0., 10.],
    [np.array([102, 2, 60]), 0.9, 0.1, 0., 10.],
    [np.array([223, 230, 234]), 0.4, 0.4, 0.9, 2000.]
]
cdef list NORMALS = [
    np.array([1, 0, 0]),
    np.array([-1, 0, 0]),
    np.array([0, -1, 0]),
    np.array([0, 1, 0]),
    np.array([0, 0, 1])
]
cdef int VIEW_DISTANCE_BORDER = 10000
cdef int DEPTH_LIMIT = 3
cdef np.ndarray BACKGROUND_COLOR = np.array([0, 0, 0], dtype=np.uint8)
cdef float REFLECTION_MULT = 1.
cdef float FLARE_MULT = 1.


cpdef float vdot(np.ndarray v1, np.ndarray v2):
    cdef int i
    cdef float result = 0.0
    for i in range(v1.shape[0]):
        result += v1[i] * v2[i]
    return result


cpdef tuple intersect_any(np.ndarray orig, np.ndarray direction, np.ndarray spheres, list materials):

    cdef list distances = []
    cdef int i
    cdef np.ndarray l
    cdef float tca
    cdef float d2
    cdef float r2
    cdef float thc
    cdef float t0
    cdef float t1
    for i in range(spheres.shape[0]):
        l = spheres[i, :3] - orig
        tca = np.vdot(l, direction)
        d2 = np.vdot(l, l) - tca * tca
        r2 = spheres[i, 3] * spheres[i, 3]
        if d2 > r2:
            distances.append(float(sys.maxsize - 1))
            continue

        thc = (r2 - d2) ** (1 / 2.)
        t0 = tca - thc
        t1 = tca + thc

        if t0 > t1:
            t0, t1 = t1, t0

        if t0 < 0:
            t0 = t1
            if t0 < 0:
                distances.append(float(sys.maxsize - 1))
                continue
        distances.append(t0)

    cdef float min_distance = min(distances)
    cdef int closest_shape_ind = distances.index(min_distance)
    cdef np.ndarray hit = orig + direction * min_distance
    cdef np.ndarray normal = hit - spheres[closest_shape_ind, :3]
    cdef list material = materials[closest_shape_ind]

    cdef float d
    cdef int ind
    cdef tuple shift_info
    cdef np.ndarray point
    for ind, shift_info in enumerate(SHIFTS):
        d = -1. * (orig[shift_info[1]] - shift_info[0]) / direction[shift_info[1]]
        point = orig + direction * d
        if shift_info[2][1][0] < point[shift_info[2][0]] < shift_info[2][1][1]:
            if shift_info[3][1][0] < point[shift_info[3][0]] < shift_info[3][1][1]:
                if 0 < d < min_distance:
                    return d <= VIEW_DISTANCE_BORDER, MATERIALS[ind], NORMALS[ind], point
    return min_distance <= VIEW_DISTANCE_BORDER, material, normal, hit


cpdef np.ndarray raytracer(np.ndarray orig, np.ndarray direction, np.ndarray shapes, list materials,
                           list lights, int depth):
    if depth > DEPTH_LIMIT:
        return BACKGROUND_COLOR

    cdef bint intersected_any
    cdef list material
    cdef np.ndarray normal
    cdef np.ndarray point
    intersected_any, material, normal, point = intersect_any(orig, direction, shapes, materials)
    if not intersected_any:
        return BACKGROUND_COLOR

    normal = normal / np.linalg.norm(normal)
    cdef float light_intensity = 0
    cdef float specular_light_intensity = 0

    cdef np.ndarray reflect_dir = direction - normal * 2. * np.vdot(direction, normal)
    cdef np.ndarray reflect_orig = point + normal * 0.001
    if np.vdot(reflect_dir, normal) < 0:
        reflect_orig = point - normal * 0.001

    cdef np.ndarray reflect_color
    if material[3] > 0.1:
        reflect_color = raytracer(reflect_orig, reflect_dir, shapes, materials, lights, depth + 1)
    else:
        reflect_color = BACKGROUND_COLOR

    cdef np.ndarray light_dir
    cdef float light_distance
    cdef np.ndarray shadow_orig
    cdef bint shadow_intersect
    cdef np.ndarray shadow_point
    cdef float scalar_product
    cdef np.ndarray ref_light
    cdef float power

    for light in lights:

        light_dir = light[:3] - point
        light_distance = np.linalg.norm(light_dir)
        light_dir = light_dir / light_distance

        shadow_orig = point + normal * 0.001
        if np.vdot(light_dir, normal) < 0:
            shadow_orig = point - normal * 0.001
        shadow_intersect, _, _, shadow_point = intersect_any(shadow_orig, light_dir, shapes, materials)
        if shadow_intersect and np.linalg.norm(shadow_point - shadow_orig) < light_distance:
            continue

        scalar_product = np.vdot(light_dir, normal)
        light_intensity += light[3] * max(0.0, scalar_product)
        ref_light = light_dir - normal * 2. * scalar_product
        power = max(0., np.vdot(ref_light, direction))
        specular_light_intensity += pow(power, material[4]) * light[3]

    cdef np.ndarray color1 = material[0] * light_intensity * material[1]
    cdef np.ndarray color2 = np.array([255., 255., 255.], dtype=np.float) * specular_light_intensity * material[2] * FLARE_MULT
    cdef np.ndarray color3 = reflect_color * material[3] * REFLECTION_MULT
    return color1 + color2 + color3
