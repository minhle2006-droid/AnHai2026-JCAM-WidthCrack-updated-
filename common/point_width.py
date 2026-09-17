

import numpy as np
from itertools import combinations

from common.geometry_utils import polygon_edges


def _segment_through_point(p, seg_a, seg_b, seg_c, seg_d):

    from scipy.optimize import minimize_scalar

    seg_a, seg_b = np.asarray(seg_a, float), np.asarray(seg_b, float)
    seg_c, seg_d = np.asarray(seg_c, float), np.asarray(seg_d, float)
    p = np.asarray(p, float)

    def eval_at(t):
        """t in [0,1]: điểm u trên cạnh 1; trả về v trên cạnh 2 nếu p nằm giữa u,v."""
        u = seg_a + t * (seg_b - seg_a)
        du = u - p
        norm = np.linalg.norm(du)
        if norm < 1e-12:
            return None
        d = du / norm
        # tia đối: p - s*d, s>0, cắt cạnh 2 tại v = seg_c + r*(seg_d-seg_c)
        # giải: p - s*d = seg_c + r*(seg_d - seg_c)
        A = np.array([[-d[0], -(seg_d - seg_c)[0]],
                      [-d[1], -(seg_d - seg_c)[1]]])
        rhs = seg_c - p
        det = np.linalg.det(A)
        if abs(det) < 1e-12:
            return None
        s, r = np.linalg.solve(A, rhs)
        if s > 1e-9 and -1e-9 <= r <= 1 + 1e-9:
            v = seg_c + r * (seg_d - seg_c)
            return u, v
        return None

    def length_at(t):
        res = eval_at(t)
        if res is None:
            return 1e9
        u, v = res
        return np.linalg.norm(u - v)

    result = minimize_scalar(length_at, bounds=(0, 1), method="bounded")
    if result.fun >= 1e8:
        return None
    u, v = eval_at(result.x)
    return u, v


def width_at_point_polygon(p, vertices):
  
    edges = polygon_edges(vertices)
    best = None
    best_uv = None

    for (a1, b1), (a2, b2) in combinations(edges, 2):
        res = _segment_through_point(p, a1, b1, a2, b2)
        if res is None:
            continue
        u, v = res
        length = np.linalg.norm(u - v)
        if best is None or length < best:
            best = length
            best_uv = (u, v)

    if best is None:
        raise ValueError("Không tìm được u*, v* — kiểm tra p có thuộc int(S) không.")

    return best, best_uv[0], best_uv[1]
