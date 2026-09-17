"""
task4_selfhealing_application/make_synthetic_sample.py
----------------------------------------------------------
Tạo bộ ảnh MÔ PHỎNG vết nứt "co lại" theo thời gian (giả lập self-healing),
dùng để TEST pipeline (preprocessing -> run_algorithm1_on_cracks ->
healing_progress_analysis) khi chưa tải được dataset thật của
Jakubowski & Tomczak (2025).

Sinh ra data/raw/specimenA_t{0,1,2,3}.png với độ rộng vết nứt giảm dần.
"""

import os
import numpy as np
import cv2


def make_crack_image(width_px, size=(400, 200), noise=3):
    """Vẽ 1 vết nứt hình sin nằm ngang, độ rộng `width_px`, nền xám sáng."""
    h, w = size
    img = np.full((h, w), 220, dtype=np.uint8)  # nền bê tông sáng

    xs = np.arange(w)
    ys_center = h // 2 + (10 * np.sin(xs / 30.0)).astype(int)

    for x, yc in zip(xs, ys_center):
        y0 = max(0, yc - width_px // 2)
        y1 = min(h, yc + width_px // 2 + 1)
        img[y0:y1, x] = 40  # vết nứt tối

    # thêm nhiễu nhẹ giống ảnh scan thật
    noise_arr = np.random.normal(0, noise, img.shape)
    img = np.clip(img.astype(float) + noise_arr, 0, 255).astype(np.uint8)
    return img


def generate_sequence(out_dir, widths_px=(10, 7, 5, 2), specimen="specimenA"):
    os.makedirs(out_dir, exist_ok=True)
    for t, w_px in enumerate(widths_px):
        img = make_crack_image(w_px)
        path = os.path.join(out_dir, f"{specimen}_t{t}.png")
        cv2.imwrite(path, img)
        print(f"Đã tạo {path}  (độ rộng mô phỏng ~ {w_px}px)")


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "data", "raw")
    generate_sequence(out_dir)
    print("\nBây giờ có thể chạy thử:")
    print("  python task4_selfhealing_application/run_algorithm1_on_cracks.py")
    print("  python task4_selfhealing_application/healing_progress_analysis.py")
