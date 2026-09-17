# Nhóm 2 — Width of Compact Sets & Ứng dụng đo độ rộng vết nứt

Repo triển khai lại các nội dung trong tài liệu:
**An, P.T. & Hai, N.N. (2026). "Widths of compact sets in normed spaces and an application in
measuring crack widths." J. Comput. Appl. Math. 485, 117498.**

## Cấu trúc repo

| Thư mục | Nội dung | Tương ứng câu hỏi |
|---|---|---|
| `task1_algorithm1/` | Triển khai lại Algorithm 1, phân tích tính hội tụ | (1) |
| `task2_convergence_conditions/` | Điều kiện đủ để Algorithm 1 hội tụ về nghiệm chính xác | (2) |
| `task3_width_of_subset/` | Thuật toán tính W(S;G) với G ⊂ S trong R² | (3) |
| `task4_selfhealing_application/` | Áp dụng đo độ rộng vết nứt tự phục hồi trên dataset Jakubowski & Tomczak (2025) | (4) |
| `common/` | Hàm hình học & W(p) dùng chung cho các task | — |
| `docs/` | Bài báo gốc, báo cáo cuối kỳ | — |

## Cài đặt

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Chạy nhanh

```bash
# (1) Demo Algorithm 1 và hội tụ
python task1_algorithm1/algorithm1.py

# (3) Demo tính W(S;G)
python task3_width_of_subset/set_width_algorithm.py

# (4) Áp dụng lên dữ liệu vết nứt tự phục hồi
python task4_selfhealing_application/run_algorithm1_on_cracks.py
```

## Dữ liệu tham khảo (Task 4)

Jakubowski, J. & Tomczak, K. (2025). *Dataset for developing deep learning models to assess
crack width and self-healing progress in concrete.* Scientific Data, 12, 165.
DOI: 10.1038/s41597-025-04485-z
https://www.researchgate.net/publication/388460885

> Đặt các file ảnh/brightness-profile đã tải từ dataset vào `task4_selfhealing_application/data/`
> trước khi chạy pipeline (xem `task4_selfhealing_application/README.md`).

## Tài liệu lý thuyết liên quan

- Definition 1, 2 — W(p), W(G)
- Proposition 1 — infimum trong Definition 1 là minimum (đạt được)
- Theorem 1 — tính lsc/usc của x ↦ W(x)
- Proposition 7 & Algorithm 1 — xấp xỉ W_S(p) bằng hữu hạn đoạn thẳng qua p
