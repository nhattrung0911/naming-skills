# Category map (vòng bi)

Engine gán category qua `category_map.json` (loại chuẩn → category_id). Bảng dưới để người đọc đối chiếu.

## Bảng category chính (độ tin cậy cao)
| category_id | Loại chuẩn | Mã điển hình |
|---|---|---|
| **1604** | Vòng Bi Cầu Rãnh Sâu | 6xxx, 60/62/63/64/68/69/16, mini 6xx |
| **1605** | Vòng Bi Tiếp Xúc Góc Một Dãy | 7xxx, B7xxx, 70/72/73 |
| **1607** | Vòng Bi Cầu Tự Lựa | 12xx, 13xx, 22xx, 23xx |
| **2988** | Vòng Bi Côn 1 Dãy | 302/303/313/320/322/323/329/330/331/332xx, inch Timken |
| **4625** | Vòng Bi Côn 2 Dãy | 2-row taper |
| **4265** | Vòng Bi Đũa Trụ 1 Dãy | N/NU/NJ/NUP/NF (dãy 2/3/4/10/22/23) |
| **4622** | Vòng Bi Đũa Trụ 2 Dãy | NN/NNU |
| **4268** | Vòng Bi Tang Trống | 213/222/223/230/231/232/240/241xx |
| **4272** | Vòng Bi Chặn 1 Chiều (cầu chặn) | 511/512/513/514xx |
| **4270** | Vòng Bi Tang Trống Chặn Trục | 293/294xx (thrust spherical) |
| **4256** | Vòng Bi Kim Vỏ Dập | HK, BK, BA (drawn cup) |
| **4257** | Vòng Bi Kim | NA, RNA, NART, NK, TAF |
| **4255** | Vòng Bi Kim Với Lồng Giữ | KT, K-cage |
| **4637** | Vòng Bi Kim Chặn | AXK + AS washers |
| **1582** | Vòng Bi Kim Kết Hợp Cầu Chặn Trục | NKX, NX |
| **3842** | Gối Đỡ Vòng Bi (chân đế) | UCP, UKP |
| **3848** | Gối Đỡ Vòng Bi Mặt Bích Hình Vuông | UCF, UKF |
| **3850** | Gối Đỡ Vòng Bi Mặt Bích Hình Thoi | UCFL, UCFA |
| **3844** | Gối Đỡ Vòng Bi (căng băng tải) | UCT |
| **3846** | Gối Đỡ Vòng Bi Treo | UCHA |
| **3845** | Vòng Bi Cho Gối Đỡ (insert) | UC2xx, UC3xx, UK |
| **4267** | Gối Đỡ Hai Nửa | SNL, SN, SNK |
| **6890 / 6995** | Vòng Bi Mắt Trâu (rod end) | SA, SI, GE, POS |
| **6891** | Vòng Bi Cam (cam follower) | CF, KR, NUKR |
| **7065** | Vòng Bi Ly Hợp (one-way) | CSK, HF, TFS |
| **7257** | Vòng Bi Cầu Lỗ Côn | …K |
| **1555 / 1563 / 1567** | Vòng Bi Cầu Rãnh Sâu Inox / mini Inox | S6xxx, SS6xxx, SB |
| **1577** | Vòng Bi Không Cần Tra Dầu Mỡ | SE…PR |

> Gối đỡ: chọn category theo HÌNH DÁNG vỏ (chữ cái sau UC/UK), không theo cỡ. Inox: mã có S/SS/SB hoặc Inox/440C → dùng biến thể Inox.

## Phụ lục — toàn bộ 80 category trong dữ liệu (id | số dòng | loại trội)
> Loại "Vòng Bi" (chung chung) ở 6877/3836/4757 là dữ liệu gốc chưa phân loại kỹ — KHÔNG dùng làm đích; phân loại theo mã thực tế.

