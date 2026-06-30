# AGENTS.md — chạy với mọi agent (Codex, Gemini, Claude…)

Skill này **agent-agnostic**: phần Python chạy ở đâu cũng được; phần "research" dùng **web-search tool của agent đang chạy**. Quy trình giống nhau cho mọi agent.

> Claude Code: gõ `/naming @file` (đọc `.claude/skills/*/SKILL.md`).
> Codex / Gemini / agent khác: làm theo 3 bước dưới.

## Phần deterministic (Python, không cần mạng, miễn phí)
- Nhận domain (vòng bi / dụng cụ): `naming/scripts/detect_domain.py`
- Tách mã + cache + dedup: `naming-handtools/scripts/extract_codes.py`
- Ghép sheet chuẩn + gán category + cache: `naming-handtools/scripts/build_sheet.py`
- Vòng bi: `naming-bearings/scripts/bearing_engine.py` (loại/tên/nắp chắn + d×D×B **NHÁP** để đối chiếu — số cuối vẫn search)

## 3 bước (mọi agent)

**B1. Tách mã (rẻ — bỏ mã đã cache + mã trùng)**
```bash
python <skill>/naming-handtools/scripts/extract_codes.py INPUT.xlsx --cache cache.json
```
→ JSON: chỉ `need_research=true` mới phải tra. `need_research=false` lấy lại từ cache.

**B2. Research (dùng web-search của AGENT — chỉ mã need_research, KHÔNG tra mã `dup`)**
Chia lô ~8–12 mã. Với mỗi mã: tra **≥N nguồn uy tín** (N = `--min-sources`, mặc định **2**; client prompt tăng để chắc hơn) — trang hãng + đại lý có thông số, chéo kiểm.
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
python <skill>/naming-handtools/scripts/build_sheet.py research.json --orig INPUT.xlsx \
  --cache cache.json --min-sources 2 -o OUT.xlsx
```
→ sheet: cột gốc + cờ `Trùng` + Tên chuẩn + category_id + Loại + `TS_*` + Nguồn + status. Cache tự cập nhật.
`status=OK` khi ≥ `min-sources` nguồn; mọi dòng (kể cả trùng) đều được điền.

## Tối ưu chi phí (đã tích hợp)
- **Cache** `cache.json`: lần sau chỉ tra mã mới → list lớn/incremental rất rẻ.
- **Đánh dấu trùng**: mã trùng **giữ đủ dòng** (cờ `Trùng`) — research **1 lần/mã**, dòng lặp dùng lại kết quả.
- **Deterministic-first**: **loại/tên/category** ra free; **số liệu** (cả d×D×B vòng bi) thì search + đối chiếu.
- **Số nguồn tùy chỉnh**: `build_sheet.py --min-sources N` (mặc định 2). Client muốn chắc hơn → tăng N (prompt "dùng 3 nguồn").
- **Batch + early-stop**: gộp mã/lô, dừng khi đủ N nguồn khớp.

## Nguyên tắc cứng (mọi agent)
- Thông số = search + đối chiếu **≥N nguồn uy tín (mặc định 2, client chỉnh), có URL**. KHÔNG bịa, KHÔNG suy từ format mã.
- Vòng bi: bảng ISO chỉ là **số nháp đối chiếu** — d×D×B cuối vẫn từ nguồn.
- `category_id` = taxonomy của bạn (file `category_ids.local.json`, gitignored). Không có → để trống, vẫn ra tên + loại.

`<skill>` = `.claude/skills` (clone) hoặc thư mục plugin đã cài.
