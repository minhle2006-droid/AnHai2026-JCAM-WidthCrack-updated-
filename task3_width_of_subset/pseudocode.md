# Task 3 — Pseudocode: tính W(S;G) trong R²

```
Input:  S (biên ∂S cho bởi đa giác hoặc ảnh nhị phân),
        G ⊂ S (đoạn thẳng / polyline / skeleton / tập điểm),
        num_points m, số vòng lặp n (cho Algorithm 1)
Output: W_hat ~ W(S;G)

1.  Points <- RỜI_RẠC_HOÁ(G, m)      # lấy m điểm đại diện, càng dày G
                                       # (theo Hausdorff) thì xấp xỉ càng tốt
2.  best <- 0 ; p_star <- None
3.  for each p in Points:
4.      if p ∈ ∂S:                    # Definition 1: W(p)=0 nếu p biên
5.          w <- 0
6.      else:                          # p ∈ int(S)
7.          w <- ALGORITHM_1(S, p, n)  # hoặc công thức chính xác nếu S đa giác
8.      if w > best:
9.          best <- w ; p_star <- p
10. W_hat <- best
11. return W_hat, p_star
```

## Giải thích cơ sở lý thuyết

- **Bước 1 (rời rạc hoá):** dựa trên Theorem 2(a) — hàm `G ↦ W(G)` là *lsc*
  trên không gian `(F, d_H)`. Khi lưới điểm `{p_k}` xấp xỉ `G` theo khoảng
  cách Hausdorff `d_H({p_k}, G) → 0`, ta có `W({p_k}) ≤ W(G)` luôn đúng
  (vì `{p_k} ⊂ G`).

- **Bước 3–9 (lấy max):** đây chính là công thức `W(G) = sup_{p∈G} W(p)`
  (Definition 2) áp dụng trên tập rời rạc — tương tự **Proposition 4**
  (`W(G) = max W(G_i)` khi `G` là hợp hữu hạn tập con) với mỗi điểm `p_k`
  đóng vai trò một "G_i" suy biến (tập 1 điểm).

- **Độ chính xác của kết quả trả về** phụ thuộc `m` (mật độ lưới) và `n`
  (độ chính xác Algorithm 1 tại từng điểm — xem Task 1, Task 2). Sai số tổng
  gồm 2 phần:
  ```
  |W_hat - W(S;G)| ≤ (sai số rời rạc hoá G, giảm khi m tăng)
                    + (sai số Algorithm 1 tại từng điểm, giảm khi n tăng
                       NẾU điều kiện Task 2 được thoả)
  ```

## Trường hợp đặc biệt: G là skeleton của vết nứt (ứng dụng Task 4)

Khi `G` là đường skeleton trích từ ảnh nhị phân của vết nứt (`red curve` trong
Fig. 6, 8 của bài báo), `Points` ở bước 1 chính là **các pixel trên skeleton**
(không cần rời rạc hoá thêm — đã hữu hạn và đủ dày theo độ phân giải ảnh).
`ALGORITHM_1` tại mỗi điểm cho ta W(p) theo pixel, và `W(S;G)` xấp xỉ **độ
rộng lớn nhất của vết nứt dọc theo toàn bộ đường đi của nó** — đây là đại
lượng thực tế cần báo cáo khi đánh giá mức độ nghiêm trọng / theo dõi phục
hồi của vết nứt (xem Task 4).
