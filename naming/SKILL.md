---
name: naming
description: "Entry CHUNG chuẩn hóa tên + thông số sản phẩm từ danh sách MÃ HÃNG. Tự nhận DOMAIN (vòng bi / dụng cụ cầm tay) rồi route sang sub-skill đúng (naming-bearings / naming-handtools). Dùng khi user gõ /naming @file (Excel/CSV có cột mã hãng), hoặc yêu cầu: chuẩn hóa/đặt tên/điền thông số + category cho list mã sản phẩm mà chưa rõ là vòng bi hay dụng cụ, hoặc file lẫn nhiều loại. Mở rộng được: thêm domain mới = thêm registry + 1 sub-skill."
---

# /naming — Router chuẩn hóa tên + thông số theo MÃ HÃNG

Skill CHUNG (kiểu dispatcher). Nhận file có **cột mã hãng** → tự phân loại từng dòng theo **domain** → route sang sub-skill chuyên trách. Output: sheet chuẩn (mã + Tên chuẩn/description + category_id + thông số kĩ thuật + Nguồn + status).

## Registry domain (mở rộng tại đây)
| Domain | Sub-skill | Tín hiệu nhận diện | Số liệu |
|---|---|---|---|
| **bearing** (vòng bi) | `naming-bearings` | desc "Vòng Bi/Bạc Đạn/Gối Đỡ"; brand SKF/FAG/NSK/NTN/Koyo/Timken/C&U; mã 6xxx·62/22·NU·30xxx·222xx·UCP·GE… | d×D×B từ bảng ISO (mã chuẩn) / web-search (inch/GOST) |
| **handtool** (dụng cụ cầm tay) | `naming-handtools` | desc cờ lê/kìm/tua vít/đầu tuýp/lục giác/cảo/cần lực/búa…; brand Sata/Stanley/Bosch/Anex/Kingtony… | research subagent đa nguồn uy tín ≥2 |
| **unknown** | (hỏi / mặc định research) | không tín hiệu | → naming-handtools research, hoặc hỏi user |

## Quy trình (chạy full)

### B1 — Phát hiện domain từng dòng
```bash
python "<skill>/scripts/detect_domain.py" "<file>" [--sheet <s>] [--code-col "<cột>"]
```
Trả JSON `{code_col, n, counts:{bearing,handtool,unknown}, rows:[{i,code,domain,why}]}`.
- `error` (không thấy cột mã) → hỏi user tên cột.
- In tóm tắt cho user: tổng + số mỗi domain.

### B2 — Tách file theo domain
Chia `rows` thành 2 (hoặc 3) tập theo `domain`. Mỗi tập → 1 file con (cùng cột mã), lưu scratchpad: `part_bearing.xlsx`, `part_handtool.xlsx`, `part_unknown.xlsx`.

### B3 — Route + chạy sub-skill cho mỗi tập (CÓ DÒNG mới chạy)
- **bearing** → **invoke Skill `naming-bearings`**, theo SKILL.md của nó (engine gán loại/category/d-D-B + web-search mã inch/GOST). Input = `part_bearing.xlsx`.
- **handtool** → **invoke Skill `naming-handtools`**, theo SKILL.md của nó (dispatch subagent research đa nguồn → description + TS_*). Input = `part_handtool.xlsx`.
- **unknown** → ưu tiên hỏi user; nếu user muốn auto → đưa vào `naming-handtools` (luồng research tự xác định loại), mã nào research thấy là vòng bi thì chuyển sang bearing.

> Nếu file CHỈ 1 domain (counts cho thấy thuần) → bỏ qua tách, route thẳng cả file.

### B4 — Gộp + báo cáo
Gộp output các domain về 1 sheet chuẩn (giữ thứ tự dòng gốc theo `i` nếu cần). Báo cáo:
```
tổng N | bearing: x (OK/REVIEW) | handtool: y (OK/REVIEW) | unknown: z
-> <file out> + danh sách REVIEW/UNKNOWN cần xử lý
```

## Tài sản
| File | Vai trò |
|---|---|
| `scripts/detect_domain.py` | Phân loại dòng → bearing/handtool/unknown (desc>brand>code). |
| sub-skill `naming-bearings` | Domain vòng bi (engine ISO + web-search dims). |
| sub-skill `naming-handtools` | Domain dụng cụ cầm tay (research subagent đa nguồn). |

## Nguyên tắc cứng (chung mọi domain)
- **Số liệu = data thật / search có nguồn.** KHÔNG bịa, KHÔNG suy từ format mã.
- **Cấu trúc tên + category = deterministic** theo từng sub-skill (không tự chế category_id).
- **Mã = mã hãng input.** Bỏ tiền tố nội bộ (KTN-/DL-), giữ hậu tố/dấu.
- Phân loại nhầm rủi ro thấp: ưu tiên DESC keyword; thiếu thì brand; cuối mới đoán theo mã. Không chắc → `unknown`, hỏi user.
- **Mở rộng domain mới**: thêm pattern vào `detect_domain.py` + Registry + tạo sub-skill `naming-<domain>`.
