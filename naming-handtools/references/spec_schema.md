# Sheet chuẩn & schema thông số kĩ thuật

> ⚠️ **NGUYÊN TẮC CỨNG:** Thông số kĩ thuật của mỗi mã **PHẢI lấy bằng SEARCH MÃ HÃNG** trên catalog hãng (có nguồn URL). **KHÔNG** suy từ mã/part# cũ, **KHÔNG** bịa, **KHÔNG** coi số trong mô tả là chân lý (mô tả có thể sai/thiếu). Engine chỉ cho LOẠI/CATEGORY/FORM + thông số **DRAFT để đối chiếu** — draft ≠ giá trị cuối.

## Cấu trúc sheet chuẩn (output)
| Nhóm cột | Cột | Nguồn |
|---|---|---|
| **Gốc (giữ nguyên)** | Part ID · Part # · Description · Mã hãng | input |
| **Chuẩn hóa (engine)** | Tên chuẩn · category_id · Loại · status | engine deterministic |
| **Thông số kĩ thuật (TS_*)** | xem bảng dưới — **TRỐNG, điền bằng search mã hãng** | catalog hãng |
| **Nguồn** | Nguồn (URL catalog hãng) | bắt buộc khi điền TS_ |
| **Draft (đối chiếu)** | draft_* (gợi ý từ mô tả) | engine — KHÔNG phải giá trị cuối |

## Cột thông số kĩ thuật chính thức (TS_)
| Cột | Ý nghĩa | Áp dụng cho họ |
|---|---|---|
| TS_Hệ Dẫn Động | 1/4 · 3/8 · 1/2 · 3/4 · 1 Inch | đầu tuýp, cần, tay vặn, cần siết lực |
| TS_Cỡ/Khẩu (mm) | cỡ mở/khẩu, hoặc cỡ lục giác | đầu tuýp, cờ lê, lục giác |
| TS_Số Cạnh | 6 cạnh / 12 cạnh (hex/bi-hex) | đầu tuýp, cờ lê |
| TS_Chiều Dài | mm hoặc Inch | kìm, mỏ lết, cảo, búa, tua vít, thước |
| TS_Lực Min / TS_Lực Max / TS_Đơn Vị Lực | dải lực + Nm/ft-lb | cần siết lực, cần nổ |
| TS_Số Chi Tiết | số món trong bộ | mọi loại "Bộ ..." |
| TS_Vật Liệu/Phủ | CrV / CrMo / thép / mạ crôm / cách điện 1000V | tất cả |
| TS_Tiêu Chuẩn | DIN/ISO/ANSI nếu có | tất cả |
| TS_Đặc Điểm Khác | bi/đầu bằng/cán bọc/từ tính/... | tất cả |

> Không cần điền cột không áp dụng (vd búa không có hệ dẫn động). Cột không áp dụng → để trống, KHÔNG bịa.

## Thông số tối thiểu BẮT BUỘC theo họ (search phải lấy đủ)
- **Đầu tuýp lẻ**: Hệ dẫn động · Cỡ khẩu (mm) · Số cạnh.
- **Cờ lê**: Cỡ miệng (mm) (cặp cỡ nếu 2 đầu) · loại đầu.
- **Cần siết lực / cần nổ**: Hệ dẫn động · Dải lực + đơn vị.
- **Kìm / mỏ lết / cảo / búa**: Chiều dài (· khối lượng với búa).
- **Tua vít**: Loại đầu (PH/SL/TX) · cỡ × chiều dài.
- **Bộ ...**: Số chi tiết · phạm vi cỡ.

## status
- **NEEDS_WEB** — engine đã ra loại + tên + category; **chờ search mã hãng điền TS_ + Nguồn**. (mặc định mọi dòng có loại)
- **REVIEW_TYPE+NEEDS_WEB** — loại đoán mơ hồ (Kìm/Búa/Cảo trống đặc trưng): xác nhận loại RỒI search.
- **UNKNOWN_TYPE** — chưa ra loại: search mã hãng để biết loại + category + TS.
- **OK** — CHỈ set khi TS_ bắt buộc đã điền + có Nguồn. Engine KHÔNG tự set OK.
