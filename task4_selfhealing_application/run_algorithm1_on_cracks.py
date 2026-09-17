"""
task4_selfhealing_application/run_algorithm1_on_cracks.py
------------------------------------------------------------
Áp dụng Algorithm 1 (task1_algorithm1) + thuật toán W(S;G) (task3) lên
ảnh vết nứt thực tế (đã tiền xử lý bởi preprocessing.py), tại MỘT mốc thời
gian quan sát. Kết quả W(p) tại từng điểm skeleton + W(S;G) tổng hợp được
lưu ra CSV để dùng trong healing_progress_analysis.py.

Đơn vị: pixel. Cần hệ số chuyển đổi pixel -> mm (từ metadata ảnh / thang đo
trong dataset Jakubowski & Tomczak) để so sánh với reference_measurements.csv.
"""

import os
import sys
import csv
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from task4_selfhealing_application.preprocessing import process_image
from task1_algorithm1.algorithm1 import W_S_n
from task3_width_of_subset.set_width_algorithm import width_of_subset


def analyze_single_image(image_path, n_iter=10, theta0=0.0,
                          skeleton_subsample=1, pixel_to_mm=None):
    """
    Chạy pipeline đầy đủ trên 1 ảnh:
      1. Tiền xử lý -> vertices (biên ∂S), skeleton_points (G)
      2. Với mỗi điểm p trên skeleton (có thể subsample để giảm thời gian
         chạy), tính W(p) bằng Algorithm 1.
      3. W(S;G) = max_p W(p)  (Task 3)

    Trả về dict kết quả (per_point, W_G, p_star, pixel_to_mm).
    """
    proc = process_image(image_path)
    vertices = proc["vertices"]
    skeleton_points = proc["skeleton_points"][::skeleton_subsample]

    per_point = []
    for p in skeleton_points:
        try:
            w, _ = W_S_n(p, vertices, n=n_iter, theta0=theta0)
        except (ValueError, np.linalg.LinAlgError):
            continue
        per_point.append((p, w))

    if not per_point:
        raise ValueError(f"Không tính được W(p) nào cho ảnh: {image_path}")

    p_star, W_G = max(per_point, key=lambda item: item[1])

    result = {
        "image_path": image_path,
        "num_skeleton_points": len(skeleton_points),
        "num_valid_points": len(per_point),
        "W_G_pixels": W_G,
        "p_star": p_star,
        "per_point": per_point,
    }
    if pixel_to_mm is not None:
        result["W_G_mm"] = W_G * pixel_to_mm

    return result


def save_per_point_csv(result, out_csv):
    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y", "W_p_pixels"])
        for (x, y), w in result["per_point"]:
            writer.writerow([x, y, w])
    print(f"Đã lưu chi tiết W(p) theo từng điểm skeleton: {out_csv}")


def analyze_dataset_folder(folder, n_iter=8, skeleton_subsample=5,
                            pixel_to_mm=None, out_csv="results/width_summary.csv"):
    """
    Chạy analyze_single_image cho TẤT CẢ ảnh trong 1 thư mục (ví dụ tất cả
    mốc thời gian của 1 mẫu bê tông), lưu bảng tổng hợp W(S;G) theo tên file
    (giả định tên file mã hoá mốc thời gian, ví dụ 'specimenA_t0.png').
    """
    image_files = sorted(
        f for f in os.listdir(folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff"))
    )
    if not image_files:
        print(f"[!] Không tìm thấy ảnh nào trong: {folder}")
        return []

    rows = []
    for fname in image_files:
        path = os.path.join(folder, fname)
        try:
            result = analyze_single_image(
                path, n_iter=n_iter, skeleton_subsample=skeleton_subsample,
                pixel_to_mm=pixel_to_mm,
            )
            rows.append({
                "file": fname,
                "W_G_pixels": result["W_G_pixels"],
                "W_G_mm": result.get("W_G_mm", None),
                "num_valid_points": result["num_valid_points"],
            })
            print(f"[OK] {fname}: W(S;G) = {result['W_G_pixels']:.3f} px"
                  + (f" ({result.get('W_G_mm'):.4f} mm)" if pixel_to_mm else ""))
        except Exception as e:
            print(f"[LỖI] {fname}: {e}")

    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "W_G_pixels", "W_G_mm", "num_valid_points"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nĐã lưu bảng tổng hợp: {out_csv}")
    return rows


if __name__ == "__main__":
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")
    OUT_CSV = os.path.join(os.path.dirname(__file__), "results", "width_summary.csv")

    if not os.path.isdir(DATA_DIR) or not os.listdir(DATA_DIR):
        print(f"[!] Chưa có dữ liệu trong {DATA_DIR}.")
        print("    Xem task4_selfhealing_application/README.md để tải dataset")
        print("    Jakubowski & Tomczak (2025), hoặc chạy make_synthetic_sample.py")
        print("    để tạo ảnh mô phỏng chạy thử pipeline.")
    else:
        # pixel_to_mm cần lấy từ metadata scan thật của dataset (ví dụ DPI của scanner)
        analyze_dataset_folder(DATA_DIR, pixel_to_mm=None, out_csv=OUT_CSV)
