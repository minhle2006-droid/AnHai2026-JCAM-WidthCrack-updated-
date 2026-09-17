"""
task1_algorithm1/algorithm1.py
------------------------------
Triển khai lại ALGORITHM 1 trong tài liệu (An & Hai, 2026, Section 5.2):

    Data: n > 1, S, p
    Result: F(n)

    i <- 1
    Thêm đoạn i=1 qua p tạo 2 góc pi tại p
    num_angles <- 2
    for i <- 2 to n:
        for j <- 1 to num_angles/2:
            Thêm phân giác của angle_j
            Kéo dài phân giác thành đoạn chứa p ở phần trong
        num_angles <- 2^i
    num_segments <- 2^(n-1)

    => W_S^(n)(p) := min F(n)  xấp xỉ (từ trên) cho W_S(p).

CÂU HỎI 1: Thuật toán có hội tụ về nghiệm CHÍNH XÁC hay không?
---------------------------------------------------------------
KHÔNG đảm bảo tổng quát. Bài báo chỉ chứng minh (Proposition 7):

    lim_{n->∞} W_S^(n)(p) >= W_S(p)          (*)

tức dãy W_S^(n)(p) đơn điệu giảm (theo n tăng, số đoạn tăng gấp đôi, min
không tăng) và hội tụ, nhưng giới hạn CHỈ chặn trên W_S(p), KHÔNG chắc
BẰNG W_S(p).

Lý do: Algorithm 1 chỉ sinh ra 2^(n-1) HƯỚNG cụ thể quanh p — đó là các
hướng thu được bằng cách liên tục chia đôi góc bắt đầu từ 1 đường thẳng
tuỳ ý qua p. Đây là một lưới hướng RỜI RẠC và ĐỊNH TRƯỚC theo một quy
tắc hình học cố định (phân giác góc), không phải là "quét" tất cả các
hướng trong [0, pi). Trong khi đó, theo Definition 1:

    W(p) = inf{ ||u-v|| : u,v ∈ ∂S, p ∈ [u,v] }

infimum này lấy trên TẤT CẢ hướng (liên tục), và theo Proposition 1,
infimum đó đạt được tại một hướng d* xác định (có thể vô số hướng đạt
inf, nhưng nói riêng ít nhất một). Nếu hướng d* đó KHÔNG bao giờ xuất
hiện trong lưới hướng mà Algorithm 1 sinh ra (vì lưới hướng phụ thuộc
vào lựa chọn đoạn ban đầu i=1), thì với MỌI n, W_S^(n)(p) > W_S(p), và
dãy chỉ hội tụ về infimum của các giá trị corresponding với các hướng
trong lưới — có thể lớn hơn thực sự W_S(p).

=> Xem chứng minh/phản ví dụ chi tiết trong `../task2_convergence_conditions/`.
"""

import numpy as np
import matplotlib.pyplot as plt

from common.geometry_utils import closest_pair_straddling_p


def generate_directions(n, theta0=0.0):
    """
    Sinh 2^(n-1) HƯỚNG (không phải đoạn) quanh điểm p, theo đúng logic
    Algorithm 1: bắt đầu từ 1 đường thẳng (2 tia tạo góc pi ở 2 phía),
    sau đó liên tục chia đôi các góc.

    Vì các hướng chia đôi góc bắt đầu từ 1 đường thẳng ban đầu theo góc
    theta0 sẽ luôn tạo thành các góc CÁCH ĐỀU nhau pi/2^(n-1) (đây là hệ
    quả hình học của việc chia đôi liên tiếp một đường thẳng: kết quả
    luôn là một lưới góc đều), ta sinh trực tiếp:

        theta_k = theta0 + k * pi / 2^(n-1),   k = 0, 1, ..., 2^(n-1) - 1

    (mỗi theta_k cho một ĐƯỜNG THẲNG qua p, ứng với 1 "segment" trong F(n)).

    Trả về: mảng hướng (vector đơn vị) độ dài 2^(n-1).
    """
    num_segments = 2 ** (n - 1)
    thetas = theta0 + np.arange(num_segments) * np.pi / num_segments
    directions = np.stack([np.cos(thetas), np.sin(thetas)], axis=1)
    return directions


