"""
geometry_utils.py
------------------
Các hàm hình học cơ bản dùng chung cho toàn bộ repo:
- Biểu diễn đa giác đơn S bởi danh sách đỉnh (biên ∂S).
- Giao điểm của một tia/đường thẳng qua điểm p với biên ∂S.
- Kiểm tra điểm nằm trong / trên biên đa giác.

"""

import numpy as np


def polygon_edges(vertices):
    """Trả về danh sách các cạnh (đoạn thẳng) của đa giác, mỗi cạnh là (A, B)."""
    n = len(vertices)
    return [(np.array(vertices[i]), np.array(vertices[(i + 1) % n])) for i in range(n)]


def is_point_inside_polygon(point, vertices):
    """Kiểm tra điểm p có nằm trong đa giác (ray casting), dùng cho việc lọc p ∈ int S."""
    x, y = point
    n = len(vertices)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = vertices[i]
        xj, yj = vertices[j]
        if ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / (yj - yi + 1e-15) + xi
        ):
            inside = not inside
        j = i
    return inside


def ray_segment_intersection(p, direction, seg_a, seg_b):
   
    p = np.asarray(p, dtype=float)
    d = np.asarray(direction, dtype=float)
    a = np.asarray(seg_a, dtype=float)
    b = np.asarray(seg_b, dtype=float)

    e = b - a
    # Giải hệ: p + t*d = a + s*e  ->  t*d - s*e = a - p
    A = np.array([[d[0], -e[0]], [d[1], -e[1]]])
    rhs = a - p
    det = np.linalg.det(A)
    if abs(det) < 1e-12:
        return None  # song song hoặc trùng
    t, s = np.linalg.solve(A, rhs)
    if t > 1e-9 and -1e-9 <= s <= 1 + 1e-9:
        point = p + t * d
        return t, point
    return None


def line_boundary_intersections(p, direction, vertices):
  
    pts = []
    for seg_a, seg_b in polygon_edges(vertices):
        for sign in (1, -1):
            hit = ray_segment_intersection(p, sign * np.asarray(direction), seg_a, seg_b)
            if hit is not None:
                t, pt = hit
                pts.append((sign * t, pt))
    return pts


def closest_pair_straddling_p(p, direction, vertices):
   
    hits = line_boundary_intersections(p, direction, vertices)
    if not hits:
        return None

    pos_side = [(t, pt) for t, pt in hits if t > 1e-9]
    neg_side = [(t, pt) for t, pt in hits if t < -1e-9]

    if not pos_side or not neg_side:
        return None

    # điểm gần p nhất về mỗi phía
    t_pos, u = min(pos_side, key=lambda x: x[0])
    t_neg, v = max(neg_side, key=lambda x: x[0])  # t âm, gần 0 nhất => max

    return u, v, float(np.linalg.norm(u - v))
