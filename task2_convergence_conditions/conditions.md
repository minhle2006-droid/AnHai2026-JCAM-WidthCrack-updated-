# Task 2 — Điều kiện đủ để Algorithm 1 hội tụ về nghiệm chính xác

Ta xây dựng các điều kiện (giả thiết) trên `S` và `p` để đảm bảo:

```
lim_{n→∞} W_S^(n)(p) = W_S(p)
```

## Ký hiệu

- `θ₀`: hướng của đoạn ban đầu (i=1) trong Algorithm 1.
- `D_n := { θ₀ + k·π/2^(n-1) mod π : k = 0,...,2^(n-1)-1 }` — lưới hướng sau `n` vòng.
- Theo Proposition 1, tồn tại `u*, v* ∈ ∂S` với `p ∈ ]u*,v*[ ⊂ int(S)`,
  `||u*-v*|| = W(p)`. Gọi `d* := hướng của (u*-v*)` (một hướng đạt inf; có thể
  không duy nhất — gọi `D* ⊂ [0,π)` là **tập tất cả** các hướng đạt `W(p)`).

## Điều kiện đủ (giả thiết) — 3 nhóm

### (C1) Điều kiện về "tính trù mật" của lưới hướng
```
liminf_{n→∞} dist(D_n, D*) = 0
```
nghĩa là: có một dãy con các hướng trong `D_n` tiến tới một hướng thuộc `D*`.

- **Trường hợp riêng đủ dùng trong thực hành:** nếu ta chọn `θ₀` sao cho `D*`
  chứa **ít nhất một hướng dạng** `θ₀ + q·π` với `q ∈ ℚ` có dạng nhị phân
  hữu hạn (`q = k/2^m`), thì với `n ≥ m+1`, hướng đó **xuất hiện chính xác**
  trong `D_n` → hội tụ **hữu hạn bước** (không chỉ tiệm cận).
- Vì lưới `D_n` là lưới nhị phân đều đặn, một cách đơn giản và **kiểm chứng được
  bằng máy** để đảm bảo (C1): quét nhiều giá trị `θ₀` khác nhau (ví dụ
  `θ₀ = j·π/N₀`) và chạy Algorithm 1 cho từng `θ₀`, lấy `min` trên tất cả — điều
  này tương đương mở rộng lưới hướng ra dày hơn (xem `convergence_conditions_note`
  trong `verify_conditions.py`).

### (C2) Điều kiện hình học trên `S` (đủ để `D*` không "cô lập")
Nếu `S` thoả:
> **(C2a)** `S` là **đa giác lồi** với `p ∈ int(S)`, **và**
> **(C2b)** hàm `x ↦ W(x)` liên tục tại `p` (theo Theorem 1 / Corollary 2, luôn
> đúng nếu `p` là điểm trong của tập lồi `S`),

thì tập `D*` các hướng đạt `W(p)` là **đóng** trong `[0,π)` (do compact + liên tục
theo Weierstrass), và với mọi `θ₀`, `liminf dist(D_n, D*) = 0` **tự động đúng**
vì lưới nhị phân `⋃_n D_n` là **trù mật** trong `[0,π)` — đây là điều kiện đủ
**không cần chọn `θ₀` đặc biệt**.

> **Chứng minh trù mật:** `⋃_{n≥1} D_n` với `D_n = {θ₀+kπ/2^{n-1}}` chính là tập
> các số hạng `θ₀ + k·π/2^m, m∈ℕ, k∈ℤ` — đây là tập các "số nhị phân hữu tỉ" nhân
> `π`, trù mật trong `ℝ` (do đó trù mật trong `[0,π)` khi rút modulo). ∎

**⇒ Kết luận (C2):** Nếu `S` lồi và `p ∈ int(S)`, Algorithm 1 hội tụ về `W_S(p)`
**chính xác** với `θ₀` bất kỳ:
```
S lồi, p ∈ int(S)   ⟹   lim_{n→∞} W_S^(n)(p) = W_S(p)
```

### (C3) Điều kiện khi `S` KHÔNG lồi
Nếu `S` không lồi (như *Example 3*), `D*` có thể chỉ gồm **một hướng duy nhất
cô lập** (không phải điểm giới hạn của các hướng lân cận có giá trị nhỏ hơn), và
hội tụ về giá trị đúng **không còn tự động** — cần thêm giả thiết:

> **(C3)** Hướng `d* ∈ D*` là **giới hạn của một dãy hướng nhị phân** dạng
> `θ₀ + k_m π / 2^m` (`m → ∞`) — tương đương yêu cầu `θ₀` được chọn (hoặc suy ra)
> từ chính hướng `d*`, ví dụ đặt `θ₀ := d* mod π` (nếu biết trước hướng tối ưu,
> điều này tầm thường); **hoặc**
> **(C3')** dùng **nhiều `θ₀` khác nhau** đồng thời (multi-start), tăng dần độ phủ
> của lưới hướng tổng hợp — khi đó theo Baire/trù mật, xác suất "trúng" lân cận
> `d*` tiến tới 1 khi số lượng `θ₀` tăng, nhưng **không đảm bảo tuyệt đối** với
> `S` không lồi tổng quát (có thể xây `S` sao cho `D*` là một điểm hữu hạn duy
> nhất với hướng vô tỉ · `π`, khi đó không `θ₀` hữu tỉ nào cho hội tụ hữu hạn
> bước, chỉ có xấp xỉ dần theo `n → ∞` nếu `θ₀` được chọn tại chính hướng đó).

## Bảng tổng hợp điều kiện

| Giả thiết trên `S`, `p` | Kết luận về hội tụ |
|---|---|
| `S` lồi, `p ∈ int(S)` | Hội tụ đúng `W_S(p)` với **mọi** `θ₀` (do Corollary 2: `W` liên tục trên `int S`) |
| `S` không lồi, nhưng `d* mod π` là số **nhị phân hữu hạn** và ta biết trước để chọn `θ₀` phù hợp | Hội tụ đúng, **hữu hạn bước** |
| `S` không lồi, `d*` bất kỳ, `θ₀` cố định tuỳ ý | **Không đảm bảo** — chỉ có `lim ≥ W_S(p)` (Proposition 7) |
| `S` không lồi, nhưng dùng `θ₀ → d*` (biết hướng tối ưu qua tiền xử lý, ví dụ PCA trên biên cục bộ) | Hội tụ đúng |

## Liên hệ với Proposition 6 (chặn trên bằng minimal width)

Nếu chọn đoạn đầu `i=1` **cùng hướng với trục `α`** (vuông góc 2 siêu phẳng tựa
song song xác định minimal width `l` của `conv(S)`), Proposition 7 cho thêm:
```
W_S(p) ≤ lim_n W_S^(n)(p) ≤ l
```
Đây là cách chọn `θ₀` "an toàn" trong thực hành: **luôn cho sai số bị chặn bởi
`l - W_S(p)`**, dù không đảm bảo bằng 0 khi `S` không lồi.
