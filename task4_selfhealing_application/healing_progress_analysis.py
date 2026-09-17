"""
task4_selfhealing_application/healing_progress_analysis.py
-------------------------------------------------------------
Phân tích SỰ PHỤC HỒI (self-healing) của vết nứt dựa trên kết quả W(S;G)
tại nhiều mốc thời gian (đầu ra của run_algorithm1_on_cracks.py), so sánh
với reference_measurements.csv (đo tay, có sẵn trong dataset Jakubowski &
Tomczak) để đánh giá độ chính xác của Algorithm 1.

Yêu cầu file đầu vào:
  - results/width_summary.csv          (cột: file, W_G_pixels, W_G_mm, ...)
  - data/reference_measurements.csv    (cột: file, t (ngày quan sát),
                                         width_ref_mm, ... — tuỳ cấu trúc
                                         thật của dataset, cần map lại tên
                                         cột nếu khác)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_results(summary_csv, reference_csv=None):
    df = pd.read_csv(summary_csv)
    if reference_csv and os.path.exists(reference_csv):
        ref = pd.read_csv(reference_csv)
        df = df.merge(ref, on="file", how="left")
    return df


def parse_time_from_filename(fname, pattern_hint="t"):
    """
    Cố gắng trích mốc thời gian t từ tên file, ví dụ 'specimenA_t0.png' -> 0,
    'specimenA_day14.png' -> 14. Điều chỉnh regex cho khớp quy ước đặt tên
    thật của dataset sau khi tải về.
    """
    import re
    m = re.search(r"(?:t|day)(\d+)", fname, flags=re.IGNORECASE)
    return int(m.group(1)) if m else None


def plot_healing_curve(df, width_col="W_G_mm", time_col="t",
                        ref_col=None, specimen_col=None, out_path=None):
    """
    Vẽ đường cong W(S;G) theo thời gian (đường cong phục hồi), tuỳ chọn overlay
    với reference measurement để so sánh.
    """
    if time_col not in df.columns:
        df[time_col] = df["file"].apply(parse_time_from_filename)

    df = df.sort_values(time_col)

    plt.figure(figsize=(7, 4.5))
    if specimen_col and specimen_col in df.columns:
        for specimen, group in df.groupby(specimen_col):
            plt.plot(group[time_col], group[width_col], "o-", label=f"{specimen} (Algorithm 1)")
    else:
        plt.plot(df[time_col], df[width_col], "o-", label="W(S;G) — Algorithm 1")

    if ref_col and ref_col in df.columns:
        plt.plot(df[time_col], df[ref_col], "x--", color="red", label="Reference (đo tay)")

    plt.xlabel("Thời gian quan sát (ngày)")
    plt.ylabel("Độ rộng vết nứt (mm)")
    plt.title("Diễn biến độ rộng vết nứt theo thời gian (self-healing)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if out_path:
        plt.savefig(out_path, dpi=150)
        print(f"Đã lưu biểu đồ: {out_path}")
    return plt.gcf()


def compute_accuracy_metrics(df, pred_col="W_G_mm", ref_col="width_ref_mm"):
    """So sánh Algorithm 1 với đo tay: MAE, RMSE, R^2 — giống cách bài báo
    gốc của dataset đánh giá mô hình CNN/analytic của họ."""
    valid = df.dropna(subset=[pred_col, ref_col])
    if valid.empty:
        print("[!] Không có dữ liệu tham chiếu để so sánh.")
        return None

    err = valid[pred_col] - valid[ref_col]
    mae = err.abs().mean()
    rmse = np.sqrt((err ** 2).mean())
    ss_res = (err ** 2).sum()
    ss_tot = ((valid[ref_col] - valid[ref_col].mean()) ** 2).sum()
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    metrics = {"MAE_mm": mae, "RMSE_mm": rmse, "R2": r2, "n": len(valid)}
    print("=== Độ chính xác Algorithm 1 so với đo tay (reference) ===")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
    return metrics


def compute_healing_rate(df, width_col="W_G_mm", time_col="t"):
    """
    Ước lượng tốc độ phục hồi (healing rate) bằng độ dốc tuyến tính (mm/ngày)
    của W(S;G) theo thời gian — chỉ mang tính minh hoạ đơn giản, có thể thay
    bằng mô hình mũ suy giảm nếu dữ liệu phù hợp hơn.
    """
    if time_col not in df.columns:
        df[time_col] = df["file"].apply(parse_time_from_filename)
    valid = df.dropna(subset=[width_col, time_col])
    if len(valid) < 2:
        print("[!] Không đủ dữ liệu để ước lượng tốc độ phục hồi.")
        return None

    slope, intercept = np.polyfit(valid[time_col], valid[width_col], 1)
    print(f"Tốc độ thay đổi độ rộng ước lượng: {slope:.5f} mm/ngày "
          f"({'giảm -> đang tự phục hồi' if slope < 0 else 'tăng -> vết nứt lan rộng'})")
    return slope


if __name__ == "__main__":
    base = os.path.dirname(__file__)
    summary_csv = os.path.join(base, "results", "width_summary.csv")
    reference_csv = os.path.join(base, "data", "reference_measurements.csv")

    if not os.path.exists(summary_csv):
        print(f"[!] Chưa có {summary_csv}. Hãy chạy run_algorithm1_on_cracks.py trước.")
    else:
        df = load_results(summary_csv, reference_csv if os.path.exists(reference_csv) else None)

        # Nếu chưa có hệ số pixel->mm (W_G_mm toàn NaN), tạm dùng W_G_pixels
        # để vẫn xem được xu hướng (đơn vị pixel) — thay bằng W_G_mm khi có
        # thông tin thang đo thật của ảnh scan.
        width_col = "W_G_mm" if df["W_G_mm"].notna().any() else "W_G_pixels"
        print(f"[i] Dùng cột '{width_col}' để vẽ/ước lượng (chưa có hệ số pixel->mm).")

        fig = plot_healing_curve(
            df, width_col=width_col,
            out_path=os.path.join(base, "results", "figures", "healing_curve.png")
        )
        if "width_ref_mm" in df.columns:
            compute_accuracy_metrics(df, pred_col=width_col)
        compute_healing_rate(df, width_col=width_col)
