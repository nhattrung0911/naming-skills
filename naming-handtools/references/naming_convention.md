# Văn phong đặt tên dụng cụ cầm tay

Học từ a sample sheet ( Kingtony) + corpus (Sata/Stanley/Bosch...).

## Cấu trúc chuẩn
```
{Tên loại} [{Đặc trưng}] {Thông số} {Hãng} {Mã hãng} [({Số lượng})]
```
- **Tên loại** đứng đầu, Title Case, theo tên chuẩn trong `category_map.md`.
- **Đặc trưng** = biến thể/kiểu, đi liền sau tên (Vòng Miệng, Tự Động, Mở Phe, - Sao, Đầu Bi, 3 Chấu, Điện Tử, Cách Điện, Bộ...).
- **Thông số** ở giữa, đơn vị chuẩn (chi tiết `attributes.md`).
- **Hãng** rồi **Mã hãng** ở cuối. Mã giữ nguyên hậu tố/dấu (`423024M`, `34467-1AG-1`, `68HS-05`).

## Ví dụ thật (Sheet3 + corpus)
- `Đầu Tuýp 24 mm 1/2 Inch Kingtony 423024M`
- `Cờ Lê Vòng Miệng 46 mm Kingtony 1071-46`
- `Kìm Mở Phe 10 Inch Kingtony 68SS-10`
- `Cần Nổ Điện Tử 1/2 Inch 40-200 Nm Kingtony 34467-1AG-1`
- `Bộ Đầu Tuýp 1/2 Inch 24 Cái Kingtony 4526MR03`
- `Đầu Tuýp - Sao 18 mm 1/2 Inch Kingtony 437518M`
- `Cảo 3 Chấu 8 Inch Kingtony 7963-08`
- (corpus) `Cờ Lê Vòng Miệng Basic 18 mm Stanley STMT80231-8B` · `Tua Vít Dẹp 3x125mm Stanley 60-819` · `Búa Nhổ Đinh Cán Gỗ 16oz Stanley STHT51339-8`

## Từ vựng ĐẶC TRƯNG (head-noun → biến thể hay gặp)
| Họ (Tên) | Đặc trưng |
|---|---|
| Cờ Lê | Vòng Miệng · 2 Đầu Vòng · 2 Đầu Miệng · Tự Động/Bánh Cóc · Móc · Đóng · Cách Điện · Lực |
| Mỏ Lết | (thường) · Răng |
| Kìm | Cắt · Mỏ Nhọn · Mở Phe · Điện/Đầu Bằng · Bấm Chết · Bấm Cos · Tuốt Dây · Mỏ Quạ |
| Tua Vít | Dẹp · Bake (PH) · Hoa Thị/Sao · 2 Đầu · Đầu Lục Giác · Đóng · Cách Điện |
| Đầu Tuýp | (lẻ) · - Sao/Gắn Mũi · Chuyển Đổi/Đầu Nối · Lắc Léo · Lục Giác |
| Lục Giác | Đầu Bằng · Đầu Bi/Bi · Chữ L · Chữ T |
| Cảo | 2 Chấu · 3 Chấu · Chữ C · Chữ F · Vô Bạc · Lọc Dầu |
| Cần | Tự Động · Chữ L · Chữ T · Trượt · Siết Lực/Nổ · Lắc Léo |
| Búa | Nhựa · Cao Su · Tạ · Đầu Bi · Nhổ Đinh · Gò · Đồng |

## Mã
- Bỏ tiền tố nội bộ đại lý (`KTN-`, `DL-`...). Dùng **cột Mã hãng** làm mã cuối.
- Giữ nguyên dấu/hậu tố của mã hãng: `-`, `/`, chữ cuối (`6011-07R`, `P404526MR01-VN`).
- Mã của mỗi hãng có format riêng: Sata = 5 số · Stanley = `NN-NNN` hoặc `STMT…` · Anex = `No.…` · Bosch = 10 số · Kingtony = số+chữ.

## Số lượng (bộ)
Cụm `(10 Cái/Bộ)`, `(20 Cái/Bộ)` để trong ngoặc ở **cuối cùng** (sau mã). Bộ nhiều món thì số chi tiết là thông số (`24 Cái`, `11 Chi Tiết`) đặt trong phần thông số.
