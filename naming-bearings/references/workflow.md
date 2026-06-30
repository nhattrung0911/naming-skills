# Quy trình END-TO-END: từ chỉ có MÃ + HÃNG → bản ghi chuẩn hóa

Mục tiêu: nhận file chỉ có mã (và đôi khi hãng) → loại, category, **tên đúng cấu trúc** + **số liệu lấy từ search catalog hãng thật**.

> Skill = hiểu CẤU TRÚC (loại/category/template/nắp chắn — deterministic). SỐ LIỆU = search hãng thật. Đừng coi bảng nhúng là nguồn chân lý: mỗi hãng/hậu tố/series khác nhau.

## Bước 0 — Nhận file
Xác định cột mã (`part_number`) và cột hãng nếu có. Nếu hãng nằm chung trong mã (vd `NTN-6204-ZZ`, `UCP206 Asahi`) engine tự tách.

## Bước 1 — Chạy engine hàng loạt
```bash
python standardize.py input.csv --code-col part_number --brand-col brand -o output.csv
```
Mỗi dòng nhận `status`:
- **OK** — đủ loại + d/D/B + category + tên. Không cần làm gì thêm.
- **NEEDS_WEB** — nhận ra loại nhưng bảng KHÔNG có kích thước (mã inch/GOST/hiếm). → Bước 2.
- **UNKNOWN_TYPE** — không suy được loại từ mã. → Bước 2 (xác định loại + dims).
- **SLEEVE** — măng xông H… → không gán dims, đánh dấu phụ kiện.

`standardize.py` xuất thêm `output.NEEDS_WEB.csv` = danh sách mã cần tra.

## Bước 2 — Web-search cho NEEDS_WEB / UNKNOWN_TYPE
Với MỖI mã:
1. Tra catalog NHÀ SẢN XUẤT trước (cad.timken.com, skf.com, koyo, ntnglobal, nsk), rồi đại lý uy tín để cross-check.
2. Lấy **d, D, B/T** (mm). Nếu nguồn inch → đổi ×25.4, làm tròn 3 số lẻ.
3. Nhận diện loại (côn/cầu/đũa/…) để gán category.
4. **KHÔNG đoán.** Không tìm được nguồn tin cậy → để trống D/B + đánh dấu `CAN_REVIEW`, ghi lý do.
5. Ghi nguồn (URL/catalog) vào cột ghi chú để minh chứng.

Mẹo phân khối khi nhiều mã: gom theo họ (Timken inch /xx, GOST 7xxx…) và tra song song; mã cùng cup/cone chia sẻ D.

## Bước 3 — Điền lại bằng engine
Với mỗi mã đã có dims:
```python
from bearing_engine import standardize
rec = standardize("LM12649/10", brand="Timken", dims=(21.43, 50.005, 17.526))
# rec['name'], rec['category'], ...
```
Hoặc thêm mã vào dict `WEB` trong `dimension_tables.py` rồi chạy lại cả file (tự nhân rộng cho các lần sau).

## Bước 4 — CỔNG QA (bắt buộc, trước khi báo done)
1. **Bore < OD**: mọi dòng `d < D`. Có dòng `d ≥ D` → sai, sửa (thường bore nguồn rác → tính lại từ mã cỡ).
2. **Đối chiếu ground-truth**: nếu input có sẵn vài dòng đã biết d/D/B → so với engine; tỉ lệ khớp phải ~100%. Lệch → kiểm tra bảng.
3. **Tên hợp lệ**: chứa hãng + mã + (d×D×B). Hệ inch dùng phân số, không dấu chấm.
4. **Category hợp lệ**: lấy từ `category_map.json`; không tự chế id. Loại không map được → để trống + CAN_REVIEW.
5. **Không phải vòng bi**: măng xông/mã lạ → SLEEVE/CAN_REVIEW, không gán dims.

## Bước 5 — Tự review rồi báo done
In thống kê cuối:
```
tổng dòng | OK | NEEDS_WEB còn lại | CAN_REVIEW | bore>=OD (=0) | đối chiếu khớp
```
Chỉ báo "done" khi: 0 bore≥OD, 0 NEEDS_WEB chưa xử lý (hoặc đã chuyển CAN_REVIEW có lý do), đối chiếu khớp ~100%.

## Lỗi thường gặp (đã gặp thực tế)
- **NU22xx/NU23xx** dễ bị nhầm thành cầu tự lựa — engine đã ưu tiên tiền tố đũa trụ.
- **Măng xông H2307…** trùng lõi số với vòng bi 2307 → engine chặn `H\d`.
- **62/22, 63/28…** là cầu rãnh sâu lỗ phi chuẩn, KHÔNG phải côn.
- **331xx/332xx** là côn dãy RỘNG (DIN 720), không cùng biên với 303/302.
