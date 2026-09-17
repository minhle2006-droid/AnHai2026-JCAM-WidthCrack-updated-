"""
task3_width_of_subset/set_width_algorithm.py
---------------------------------------------
THUẬT TOÁN tính W(S;G) trong R^2, với G ⊂ S là một tập con (không chỉ 1 điểm).

Theo Definition 2:
    W(S; G) := sup_{p ∈ G} W(S; p)

Vì G có thể là tập vô hạn điểm (đường cong, skeleton, đoạn thẳng, hợp hữu hạn
đoạn...), ta không thể tính sup chính xác bằng máy trong trường hợp tổng quát.
Thuật toán dưới đây XẤP XỈ W(S;G) bằng cách:

  1. RỜI RẠC HOÁ G thành lưới điểm hữu hạn {p_1,...,p_m} (mật độ càng cao,
     xấp xỉ càng tốt — xem `discretize_G`).
  2. Với MỖI p_k, tính W(S; p_k) — dùng Algorithm 1 (xấp xỉ, task1) hoặc công
     thức chính xác cho đa giác (`common/point_width.py`) nếu có thể.
  3. Lấy W(S;G) ≈ max_k W(S; p_k)   (Proposition 4: với G hữu hạn hợp các G_i,
     W(G) = max W(G_i); ta áp dụng ý tưởng này cho lưới rời rạc).

ĐỘ CHÍNH XÁC: theo Theorem 2(a), hàm G ↦ W(G) là lsc trên (F, d_H) (không gian
các tập đóng khác rỗng với metric Hausdorff). Do đó khi lưới điểm {p_k} hội tụ
tới G theo Hausdorff (d_H({p_k}, G) -> 0), ta có:

    liminf_m  max_k W(p_k)  >=  ... (cần cẩn trọng, xem GHI CHÚ dưới)

GHI CHÚ QUAN TRỌNG (đúng theo lý thuyết, không phóng đại):
  - `max_k W(p_k) <= W(G)` LUÔN đúng (vì {p_k} ⊂ G, theo tính chất hiển nhiên
    W(A) <= W(B) khi A ⊂ B, xem Proposition 4/lời chứng minh trong bài báo).
  - Nếu THÊM giả thiết p ↦ W(p) liên tục trên một tập đóng K ⊃ G (Theorem 2b),
    thì khi lưới điểm ngày càng dày, max_k W(p_k) -> W(G) (do compact + liên tục,
    hàm đạt max tại 1 điểm p* ∈ G và lưới điểm gần p* đủ dày sẽ có W(p_k) gần
    W(p*) = W(G)).
  - Nếu p ↦ W(p) KHÔNG liên tục trên G (chỉ lsc — Theorem 2a), việc rời rạc
    hoá có thể ĐÁNH GIÁ THẤP W(G) (under-estimate), vì (2) trong bài báo
    (Example 3) cho thấy sup có thể không đạt được tại bất kỳ điểm cụ thể nào
    của G, kể cả khi G compact.
"""

import numpy as np
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from common.point_width import width_at_point_polygon
from task1_algorithm1.algorithm1 import W_S_n


def discretize_G(G_description, num_points=200):
    """
    Rời rạc hoá G thành lưới điểm.

    G_description có thể là:
      - list các điểm (đã rời rạc sẵn, ví dụ skeleton từ ảnh) -> trả về nguyên vẹn
      - ('segment', p_start, p_end) -> lấy num_points điểm đều trên đoạn
      - ('polyline', [p0, p1, ..., pk]) -> lấy num_points điểm đều dọc theo polyline
    """
    if isinstance(G_description, tuple):
        kind = G_description[0]
        if kind == "segment":
            _, p_start, p_end = G_description
            p_start, p_end = np.array(p_start, float), np.array(p_end, float)
            ts = np.linspace(0, 1, num_points)
            return [tuple(p_start + t * (p_end - p_start)) for t in ts]

        elif kind == "polyline":
            _, pts = G_description
            pts = [np.array(pt, float) for pt in pts]
            seg_lengths = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
            total = sum(seg_lengths)
            n_per_seg = [max(2, int(round(num_points * L / total))) for L in seg_lengths]

            out = []
            for i, n_i in enumerate(n_per_seg):
                ts = np.linspace(0, 1, n_i, endpoint=(i == len(n_per_seg) - 1))
                for t in ts:
                    out.append(tuple(pts[i] + t * (pts[i + 1] - pts[i])))
            return out
        else:
            raise ValueError(f"Loại G_description không hỗ trợ: {kind}")

    # Nếu đã là list điểm sẵn (ví dụ skeleton pixel)
    return list(G_description)


def width_of_subset(S_vertices, G_description, num_points=200,
                     method="algorithm1", n_iter=10, theta0=0.0):
    """
    Tính W(S; G) ~ xấp xỉ theo thuật toán mô tả ở đầu file.

    Parameters
    ----------
    S_vertices : list đỉnh của đa giác S (biên ∂S)
    G_description : mô tả G (xem discretize_G)
    method : "algorithm1" (dùng Algorithm 1 xấp xỉ, nhanh, dùng được cho ảnh
             thực tế) hoặc "exact" (dùng width_at_point_polygon, chính xác
             nhưng chỉ chạy được khi S là đa giác đơn nhỏ)
    n_iter : số vòng lặp Algorithm 1 nếu method="algorithm1"
    theta0 : hướng khởi tạo cho Algorithm 1

    Returns
    -------
    W_G : float, xấp xỉ W(S;G)
    p_star : điểm trong lưới đạt max (ứng viên cho argmax)
    per_point : list (p_k, W(p_k)) toàn bộ lưới — để vẽ / phân tích
    """
    points = discretize_G(G_description, num_points=num_points)

    per_point = []
    for p in points:
        try:
            if method == "exact":
                w, _, _ = width_at_point_polygon(p, S_vertices)
            else:
                w, _ = W_S_n(p, S_vertices, n=n_iter, theta0=theta0)
        except ValueError:
            continue  # p có thể nằm ngoài int(S) hoặc suy biến -> bỏ qua
        per_point.append((p, w))

    if not per_point:
        raise ValueError("Không tính được W(p) cho bất kỳ điểm nào trong G.")

    p_star, W_G = max(per_point, key=lambda item: item[1])
    return W_G, p_star, per_point


if __name__ == "__main__":
    # Demo: tái hiện Example 3 / Fig. minh hoạ trong bài báo — G là 1 đoạn thẳng
    # [p0, p_{1/2}] trong ví dụ đa giác không lồi (Section 3, Example 3):
    polygon = [
        (-5, 13), (0, 3), (0, 13), (6, 13), (6, -1),
        (2, -1), (0, -2), (0, -1), (-5, -1)
    ]
    G = ("segment", (0.0001, 0.0), (0.5, 0.0))  # ~ [p0, p_{1/2}] (lệch nhẹ khỏi biên)

    W_G, p_star, per_point = width_of_subset(polygon, G, num_points=100, n_iter=10)

    print("=== Demo tính W(S;G) — G = đoạn [p0, p_1/2] (Example 3) ===")
    print(f"W(S;G) xấp xỉ = {W_G:.6f}  đạt tại p* = {p_star}")
    print(f"(Bài báo: W(G) = 5 = ||u_bar - b||, không đạt tại điểm cụ thể nào")
    print(f" khi G đóng — ở đây ta chỉ xấp xỉ bằng sup trên lưới rời rạc.)")
