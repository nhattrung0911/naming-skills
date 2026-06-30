# Tiêu chuẩn kích thước & cách engine resolve

> ⚠️ **Bảng số trong `dimension_tables.py` chỉ là BOOTSTRAP cho mã ISO mét TIÊU CHUẨN** (vd 6204=20×47×14, đúng ở mọi hãng). Nó KHÔNG phải nguồn chân lý. Với mã có hậu tố hãng (E/ECP/EM/DB/DF/CC…), series riêng, hoặc hệ inch → **PHẢI search catalog hãng thật** để lấy số đúng, vì mỗi hãng mỗi khác. Bảng dùng để chạy nhanh + làm số nháp đối chiếu.

Kích thước biên d (lỗ), D (ngoài), B/T/H (rộng/cao) của mã ISO mét tiêu chuẩn là cố định theo tiêu chuẩn dưới đây — dùng làm điểm khởi đầu, luôn đối chiếu catalog hãng.

## Tiêu chuẩn theo loại
| Loại | Tiêu chuẩn | Bảng trong code |
|---|---|---|
| Cầu rãnh sâu 60/62/63/64/68/69/16, mini 6xx | ISO 15 / DIN 625 | T60,T62,T63,T64,T68,T69,T16,MINI |
| Cầu tự lựa 12/13/22/23 | ISO 15 | S12,S13,S22,S23 |
| Tiếp xúc góc 2 dãy 52/53 | ISO 15 | A52,A53 |
| Đũa trụ N/NU/NJ/NUP/NF (2/3/4/10/22/23) | ISO 15 (dùng chung biên với cầu cùng dãy) | T60/62/63/64, S22/S23 |
| Côn mét 302/303/313/320/322/323/329/330/331/332 | ISO 355 / DIN 720 | TR302…TR332 (D, T=rộng tổng) |
| Côn inch (Timken cone/cup) | ANSI/ABMA, catalog Timken | dict WEB |
| Chà cầu 511/512/513/514 | ISO 104 | TH511…TH514 (D, H) |
| Chà tang trống 293/294 | ISO 104 | ST293,ST294 |
| Tang trống 213/222/223/230/231/232/240/241 | ISO 15 | SR…, S13 |
| Kim chà AXK | ISO 104 | AXK |
| Gối đỡ UC/UK insert | JIS/ABMA | UC2,UC3 (D, B tổng) |

## Quy ước MÃ CỠ (bore code) → d (mm)
`00=10, 01=12, 02=15, 03=17`; từ `04` trở lên = **số × 5**. (vd 6204 → 04 → 20mm; 32216 → 16 → 80mm).
- Mini 3 chữ số (604,625,688…): d = chữ số cuối (604→4, 688→8).
- Gối đỡ UCxYY: YY = mã cỡ (UCP206 → 06 → 30mm).
- Inch: d lấy theo phân số inch gốc.

## Hệ INCH → phân số/hỗn số (KHÔNG dấu chấm)
Khi cả d,D,B đổi sang inch ra phân số sạch (mẫu ≤ 64): ghi `2-1/4 x 3-13/16 x 1 inch`. Cột số mm vẫn giữ thập phân chính xác. Hàm `inch_frac` trong engine làm việc này. Cup Timken có OD lẻ (vd 1.980"=50.292mm) không phải phân số → để mm.

## Thứ tự resolve trong engine (quan trọng)
`WEB → SPECIAL → AXK → PILLOW → (tiền tố N/NU/NJ/NUP/NF ⇒ đũa trụ) → 5-digit (chà/côn/tang trống) → ball 4-5 digit → mini`.
- Tiền tố đũa trụ phải resolve TRƯỚC ball, nếu không NU22xx bị nhầm thành cầu tự lựa dãy 22.
- Mã `H<số>` = măng xông (adapter sleeve) → KHÔNG phải vòng bi → trả None.
- Sai số nguồn: nếu `d ≥ D` → bore sai, tính lại từ mã cỡ.

## ⚠️ UK/UKP/UKF (lắp măng xông adapter) — KHÔNG dùng công thức
Bore (d) của UK* = **đường kính TRỤC** kẹp qua măng xông H23xx/H30xx — **KHÔNG phải mã×5**.
- Ví dụ: **UKP216 → trục 70 mm** (qua H2316), KHÔNG phải 80. UK218→80, UKP310→45.
- Không có quy luật ổn định (2xx, 3xx, cỡ 205 đều lệch) → **PHẢI search sản phẩm thật / măng xông H tương ứng**.
- Engine: UK* lấy d từ `UK_SHAFT` (giá trị đã search per-product); mã chưa có → NEEDS_WEB, KHÔNG đoán.
- D/B (đường kính ngoài/bề rộng insert) = theo envelope UC cùng mã cỡ (ổn định). Chỉ d (trục) là phải tra.
- UC (set-screw, vít định vị) thì bore = mã×5 (đúng) — chỉ UK adapter mới khác.

## Thêm mã mới đã tra web
Sửa `dimension_tables.py`, thêm vào dict `WEB`: `'<mã>': (d, D, B_hoặc_T)` — đơn vị mm, có ghi chú nguồn. Mã hệ inch nhớ đổi 1in = 25.4mm.

## Minh chứng / kiểm chứng
Bảng đã được đối chiếu với 726+ dòng dữ liệu thật (khớp 100%) và kiểm chứng độc lập các dãy hiếm (côn 331/332, chà 511/513/514, đũa trụ, chà tang trống) vs catalog SKF/FAG/NSK/NTN/Koyo/Timken + ISO. Khi thêm mã, ưu tiên catalog hãng > đại lý.
