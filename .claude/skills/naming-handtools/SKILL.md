---
name: naming-handtools
description: "Từ danh sách MÃ HÃNG dụng cụ cầm tay -> tự NGHIÊN CỨU đa nguồn uy tín bằng subagent Claude Code, tạo DESCRIPTION (tên chuẩn tiếng Việt) + THÔNG SỐ KĨ THUẬT thật cho từng mã, gán category_id, xuất sheet chuẩn. Dùng khi user gõ /naming-handtools @file (Excel/CSV có cột mã hãng), hoặc yêu cầu: đặt tên + tra thông số dụng cụ cầm tay từ mã hãng, chuẩn hóa handtool theo mã, làm description + spec cho list mã dụng cụ (cờ lê, kìm, tua vít, đầu tuýp, lục giác, cảo, cần siết lực, búa, thước, mỏ lết...)."
---

# /naming-handtools — Tự tạo description + thông số kĩ thuật từ mã hãng

Input: file Excel/CSV có **cột mã hãng** (có thể KHÔNG có description). Output: **sheet chuẩn** = mã + Tên chuẩn (description) + category_id + **cột thông số kĩ thuật TS_*** + Nguồn + status.

> ⚠️ **NGUYÊN TẮC CỨNG:** Mọi description & thông số **PHẢI lấy từ SEARCH NHIỀU NGUỒN UY TÍN, chéo kiểm ≥2 nguồn khớp**. KHÔNG bịa, KHÔNG suy từ format mã, KHÔNG nhận 1 nguồn rao vặt làm chân lý. Không tra được → status REVIEW, để trống, KHÔNG đoán.

## Quy trình agent (chạy full, không hỏi lại trừ khi thiếu cột mã)
> Trong các lệnh dưới, `<SKILL_DIR>` = thư mục chứa SKILL.md này (cùng cấp `scripts/`) — dùng đường dẫn tuyệt đối.

### B1 — Đọc mã (+ cache để RẺ)
```bash
python "<SKILL_DIR>/scripts/extract_codes.py" "<file>" [--code-col "<cột>"] --cache cache.json
```
Trả `{n, n_todo, n_cached, rows:[{i,code,brand,desc,need_research}]}`. **CHỈ research mã `need_research=true`** (mã trùng đã gộp, mã đã cache bỏ qua). `error` → hỏi tên cột.

### B2 — Nghiên cứu đa nguồn (DISPATCH SUBAGENT SONG SONG) — chỉ mã `need_research`
Chia mã `need_research` thành lô (~8–12 mã/agent). Mỗi lô = 1 subagent song song (nhiều Agent trong 1 message), dùng **template "Prompt subagent"**. Mỗi lô trả **JSON list** theo Schema → ghi `research_part<k>.json`. Dừng ở 2 nguồn khớp (early-stop).

### B3 — Gộp + ghép sheet + cập nhật cache
```bash
python "<SKILL_DIR>/scripts/build_sheet.py" research_all.json --orig "<file>" \
 --code-col "<code_col>" --cache cache.json --min-sources 2 -o "<out>.xlsx"
```
Engine gán `category_id` (nếu có `category_ids.local.json`), đổ TS_*, set status. **Mọi dòng gốc giữ nguyên** (mã trùng có cờ `Trùng`, điền cùng kết quả). `status=OK` khi ≥ `--min-sources` nguồn (client chỉnh được). `--cache` bù mã đã cache + ghi cache mới.

### B4 — Cổng QA + báo cáo
- Mọi dòng `OK` phải có **≥2 nguồn** + tên chuẩn + category. `REVIEW_LOW_SOURCE`/`REVIEW`/`UNKNOWN_TYPE` → liệt kê để user xử lý.
- Đối chiếu: nếu file gốc có sẵn vài description → so khớp loại/cỡ; lệch lớn → kiểm lại nguồn.
- In thống kê: `tổng | OK | REVIEW | UNKNOWN` + đường dẫn file + danh sách mã chưa chắc.

