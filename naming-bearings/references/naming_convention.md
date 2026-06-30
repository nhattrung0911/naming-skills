# Văn phong đặt tên vòng bi (form tối ưu — internal catalog export, )

## Cấu trúc chuẩn
```
{Loại} {d}x{D}x{B} mm [{Nắp chắn}] {Hãng} {Mã}
```
- **Loại** đứng đầu (Title Case), tên chuẩn theo `category_map.md`.
- **Kích thước**: `{d}x{D}x{B} mm` — đầy đủ, có chữ "mm", KHÔNG ngoặc. Hệ inch → phân số + "inch". Khi chỉ biết bore → `d{bore} mm`.
- **Nắp chắn** (nếu có) đứng **sau đơn vị mm, trước hãng**.
- **Hãng** rồi **Mã** ở cuối. Mã **giữ nguyên hậu tố/dấu** như input (6204-2RS, NU-324, 63/22-2RS).

Ví dụ thật (file tối ưu):
- `Vòng Bi Cầu Rãnh Sâu Một Dãy 25x52x15 mm 2 Nắp Chắn Cao Su C&U 6205-2RS`
- `Vòng Bi Đũa Trụ 1 Dãy 25x62x17 mm NTN NF305`
- `Vòng Bi Cầu Tự Lựa 80x170x58 mm NTN 2316`
- `Vòng Bi Đũa Côn 1 Dãy 100x180x37 mm C&U 30220`
- `Gối Đỡ Vòng Bi Mặt Bích Vuông 80x190x52 mm Asahi UKF318`

## Từ vựng NẮP CHẮN (suy từ hậu tố mã)
| Hậu tố | Cụm | Ý nghĩa |
|---|---|---|
| `ZZ`, `2Z`, `DD` | **2 Nắp Chắn Thép** | 2 nắp kim loại |
| `2RS`, `DDU`, `LLU` | **2 Nắp Chắn Cao Su** | 2 phớt cao su |
| `Z` (1) | **1 Nắp Chắn Thép** | |
| `RS`, `DU`, `LU` (1) | **1 Nắp Chắn Cao Su** | |
| (không có) | (bỏ trống) | vòng bi hở |

> Lưu ý: form mới dùng "**2 Nắp Chắn**" (không phải "Hai Nắp"). Một số dòng cũ vẫn còn "Hai Nắp Chắn Thép" đặt ở cuối — khi chuẩn hóa nên đưa về "2 Nắp Chắn ..." sau loại.

## Vật liệu / mô tả thêm
`Thép` (mặc định) · `Inox`/`Thép Không Gỉ`/`440C` (mã S/SS/SB) · `Nhựa`/`POM` · `Vòng Cách Nhựa` (mã ECP/TVH).
Inox → thêm "Inox" vào loại + dùng category Inox.

## Mã
- Bỏ tiền tố hãng (NTN, SKF, C&U, CUB, DYZV, Asahi, PBC…), GIỮ phần còn lại nguyên: dấu `/`, `-`, hậu tố ZZ/2RS/ECP/JR/K/C3.
- Hệ inch Timken: `387/382`, `LM12649/10` — giữ nguyên dấu `/` + tiền tố LM/HM.

## HỆ INCH — KHÔNG ghi kích thước trong tên
Vòng bi côn hệ inch (Timken cone/cup, mã có `/` hoặc R-series): tên chỉ `{Loại} {Hãng} {Mã}`, **KHÔNG ghi dxDxB** (vì ra phân số inch xấu). Số mm vẫn để ở cột d/D/B cho vlookup.
- Đúng: `Vòng Bi Đũa Côn 1 Dãy PBC 603049/11`
- Sai: ~~`...1-25/32x3-1/16x25/32 inch...`~~
- Học từ: internal catalog export (`Vòng Bi Đũa Côn Một Dãy KYS LM501349/10`) + vongbikg.com (`Vòng Bi Côn ... 387A/382S`, dims để mm riêng).