| category_id | loại trội |
|---|---|
| 1604 | Vòng Bi Cầu Rãnh Sâu |
| 6877 | (Gối đỡ SKF FNL/housing — phân loại theo mã) |
| 1605 | Vòng Bi Tiếp Xúc Góc Một Dãy |
| 4378 | Gối Đỡ Trục Chữ T (shaft support SK) |
| 4376 | Gối Đỡ Trục Mặt Bích Nhỏ |
| 4265 | Vòng Bi Đũa Trụ 1 Dãy |
| 1607 | Vòng Bi Cầu Tự Lựa |
| 2988 | Vòng Bi Côn 1 Dãy |
| 4380 | Gối Đỡ Trục Nhỏ Gọn Tách Đôi |
| 4272 | Vòng Bi Chặn 1 Chiều |
| 4268 | Vòng Bi Tang Trống |
| 4379 | Gối Đỡ Trục Chữ L |
| 3842 | Gối Đỡ Vòng Bi (chân đế UCP) |
| 4256 | Vòng Bi Kim Vỏ Dập |
| 3848 | Gối Đỡ Vòng Bi Mặt Bích Hình Vuông |
| 3845 | Vòng Bi Cho Gối Đỡ |
| 1577 | Vòng Bi Không Cần Tra Dầu Mỡ |
| 4257 | Vòng Bi Kim |
| 3844 | Gối Đỡ Vòng Bi (UCT căng băng tải) |
| 3850 | Gối Đỡ Vòng Bi Mặt Bích Hình Thoi |
| 4622 | Vòng Bi Đũa Trụ 2 Dãy |
| 3609 | Vòng Bi Rãnh Sâu Có Mặt Bích |
| 6891 | Vòng Bi Cam |
| 3849 | Gối Đỡ Vòng Bi |
| 4255 | Vòng Bi Kim Với Lồng Giữ |
| 6890 | Vòng Bi Mắt Trâu |
| 1578 | Vòng Bi Cầu Nhựa POM |
| 4587 | Vòng Bi Cầu 1 Dãy Hướng Tâm |
| 4267 | Gối Đỡ Hai Nửa |
| 1574 | Vòng Bi Ít Sinh Hạt Bụi Mỡ |
| 4270 | Vòng Bi Tang Trống Chặn Trục |
| 7065 | Vòng Bi Ly Hợp |
| 1567 | Vòng Bi Cầu Rãnh Sâu Inox |
| 3610 | Vòng Bi Cầu Rãnh Sâu (Có Mặt Bích) |
| 4637 | Vòng Bi Kim Chặn |
| 1558 | Vòng Bi Cầu Rãnh Sâu Mini Inox Có Mặt Bích |
| 1582 | Vòng Bi Kim Kết Hợp Cầu Chặn Trục |
| 6995 | Vòng Bi Mắt Trâu |
| 7278 | Vòng Bi Cầu Cho Gối Đỡ |
| 1570 | Vòng Bi Tra Mỡ Chịu Nhiệt 160° |
| 3829 | Vòng Bi Dùng Cho Máy (Bosch) |
| 4673 | Gối Đỡ Vòng Bi |
| 1571 | Vòng Bi Tra Mỡ Chịu Nhiệt 230° |
| 7257 | Vòng Bi Cầu Lỗ Côn |
| 6880 | Gối Đỡ Vòng Bi |
| 1555 | Vòng Bi Cầu Rãnh Sâu Inox |
| 4675 | Gối Đỡ Dạng Tròn |
| 1553 | Vòng Bi Rãnh Sâu Nhỏ Inox |
| 1554 | Vòng Bi Đường Kính Nhỏ Inox |
| 3846 | Gối Đỡ Vòng Bi Treo |
| 7271 | Gối Đỡ (FL Nachi) |
| 3851 | Gối Đỡ Vòng Bi |
| 1576 | Vòng Bi Chống Nước Chịu Nhiệt Inox |
| 1583 | Vòng Bi Đũa Chặn Trục |
| 7283 | Vòng Bi Chữ Thập (universal joint) |
| 1575 | Vòng Bi Ít Sinh Hạt Bụi Có Mặt Bích |
| 4674 | Gối Đỡ Vòng Bi Mặt Bích Hình Vuông |
| 4678 | Vòng Bi Có Gối Đỡ Chữ T |
| 1563 | Vòng Bi Cầu Rãnh Sâu Mini Inox |
| 7034 | Vòng Bi Trượt Trục Tròn |
| 7223 | Gối Đỡ Vòng Bi Treo |
| 1573 | Vòng Bi Có Cấy Bi |
| 1584 | Vòng Bi Tự Chỉnh |
| 3381 | Vòng Bi Trượt Trục Tròn Đế Vuông |
| 4625 | Vòng Bi Đũa Côn 2 Dãy |
| 7077 | Gối Đỡ Vòng Bi Mặt Bích Tròn |
| 3380 | Vòng Bi Trượt Trục Tròn Hở |
| 7064 | Gối Đỡ Vòng Bi |
| 3768 | Vòng Bi Mắt Trâu (ren) |
| 4219 | Gối Đỡ Trục Trượt Tròn |
| 2943 | Vòng Bi Căng Đai |
| 4623 | Vòng Bi Đũa Trụ 4 Dãy |
| 4269 | Vòng Bi Tang Trống Lỗ Côn |
| 4254 | Vòng Bi Đũa Kim Đỡ Chặn |
