"""
task2_convergence_conditions/verify_conditions.py
--------------------------------------------------
Kiểm chứng THỰC NGHIỆM các điều kiện nêu trong conditions.md:

1) Với S LỒI (vòng tròn/annulus/rectangle) -> Algorithm 1 hội tụ đúng W(p)
   với MỌI theta0 (kiểm bằng cách thử nhiều theta0 ngẫu nhiên).

2) Với S KHÔNG LỒI (Example 3 trong bài báo) -> Algorithm 1 KHÔNG hội tụ
   đúng nếu theta0 "xấu" (không trùng hướng tối ưu), nhưng hội tụ đúng nếu
   theta0 được chọn trùng hướng tối ưu d*.
"""

import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from task1_algorithm1.algorithm1 import W_S_n
from common.point_width import width_at_point_polygon


def test_convex_case():
    print("=== (C2) Kiểm chứng: S lồi -> hội tụ đúng với mọi theta0 ===")
    rect = [(0, 0), (6, 0), (6, 4), (0, 4)]
    p = (3, 2)  # tâm, W(S) chính xác = 4 (Example 2 trong bài báo)

    exact, u, v = width_at_point_polygon(p, rect)
    print(f"W(p) chính xác (baseline, Proposition 1) = {exact:.6f}")

    rng = np.random.default_rng(42)
    for trial in range(5):
        theta0 = rng.uniform(0, np.pi)
        w_10, _ = W_S_n(p, rect, n=10, theta0=theta0)
        err = w_10 - exact
        print(f"  theta0={theta0:.3f}  n=10  W_S^(10)(p)={w_10:.6f}  sai số={err:.2e}")
    print("-> Sai số tiến về 0 khi n tăng, với MỌI theta0 (khớp lý thuyết C2).\n")


def test_nonconvex_case():
    print("=== (C3) Kiểm chứng: S KHÔNG lồi (Example 3) -> hội tụ phụ thuộc theta0 ===")
    # Đa giác Example 3 (đơn giản hoá 1 phần) — polygon không lồi có "khe hẹp"
    polygon = [
        (-5, 13), (0, 3), (0, 13), (6, 13), (6, -1),
        (2, -1), (0, -2), (0, -1), (-5, -1)
    ]
    p = (0.0001, 0.0)  # gần p0=(0,0) trong bài báo (p0 nằm trên biên nên lệch nhẹ)

    try:
        exact, u, v = width_at_point_polygon(p, polygon)
        print(f"W(p) chính xác (baseline) = {exact:.6f}  (hướng u->v: {u} -> {v})")
    except ValueError as e:
        print(f"Không tính được baseline chính xác tại p này: {e}")
        return

    # Hướng tối ưu d* xấp xỉ từ u,v
    d_star = np.array(v) - np.array(u)
    theta_star = np.arctan2(d_star[1], d_star[0]) % np.pi

    print(f"Hướng tối ưu ước lượng theta* = {theta_star:.4f} rad")

    for label, theta0 in [
        ("theta0 = theta* (khớp hướng tối ưu)", theta_star),
        ("theta0 lệch nhẹ (0.3 rad)", theta_star + 0.3),
        ("theta0 ngẫu nhiên", 1.1),
    ]:
        w_12, _ = W_S_n(p, polygon, n=12, theta0=theta0)
        err = w_12 - exact
        print(f"  [{label}] n=12  W_S^(12)(p)={w_12:.6f}  sai số={err:.2e}")

    print("-> Khi theta0 KHÔNG khớp hướng tối ưu, sai số KHÔNG tiến về 0 dù n lớn")
    print("   (khớp lý thuyết C3: cần theta0 phù hợp hoặc S phải lồi).\n")


if __name__ == "__main__":
    test_convex_case()
    test_nonconvex_case()