## Prompt subagent (template — điền {BRAND_HINT} {CODES})
```
Bạn là chuyên gia dữ liệu dụng cụ cầm tay. Với MỖI mã hãng dưới đây, SEARCH NHIỀU NGUỒN UY TÍN
và trả thông tin THẬT. Mã + (gợi ý hãng nếu có): {CODES}

NGUỒN ưu tiên (chéo kiểm tối thiểu 2 nguồn khớp nhau):
1. Trang chính hãng / catalog hãng (vd kingtony.com, sata.cn/sata.vn, stanleytools, bosch-professional,
 anextool, mitutoyo, tsunoda...). Tìm bằng web-search "<mã> <hãng?> specification".
2. Đại lý/sàn uy tín có thông số kĩ thuật rõ (không lấy trang rao vặt thiếu nguồn).
Đổi inch<->mm khi cần (1 in = 25.4 mm). KHÔNG bịa: không tìm được/chỉ 1 nguồn yếu -> confidence "low".

Với mỗi mã trả 1 object JSON (KHÔNG văn bản thừa), gộp thành 1 JSON array:
{
 "i": <giữ index nếu được cấp>, "code": "<mã>", "brand": "<hãng>",
 "type": "<loại tiếng Việt: vd Đầu Tuýp Lẻ / Cờ Lê Vòng Miệng / Kìm Cắt / Cần Siết Lực ...>",
 "name_vi": "<TÊN CHUẨN tiếng Việt theo form: {Tên+Đặc trưng} {Thông số} {Hãng} {Mã}>",
 "specs": {"drive": "<1/4|3/8|1/2|3/4|1 Inch | null>", "size_mm": <số|null>, "points": <6|12|null>,
 "length": "<vd 200 mm | 8 Inch | null>", "torque_min": <số|null>, "torque_max": <số|null>,
 "torque_unit": "<Nm|ft-lb|null>", "pieces": <số|null>, "material": "<CrV|CrMo|...|null>",
 "standard": "<DIN/ISO/ANSI|null>", "features": "<đặc điểm ngắn|null>"},
 "sources": ["<url1>", "<url2>"], "confidence": "high|medium|low"
}

Quy ước tên (name_vi): Tên loại + đặc trưng Title Case; đơn vị "24 mm","1/2 Inch","40-200 Nm","11 Chi Tiết";
hãng rồi mã ở cuối. Ví dụ: "Đầu Tuýp 24 mm 1/2 Inch Kingtony 423024M";
"Cần Siết Lực 1/2 Inch 40-200 Nm Kingtony 34467-1AG". Chỉ điền spec nào tra được; còn lại null.
CHỈ trả JSON array.
```

## Tài sản & tham chiếu
| File | Vai trò |
|---|---|
| `scripts/extract_codes.py` | Đọc Excel/CSV, tự dò cột mã/brand/desc -> JSON. |
| `scripts/build_sheet.py` | Gộp JSON nghiên cứu -> sheet chuẩn (category + TS_* + status). |
| `scripts/handtool_engine.py` + `category_map.json` | Deterministic: loại->category, chuẩn hóa đơn vị. 84 leaf cate. |
| `references/spec_schema.md` | Schema cột TS_* + thông số bắt buộc theo họ. |
| `references/naming_convention.md` | Form tên + từ vựng đặc trưng (nhồi vào prompt subagent khi cần). |
| `references/category_map.md` | 84 category + ưu tiên nhận diện. |
| `references/attributes.md` | Quy ước đơn vị + thông số theo họ. |
| `references/workflow.md` | Quy trình + cổng QA chi tiết. |

## Nguyên tắc cứng
- **Thông số & description = search đa nguồn uy tín, chéo kiểm ≥2.** Không bịa, không suy từ mã, không lấy số mô tả cũ làm chân lý.
- **OK chỉ khi ≥2 nguồn khớp + có category.** Còn lại REVIEW/UNKNOWN — không đoán.
- **category_id từ `category_map.json`** (84 leaf). Không tự chế id.
- **Mã = mã hãng input** (bỏ tiền tố nội bộ KTN-/DL- nếu lẫn). Giữ nguyên hậu tố/dấu.
- Subagent chạy **song song theo lô**; mã không chắc → confidence low → REVIEW.