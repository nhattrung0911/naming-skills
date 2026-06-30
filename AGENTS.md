# AGENTS.md — chạy với mọi agent (Codex, Gemini, Claude…)

Skill này **agent-agnostic**: phần Python chạy ở đâu cũng được; phần "research" dùng **web-search tool của agent đang chạy**. Quy trình giống nhau cho mọi agent.

> Claude Code: gõ `/naming @file` (đọc `.claude/skills/*/SKILL.md`).
> Codex / Gemini / agent khác: làm theo 3 bước dưới.

## Phần deterministic (Python, không cần mạng, miễn phí)
- Nhận domain (vòng bi / dụng cụ): `naming/scripts/detect_domain.py`
- Tách mã + cache + dedup: `naming-handtools/scripts/extract_codes.py`
- Ghép sheet chuẩn + gán category + cache: `naming-handtools/scripts/build_sheet.py`
- Vòng bi: `naming-bearings/scripts/bearing_engine.py` (tên + d×D×B mã mét chuẩn, không cần search)

## 3 bước (mọi agent)

**B1. Tách mã (rẻ — bỏ mã đã cache + mã trùng)**
```bash
python <skill>/naming-handtools/scripts/extract_codes.py INPUT.xlsx --cache cache.json
```
→ JSON: chỉ `need_research=true` mới phải tra. `need_research=false` lấy lại từ cache.

**B2. Research (dùng web-search của AGENT — chỉ mã need_research)**
Chia lô ~8–12 mã. Với mỗi mã: tra **≥2 nguồn uy tín** (trang hãng + đại lý có thông số), chéo kiểm.
Trả JSON array theo schema:
```json
{ "code":"423024M", "brand":"Kingtony", "type":"Đầu Tuýp Lẻ",
  "name_vi":"Đầu Tuýp 24 mm 1/2 Inch Kingtony 423024M",
  "specs":{"drive":"1/2 Inch","size_mm":24,"points":6,"length":null,
           "torque_min":null,"torque_max":null,"torque_unit":null,
           "pieces":null,"material":"CrV","standard":null,"features":null},
  "sources":["url1","url2"], "confidence":"high|medium|low" }
```
Quy ước tên: `{Tên+Đặc trưng} {Thông số} {Hãng} {Mã}`. Đơn vị: `24 mm`,`1/2 Inch`,`40-200 Nm`.
KHÔNG bịa: thiếu nguồn → `confidence:"low"`, specs để null. Lưu vào `research.json`.

**B3. Ghép sheet + cập nhật cache**
```bash
python <skill>/naming-handtools/scripts/build_sheet.py research.json --orig INPUT.xlsx --cache cache.json -o OUT.xlsx
```
→ sheet: cột gốc + Tên chuẩn + category_id + Loại + `TS_*` + Nguồn + status. Cache tự cập nhật.

## Tối ưu chi phí (đã tích hợp)
- **Cache** `cache.json`: lần sau chỉ tra mã mới → list lớn/incremental rất rẻ.
- **Dedup** mã trùng tự gộp.
- **Deterministic-first**: vòng bi mã mét chuẩn ra tên + d×D×B **không cần search**; chỉ mã thiếu thông số mới research.
- **Batch + early-stop**: gộp mã/lô, dừng ở 2 nguồn khớp.

## Nguyên tắc cứng (mọi agent)
- Thông số = search ≥2 nguồn uy tín, **có nguồn**. KHÔNG bịa, KHÔNG suy từ format mã.
- `category_id` = taxonomy của bạn (file `category_ids.local.json`, gitignored). Không có → để trống, vẫn ra tên + loại.

`<skill>` = `.claude/skills` (clone) hoặc thư mục plugin đã cài.
