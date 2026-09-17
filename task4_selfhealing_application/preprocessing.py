"""
task4_selfhealing_application/preprocessing.py
------------------------------------------------
Tiền xử lý ảnh scan vết nứt (dataset Jakubowski & Tomczak, 2025):
  1. Đọc ảnh grayscale/RGB.
  2. Nhị phân hoá để tách vết nứt khỏi nền bê tông (threshold / adaptive).
  3. Trích biên ∂S của vùng vết nứt (contour) -> dùng cho width_at_point /
     Algorithm 1 (S xấp xỉ là đa giác từ contour).
  4. Skeletonization -> G, đường trung tâm vết nứt (giống Fig. 6, 8 trong
     bài báo, "colored in red").

Ghi chú: pipeline này mang tính THAM KHẢO/tổng quát; với dữ liệu thật của
Jakubowski & Tomczak, ảnh đã được xử lý sẵn theo grid-line, nên có thể cần
điều chỉnh threshold cho phù hợp với đặc điểm ảnh scan cụ thể (xem README.md
của task này).
"""

import numpy as np
import cv2
from skimage.morphology import skeletonize


def load_image(path, grayscale=True):
    flag = cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR
    img = cv2.imread(path, flag)
    if img is None:
        raise FileNotFoundError(f"Không đọc được ảnh: {path}")
    return img


def binarize_crack(gray_img, method="otsu", block_size=51, C=10):
    """
    Nhị phân hoá ảnh để tách vết nứt (vùng tối/khác biệt) khỏi nền bê tông.

    method="otsu": ngưỡng toàn cục Otsu — phù hợp ảnh sáng đều.
    method="adaptive": ngưỡng thích nghi cục bộ — phù hợp ảnh scan không đều sáng
                       (thường phù hợp hơn với ảnh bề mặt bê tông thực tế).
    """
    blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)

    if method == "otsu":
        _, binary = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )
    elif method == "adaptive":
        binary = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, block_size, C
        )
    else:
        raise ValueError(f"method không hỗ trợ: {method}")

    # loại nhiễu nhỏ
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    return binary


def extract_largest_crack_contour(binary_img, min_area=50):
    """
    Trích contour (biên ∂S) của vùng vết nứt LỚN NHẤT trong ảnh nhị phân.
    Trả về contour dưới dạng list điểm (x, y) — dùng làm 'vertices' của đa
    giác xấp xỉ S cho các hàm trong common/geometry_utils.py.
    """
    contours, _ = cv2.findContours(
        binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = [c for c in contours if cv2.contourArea(c) >= min_area]
    if not contours:
        raise ValueError("Không tìm được vùng vết nứt nào đủ lớn trong ảnh.")

    largest = max(contours, key=cv2.contourArea)
    # đơn giản hoá contour để giảm số đỉnh (Douglas-Peucker)
    epsilon = 0.5
    approx = cv2.approxPolyDP(largest, epsilon, closed=True)
    vertices = [tuple(pt[0]) for pt in approx]
    return vertices, largest


def extract_skeleton(binary_img):
    """
    Skeletonization vùng vết nứt -> đường trung tâm G (skeleton), trả về
    danh sách điểm (x, y) theo thứ tự pixel (chưa sắp xếp thành đường liên
    tục — dùng để lấy mẫu điểm cho Task 3, không cần thứ tự để tính max).
    """
    binary_bool = binary_img > 0
    skel = skeletonize(binary_bool)
    ys, xs = np.nonzero(skel)
    points = list(zip(xs.tolist(), ys.tolist()))
    return points, skel


def process_image(path, method="adaptive"):
    """Pipeline đầy đủ: ảnh -> (vertices ∂S, skeleton G)."""
    gray = load_image(path, grayscale=True)
    binary = binarize_crack(gray, method=method)
    vertices, contour = extract_largest_crack_contour(binary)
    skeleton_points, skel_mask = extract_skeleton(binary)
    return {
        "gray": gray,
        "binary": binary,
        "vertices": vertices,
        "skeleton_points": skeleton_points,
        "skel_mask": skel_mask,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Dùng: python preprocessing.py <đường_dẫn_ảnh>")
        sys.exit(1)

    result = process_image(sys.argv[1])
    print(f"Số đỉnh contour (~biên ∂S): {len(result['vertices'])}")
    print(f"Số điểm skeleton (G): {len(result['skeleton_points'])}")