def F_n(p, vertices, n, theta0=0.0):
    """
    Tính tập F(n) = { ||u_i - v_i|| : i = 1..2^(n-1) } theo Algorithm 1.

    Trả về list các độ dài hợp lệ (bỏ qua hướng không cắt được ∂S đúng cách).
    """
    directions = generate_directions(n, theta0=theta0)
    lengths = []
    segments = []  # để vẽ minh hoạ
    for d in directions:
        res = closest_pair_straddling_p(p, d, vertices)
        if res is None:
            continue
        u, v, length = res
        lengths.append(length)
        segments.append((u, v))
    return lengths, segments


def W_S_n(p, vertices, n, theta0=0.0):
    """W_S^(n)(p) := min F(n)  — xấp xỉ Algorithm 1 sau n vòng lặp."""
    lengths, segments = F_n(p, vertices, n, theta0=theta0)
    if not lengths:
        raise ValueError("Không sinh được đoạn hợp lệ nào qua p.")
    idx = int(np.argmin(lengths))
    return lengths[idx], segments[idx]


def convergence_curve(p, vertices, n_max=10, theta0=0.0):
    """Trả về danh sách (n, W_S^(n)(p)) để khảo sát tính đơn điệu & hội tụ."""
    out = []
    for n in range(1, n_max + 1):
        w, _ = W_S_n(p, vertices, n, theta0=theta0)
        out.append((n, w))
    return out


def plot_convergence(p, vertices, n_max=10, theta0=0.0, exact_value=None,
                      title="Hội tụ của W_S^(n)(p) theo n"):
    curve = convergence_curve(p, vertices, n_max=n_max, theta0=theta0)
    ns = [c[0] for c in curve]
    ws = [c[1] for c in curve]

    plt.figure(figsize=(6, 4))
    plt.plot(ns, ws, "o-", label=r"$W_S^{(n)}(p)$ (Algorithm 1)")
    if exact_value is not None:
        plt.axhline(exact_value, color="red", linestyle="--",
                     label=r"$W_S(p)$ chính xác")
    plt.xlabel("n (số vòng lặp)")
    plt.ylabel("Độ rộng xấp xỉ")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt.gcf()


if __name__ == "__main__":
    # Demo: hình chữ nhật a=6, b=4 (Example 2 trong bài báo), p = tâm (3,2)
    rect = [(0, 0), (6, 0), (6, 4), (0, 4)]
    p = (3, 2)

    print("=== Demo Algorithm 1 trên hình chữ nhật a=6, b=4 ===")
    for n in range(1, 8):
        w, (u, v) = W_S_n(p, rect, n)
        print(f"n={n:2d}  num_segments={2**(n-1):4d}   W_S^(n)(p) = {w:.6f}")

    # Với p = tâm hình chữ nhật, W(S) chính xác = b = 4 (theo Example 2)
    fig = plot_convergence(p, rect, n_max=8, exact_value=4.0,
                            title="Rectangle a=6,b=4 — p=(3,2)")
    fig.savefig("task1_algorithm1/convergence_rectangle_center.png", dpi=150)
    print("\nĐã lưu hình: task1_algorithm1/convergence_rectangle_center.png")
    print("Nhận xét: tại tâm hình chữ nhật, mọi hướng đối xứng => Algorithm 1")
    print("hội tụ đúng về W(S)=4 rất nhanh (n nhỏ đã chính xác).")
    print("Xem task2_convergence_conditions/counterexample.ipynb cho trường hợp")
    print("KHÔNG hội tụ về giá trị đúng khi p không có tính đối xứng thuận lợi.")
