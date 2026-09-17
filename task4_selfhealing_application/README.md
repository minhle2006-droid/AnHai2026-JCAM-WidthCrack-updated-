# Task 4 — Áp dụng Algorithm 1 phân tích sự phục hồi (self-healing) của vết nứt

## Nguồn dữ liệu

Jakubowski, J. & Tomczak, K. (2025). *Dataset for developing deep learning
models to assess crack width and self-healing progress in concrete.*
Scientific Data, 12, 165. DOI: 10.1038/s41597-025-04485-z

- ResearchGate: https://www.researchgate.net/publication/388460885
- Bài báo gốc (open access): https://www.nature.com/articles/s41597-025-04485-z

### Mô tả dữ liệu (tóm tắt)
- Ảnh scan độ phân giải cao bề mặt mẫu bê tông cường độ cao, tại **nhiều mốc
  thời gian** (trước và sau nứt, và các mốc theo dõi tự phục hồi — autogenous
  self-healing).
- Tại mỗi mốc thời gian, nhiều **grid line** (đường lưới) cắt qua vết nứt được
  đánh dấu cố định trên mẫu, giúp so sánh đúng vị trí giữa các mốc quan sát.
- Mỗi giao điểm grid-line × crack có: **brightness profile** (biểu đồ độ sáng
  dọc theo grid line), **reference measurement** (đo tay bằng operator), và
  **benchmark measurement** (đo bằng CNN/mô hình analytic của tác giả).
- Tổng cộng 19,098 bản ghi.

### Cách lấy dữ liệu
1. Tải dataset từ liên kết DOI trên (Figshare/Nature Scientific Data — dataset
   công khai, có thể cần đăng ký tài khoản miễn phí).
2. Giải nén, đặt các ảnh scan (`*.tif`/`*.png`) đã stack + grid-line vào:
   ```
   task4_selfhealing_application/data/raw/
   ```
3. Đặt file mô tả grid-line / đo tham chiếu (CSV) vào:
   ```
   task4_selfhealing_application/data/reference_measurements.csv
   ```

> **Lưu ý:** repo này KHÔNG đóng gói sẵn dữ liệu gốc (dung lượng lớn, cần tuân
> thủ điều khoản chia sẻ dữ liệu của tác giả) — chỉ cung cấp pipeline xử lý.
> Có thể chạy thử pipeline trên `data/sample_synthetic/` (ảnh vết nứt mô phỏng,
> tự tạo bằng `make_synthetic_sample.py`) trước khi có dữ liệu thật.

## Quy trình (pipeline)

```
Ảnh scan tại mốc t_k
        │
        ▼
preprocessing.py          # nhị phân hoá, trích biên ∂S của vết nứt,
                           # skeletonization -> G (đường skeleton)
        │
        ▼
run_algorithm1_on_cracks.py
        # Với mỗi điểm p trên skeleton G:
        #   W(p) <- Algorithm 1 (task1_algorithm1)
        # W(S;G) <- max_p W(p)   (task3_width_of_subset)
        │
        ▼
healing_progress_analysis.py
        # So sánh W(S;G) tại các mốc t0 < t1 < t2 < ...
        # -> đường cong phục hồi (healing curve)
        # -> so sánh với reference_measurements.csv (đánh giá độ chính xác)
```

## Kết quả kỳ vọng

- `results/figures/width_over_time_<specimen_id>.png`: biểu đồ `W(S;G)` (và/hoặc
  `W(p)` tại từng điểm dọc skeleton) theo thời gian quan sát — thể hiện xu hướng
  **giảm dần** nếu vết nứt đang tự phục hồi.
- `results/report.md`: nhận xét định lượng — tốc độ giảm độ rộng, so sánh với
  reference measurement (sai số RMSE/MAE), và so sánh với benchmark CNN có sẵn
  trong dataset (nếu dùng).
