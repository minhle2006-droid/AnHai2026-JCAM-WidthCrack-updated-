# Task 1 — Algorithm 1: triển khai & phân tích tính hội tụ

## 1. Tóm tắt thuật toán (đúng theo tài liệu)

**Input:** `n > 1`, tập compact `S`, điểm `p ∈ int(S)`.
**Output:** `F(n) = { ||u_i - v_i|| : u_i, v_i ∈ ∂S, p ∈ [u_i, v_i], i = 1,...,2^(n-1) }`

1. Vẽ 1 đường thẳng bất kỳ qua `p` → tạo 2 góc `π` (i = 1).
2. Với mỗi vòng `i = 2,...,n`: với **mọi** góc hiện có, vẽ đường phân giác của góc đó
   và kéo dài thành đoạn qua `p`. Sau vòng `i`, số góc là `2^i`.
3. Sau `n` vòng, có `num_segments = 2^(n-1)` đoạn thẳng qua `p`, mỗi đoạn cắt `∂S`
   tại 2 điểm `u_i, v_i`.
4. Đặt `W_S^(n)(p) := min F(n)`.

**Quan sát hình học quan trọng:** vì mỗi bước bisect **tất cả** góc đồng thời,
tập hướng sinh ra sau `n` vòng luôn là lưới hướng **cách đều nhau góc `π / 2^(n-1)`**
bắt đầu từ hướng ban đầu `θ₀` (được chọn tuỳ ý ở bước i=1). Đây là điểm mấu chốt
dùng để cài đặt lại thuật toán một cách tường minh (`generate_directions()` trong
`algorithm1.py`) thay vì phải mô phỏng đệ quy việc "chia đôi góc".

## 2. Thuật toán này có hội tụ về nghiệm chính xác không?

**Trả lời: KHÔNG đảm bảo hội tụ về `W_S(p)` chính xác trong trường hợp tổng quát.**

### Điều bài báo đã chứng minh (Proposition 7)

```
lim_{n→∞} W_S^(n)(p)  ≥  W_S(p)                                (*)
```

và nếu đoạn đầu tiên (i=1) được chọn **cùng hướng với trục `α`** (đường vuông góc
với 2 siêu phẳng tựa song song `H₁, H₂` xác định minimal width `l` của `conv(S)`) thì:

```
l  ≥  lim_{n→∞} W_S^(n)(p)
```

Nghĩa là dãy `{W_S^(n)(p)}` **đơn điệu giảm** (khi `n` tăng, số hướng xét tăng gấp đôi,
nên `min` không thể tăng) và **hội tụ**, bị chặn giữa `W_S(p)` và `l`:

```
W_S(p)  ≤  lim_{n→∞} W_S^(n)(p)  ≤  l
```

Nhưng **không có** khẳng định `lim = W_S(p)`. Đẳng thức chỉ được đảm bảo trong
trường hợp đặc biệt (xem Task 2).

### Vì sao có thể KHÔNG hội tụ về giá trị đúng — giải thích trực quan

Theo **Proposition 1**, `W(p)` được đạt (là minimum, không chỉ infimum) tại
**một hướng cụ thể** `d* = (u*-p)` sao cho `[u*,v*]` là đoạn ngắn nhất qua `p`.
Algorithm 1 chỉ kiểm tra một **lưới hữu hạn, cách đều, được xác định trước** các
hướng `θ₀ + kπ/2^(n-1)`. Có 2 trường hợp:

- **Nếu `d*` "may mắn" rơi đúng vào lưới hướng này với `n` đủ lớn** (ví dụ: `S` có
  đối xứng khiến hướng tối ưu là hướng chia đôi tự nhiên của `θ₀`) → thuật toán hội
  tụ **đúng** về `W_S(p)`. Đây là trường hợp minh hoạ trong `algorithm1.py` (hình
  chữ nhật, `p` là tâm, hướng tối ưu trùng trục đối xứng).

- **Nếu `d*` không nằm trên bất kỳ hướng nào của lưới với mọi `n`** (ví dụ hướng tối
  ưu là một góc vô tỉ so với `θ₀`, hoặc `∂S` có một "khe hẹp" theo hướng lệch khỏi
  lưới) → với mọi `n`, `W_S^(n)(p) > W_S(p)` **thực sự** (bất đẳng thức chặt), và
  dãy chỉ hội tụ về infimum của các giá trị tương ứng lưới hướng — có thể **lớn hơn**
  `W_S(p)` một khoảng cố định, KHÔNG tiến về 0.

**Ví dụ cụ thể (xem `../task2_convergence_conditions/counterexample.ipynb`):**
Với đa giác không lồi như *Example 3* trong bài báo (điểm `p_0` mà `x ↦ W(x)`
không liên tục), hướng đạt `W(p_0)` là hướng cố định `(0,3)-(0,-1)` (trục Oy). Nếu
ta chọn `θ₀` sao cho trục Oy **không bao giờ** nằm trong lưới `{θ₀ + kπ/2^(n-1)}`
(ví dụ chọn `θ₀` là số vô tỉ · `π`), thì thuật toán không bao giờ đạt đúng giá trị,
dù `n → ∞`.

## 3. Kết luận

- Algorithm 1 là một **phương pháp xấp xỉ từ trên (upper bound)**: luôn cho
  `W_S^(n)(p) ≥ W_S(p)`.
- Tính đơn điệu giảm + bị chặn dưới ⇒ dãy luôn **hội tụ** (theo nghĩa giải tích),
  nhưng **giới hạn không nhất thiết là `W_S(p)`**.
- Độ chính xác phụ thuộc vào việc lưới hướng `{θ₀ + kπ/2^(n-1)}_n` có "trù mật"
  quanh hướng tối ưu `d*` hay không — xem điều kiện đủ ở Task 2.
