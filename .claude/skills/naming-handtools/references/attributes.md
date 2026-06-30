# Thông số & quy ước đơn vị theo họ dụng cụ

Engine `normalize_units` ép các quy ước đơn vị này cho phần TÊN. Giá trị thông số CHÍNH THỨC (cột `TS_*`) **phải search mã hãng**, không lấy từ mô tả (xem `spec_schema.md`). Bảng dưới = quy ước đơn vị + thông số kì vọng theo họ.

## Quy ước đơn vị chuẩn (chuẩn hóa tự động)
| Dạng input | Chuẩn hóa |
|---|---|
| `8mm`, `8 mm` | `8 mm` |
| `7Inch`, `7In`, `7"` | `7 Inch` |
| `1/2"`, `1/2In`, `Dr.1/2` | `1/2 Inch` |
| `100Nm`, `60-340Nm` | `100 Nm`, `60-340 Nm` |
| `16oz`, `4lbs`, `680g` | `16 Oz`, `4 Lbs`, `680 G` |
| `7 Inch / 180 mm` | `7 Inch/180 mm` (giữ `/`, không cách) |

## Thông số chính theo họ
| Họ | Thông số đặc trưng | Ví dụ |
|---|---|---|
| **Đầu Tuýp** (lẻ) | cỡ mở `mm` + dẫn động `Inch` | `24 mm 1/2 Inch` |
| **Bộ Đầu Tuýp** | dẫn động + số chi tiết | `1/2 Inch 24 Cái` |
| **Cờ Lê** (đơn) | cỡ miệng `mm` | `46 mm` |
| **Cờ Lê 2 đầu** | cặp cỡ | `17 x 19 mm` |
| **Bộ Cờ Lê** | số chi tiết + dải | `14 Chi Tiết 8-32 mm` |
| **Kìm / Mỏ Lết / Cảo / Búa** | chiều dài `Inch` (đôi khi `Inch/mm`) | `8 Inch`, `10 Inch/254 mm` |
| **Búa** | thêm khối lượng | `16 Oz`, `4 Lbs`, `680 G` |
| **Cần Siết Lực / Cần Nổ** | dẫn động + dải lực | `1/2 Inch 40-200 Nm` (hoặc `ft-lb`) |
| **Lục Giác** | cỡ `mm` (hoặc `Inch`) + Bi/Đầu Bằng | `5 mm Đầu Bằng`, `3 mm Bi` |
| **Tua Vít** | đầu × dài | `PH2x100 mm`, `3x125 mm` |
| **Mũi Vít / bit** | cỡ + chiều dài | `2 mm 65 mm` |
| **Thước** | dải/độ phân giải/chiều dài | `8M`, `0-150 mm`, `0-300mm/0.02mm` |
| **Bộ (chung)** | số chi tiết | `9 Chi Tiết`, `66 Chi Tiết` |

## Hệ dẫn động (drive) — đầu tuýp / cần / tay vặn
`1/4 Inch` · `3/8 Inch` · `1/2 Inch` · `3/4 Inch` · `1 Inch`. Giữ phân số, có chữ "Inch". Gặp `F`/`M` (cái/đực) ở đầu chuyển đổi: `1/2 Inch F x 3/8 Inch M`.

## Lưu ý
- **Đầu Tuýp lẻ** có cả "cỡ mm" và "dẫn động Inch" → KHÔNG nhầm cỡ mm thành drive.
- **Số chi tiết** (`Cái`/`Chi Tiết`) chỉ có ở bộ → tín hiệu nhận diện "Bộ ...".
- Mô tả thiếu cỡ/lực/số chi tiết → đánh dấu cần search mã hãng, KHÔNG suy đoán.
