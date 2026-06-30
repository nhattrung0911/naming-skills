# Quy trình END-TO-END: Mô tả + Mã hãng → bản ghi chuẩn hóa

Mục tiêu: file dụng cụ cầm tay có `Description` (+`Mã hãng`) → loại + category_id + **tên đúng form** + **sheet chuẩn có cột thông số kĩ thuật thật cho từng mã**.

> Skill = CẤU TRÚC (form + đơn vị + loại→category) deterministic. **SỐ LIỆU = SEARCH MÃ HÃNG, CÓ NGUỒN — bắt buộc.** KHÔNG suy từ mã/part# cũ, KHÔNG bịa, KHÔNG lấy số mô tả làm chân lý (chỉ là draft đối chiếu).

## Bước 0 — Nhận file
Xác định cột mô tả (`Description`) và cột **Mã hãng** (mã chuẩn). Bỏ qua part# tiền tố nội bộ (KTN-, DL-) — chỉ dùng cho đối chiếu, KHÔNG đưa vào tên.

## Bước 1 — Chạy engine hàng loạt
```bash
python scripts/standardize.py input.xlsx --sheet Sheet3 \
 --desc-col Description --code-col "Mã hãng" -o out.xlsx
```
Output = **sheet chuẩn**: 4 cột gốc + Tên chuẩn/category_id/Loại/status + cột `TS_*` TRỐNG + Nguồn + `draft_*`. Mỗi dòng nhận `status`:
- **NEEDS_WEB** — đã ra loại + category + tên; **chờ search mã hãng điền `TS_*` + Nguồn**. (mặc định mọi dòng có loại — engine KHÔNG tự set OK)
- **REVIEW_TYPE+NEEDS_WEB** — loại đoán mơ hồ (Kìm/Búa/Cảo trống đặc trưng) → xác nhận loại RỒI search.
- **UNKNOWN_TYPE** — không suy được loại → Bước 2 (search để biết loại + TS).

## Bước 2 — SEARCH theo MÃ HÃNG (BẮT BUỘC mọi dòng)
Với MỖI mã hãng (đây là phần lõi — không bỏ qua):
1. Tra catalog HÃNG theo đúng mã: Sata (sata.com / sata.vn), Stanley, Bosch (bosch-professional), Anex, Tsunoda, Mitutoyo, Kingtony (kingtony.com)...
2. Lấy **thông số kĩ thuật thật** điền cột `TS_*` (xem `spec_schema.md` — thông số bắt buộc theo họ): hệ dẫn động, cỡ/khẩu, số cạnh, chiều dài, dải lực + đơn vị, số chi tiết, vật liệu, tiêu chuẩn. Đổi inch↔mm khi cần (1 in = 25.4 mm).
3. **Đối chiếu với `draft_*`** (gợi ý từ mô tả). Lệch → TIN catalog hãng, sửa lại. Mô tả/mã cũ KHÔNG phải nguồn chân lý.
4. **Ghi Nguồn (URL)** vào cột Nguồn. Không có nguồn tin cậy → giữ NEEDS_WEB, KHÔNG bịa.
5. Mã không ra loại (UNKNOWN) → search xác định loại + category trước, rồi điền TS.

## Bước 3 — Điền lại bằng engine
```python
from handtool_engine import standardize
rec = standardize("Cờ Lê Vòng Miệng 18 mm", ma_hang="STMT80231-8B", brand="Stanley")
# rec['name'], rec['category_id'], rec['status']
```
Mô tả sửa/bổ sung xong → chạy lại cả file.

## Bước 4 — CỔNG QA (trước khi báo done)
1. **TS_ đủ + có Nguồn**: thông số bắt buộc theo họ (xem `spec_schema.md`) đã điền, mỗi dòng có URL catalog hãng → mới được set `OK`.
2. **Form đúng**: `{Tên+Đặc trưng} {Thông số} {Hãng} {Mã}`. Mã = mã hãng, không tiền tố nội bộ.
3. **Đơn vị chuẩn**: `8 mm`, `1/2 Inch`, `40-200 Nm`, `24 Chi Tiết` (xem `attributes.md`).
4. **Category hợp lệ**: lấy từ `category_map.json`; không tự chế id. `Bộ X` → category bộ, không phải lẻ.
5. **Đối chiếu ground-truth + draft**: input có dòng đã đặt tên chuẩn (vd Sheet3) → so khớp loại; TS_ lệch draft → tin catalog hãng.
6. **Không bịa số**: chưa search được → để trống TS_ + giữ NEEDS_WEB.

## Bước 5 — Tự review rồi báo done
In thống kê: `tổng | OK (TS_ đủ + nguồn) | NEEDS_WEB còn lại | UNKNOWN_TYPE`. Chỉ báo done khi mọi dòng OK (TS_ điền + có nguồn) hoặc còn lại đã ghi rõ lý do chưa tra được.

## Lỗi thường gặp (đã gặp khi build)
- **Mã chứa số+M/F** (vd `423024M`, `373A13M`) làm regex F/M (đầu chuyển đổi) match nhầm → rule 4314 CHỈ khớp khi có dấu inch `"` trước F/M, không khớp số trần.
- **`Bộ ...` rơi vào loại lẻ** nếu rule bộ đặt sau → luôn để rule `Bộ` lên đầu.
- **"Cờ Lê … Tự Động"** = bánh cóc (3982), khác cờ lê vòng miệng thường (3981).
- **"Lục Giác Chìm/Col"** trong corpus là BU LÔNG đầu lục giác — KHÔNG phải handtool, loại bỏ.
- **Đầu tuýp lẻ** có cả cỡ mm + dẫn động inch — đừng coi cỡ mm là drive.
