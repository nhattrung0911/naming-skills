---
name: naming-bearings
slug: naming-bearings
description: "Chuẩn hóa dữ liệu VÒNG BI (bearings) từ MÃ (+HÃNG): nhận diện loại vòng bi, gán category_id, tra/điền kích thước d×D×B theo ISO, phát hiện nắp chắn, sinh tên chuẩn form '{Loại} dxDxB mm {Nắp chắn} {Hãng} {Mã}'. Mã ISO/mét resolve bằng bảng; mã inch (Timken)/GOST/lạ thì web-search số liệu thật rồi điền. Sub-skill domain BEARING của /naming. Dùng khi: chuẩn hóa/đặt tên/điền kích thước/gán category vòng bi, standardize bearing data, file có cột mã vòng bi (6xxx, UCP, 30xxx, NU..., 222xx...)."
---

# Bearing Naming & Standardizer

Skill này dạy **CÁCH & CẤU TRÚC đặt tên + phân loại** vòng bi — KHÔNG phải kho dữ liệu kích thước để tra cứng.

> ⚠️ **NGUYÊN TẮC CỐT LÕI:** Kích thước/thông số **mỗi hãng mỗi khác** (hậu tố E/ECP/EM/DB/DF, dung sai, series riêng, hệ inch…). Vì vậy **PHẢI search catalog THẬT của đúng hãng → thu thập d/D/B + thông số thật → rồi mới ghép vào cấu trúc tên.** Bảng số nhúng trong skill chỉ là *bootstrap cho mã ISO mét tiêu chuẩn* (6204 = 20×47×14 ở mọi hãng) để chạy nhanh — KHÔNG được coi là nguồn chân lý cho mã có hậu tố/đặc biệt/inch.

Skill cho 2 thứ deterministic (đúng mọi hãng): **(1) CẤU TRÚC tên** và **(2) LOẠI → category_id**. Phần **số liệu** thì đi tìm thật.

## Khi nào dùng
- File/CSV/Excel chỉ có `part_number` (và đôi khi `brand`), cần đặt tên + category chuẩn.
- Cần hiểu/áp dụng đúng cấu trúc tên + map category .
- Cần điền d×D×B, nắp chắn, vật liệu — **bằng cách tra catalog hãng thật**, ghép vào cấu trúc.

## Tài sản trong skill
| File | Vai trò |
|---|---|
| `bearing_engine.py` | Engine: parse mã → loại, category, d/D/B, seal, tên. Gọi `standardize(part_number, brand=None, dims=None)`. |
| `dimension_tables.py` | Bảng kích thước ISO (cầu/côn/đũa/chà/tang trống/kim/gối đỡ) + dict `WEB` (mã inch/GOST đã tra) đã kiểm chứng vs catalog SKF/FAG/NSK/Timken. |
| `category_map.json` | Map loại vòng bi → `category_id` . |
| `standardize.py` | Driver xử lý hàng loạt CSV/Excel → file chuẩn hóa + danh sách `NEEDS_WEB`. |
| `naming_convention.md` | Văn phong đặt tên + template từng loại + từ vựng nắp/vật liệu. |
| `category_map.md` | Bảng category (người đọc) + 80 category gốc. |
| `dimension_standards.md` | Tiêu chuẩn ISO, quy ước mã cỡ (bore code), quy tắc inch phân số, seal. |
| `workflow.md` | Quy trình end-to-end chi tiết + giao thức web-search + cổng QA. |

## Quy trình END-TO-END (từ chỉ có mã + hãng)

> Đọc `workflow.md` để biết chi tiết. Tóm tắt:

1. **Phân tích cấu trúc (engine)** — `standardize.py` đọc cột mã (+hãng), engine xác định **LOẠI → category_id → cấu trúc tên + nắp chắn** (phần này đúng mọi hãng). Engine cũng đề xuất d/D/B *nháp* nếu mã là ISO mét tiêu chuẩn.
2. **SEARCH THẬT theo HÃNG (bắt buộc cho số liệu)** — với mỗi mã, tra catalog CHÍNH của đúng hãng (vd SKF skf.com, NTN ntnglobal, Koyo/JTEKT, NSK, FAG/Schaeffler medias, Timken cad.timken.com, C&U, Asahi…). Lấy d, D, B/T + thông số THẬT của đúng hậu tố/series đó. Đổi inch→mm (1in=25.4mm). **KHÔNG dùng số nháp của engine làm cuối nếu mã có hậu tố/đặc biệt/inch — phải đối chiếu catalog hãng.** Ghi nguồn (URL).
3. **Ghép vào cấu trúc** — `standardize(code, brand, dims=(d,D,B))` để sinh tên đúng form + giữ category.
4. **Cổng QA**:
 - `d < D` luôn đúng. `d ≥ D` → sai, sửa.
 - Số nháp engine vs số catalog hãng lệch → TIN catalog hãng.
 - Tên đúng form `{Loại} dxDxB mm {Nắp chắn} {Hãng} {Mã}`. Inch → phân số, không dấu chấm.
 - Không tra được nguồn hãng → để trống D/B + `CAN_REVIEW`, KHÔNG bịa.
5. **Tự review rồi mới báo done** — thống kê OK / cần-search / CAN_REVIEW + nguồn.

## Nguyên tắc cứng
- **Số liệu = search catalog hãng thật, có nguồn.** Mỗi hãng/hậu tố/series khác nhau → không lấy số nhúng làm chân lý. Bảng nhúng chỉ là bootstrap ISO mét tiêu chuẩn.
- **Cấu trúc tên + category = deterministic** (đúng mọi hãng) — đây là phần lõi skill dạy.
- **Category lấy từ `category_map.json`.** Không tự chế id mới.
- **Inch → phân số/hỗn số** (vd `2-1/4 x 3-13/16 x 1 inch`), không dấu chấm.
- **Không phải vòng bi** (măng xông H…, mã lạ) → `SLEEVE`/`CAN_REVIEW`, không gán dims.

## Dùng nhanh
```bash
# một mã
python bearing_engine.py "NTN-6204-ZZ" "KOYO 32216" "UCP206 Asahi"

# hàng loạt: cột mã (+brand) trong CSV/Excel
python standardize.py input.csv --code-col part_number --brand-col brand -o output.csv
# -> output.csv (đã chuẩn hóa) + output.NEEDS_WEB.csv (danh sách cần tra web)
```
