# naming — Skill chuẩn hóa tên + thông số sản phẩm cho Claude Code

Bộ **skill** cho [Claude Code](https://claude.com/claude-code): đưa vào **danh sách mã hãng** →
tự ra **tên chuẩn (tiếng Việt) + thông số kĩ thuật + mã category**, bằng cách cho subagent
Claude Code **tự search nhiều nguồn uy tín** rồi điền.

> Dùng cho catalog phụ tùng công nghiệp. Repo **không kèm `category_id`** — output mặc định có
> **tên loại** chuẩn, `category_id` để trống. Gắn id theo ERP của bạn qua `category_ids.local.json`
> (gitignored) — xem [INSTALLATION.md](INSTALLATION.md).

## Có gì

| Skill | Việc |
|---|---|
| **`/naming`** | Cửa chung. Tự nhận mỗi dòng là **vòng bi** hay **dụng cụ cầm tay** rồi route đúng sub-skill. Mở rộng được: thêm domain = thêm 1 pattern + 1 sub-skill. |
| **`/naming-bearings`** | Vòng bi: nhận loại → category, điền d×D×B (bảng ISO cho mã mét chuẩn; search web cho mã inch/GOST), nhận nắp chắn, dựng tên chuẩn. |
| **`/naming-handtools`** | Dụng cụ cầm tay (cờ lê, kìm, tua vít, đầu tuýp, lục giác, cảo, cần siết lực, búa, thước…): cho subagent **chéo kiểm nhiều nguồn uy tín** → ra description + thông số. |

## Nguyên tắc cốt lõi (cứng)

**Thông số phải lấy từ data thật / search chéo kiểm có nguồn — KHÔNG bịa, KHÔNG suy từ format mã.**
Phần cấu trúc (loại → category, form tên, chuẩn hóa đơn vị) là deterministic; phần con số thì đi tìm thật.

## Cài & dùng nhanh

**Cách A — plugin marketplace:**
```
/plugin marketplace add nhattrung0911/naming-skills
/plugin install naming-skills@naming-skills
```

**Cách B — clone & dùng ngay:**
```bash
git clone https://github.com/nhattrung0911/naming-skills.git
cd naming-skills && pip install -r requirements.txt
```
Mở thư mục bằng Claude Code → skill trong `.claude/skills/` tự nhận.

Chi tiết + gắn `category_id` theo ERP của bạn: xem **[INSTALLATION.md](INSTALLATION.md)**.

## Dùng

Trong Claude Code, gõ:

```
/naming @danh_sach_ma.xlsx
```

File chỉ cần có **cột mã hãng** (tự dò tên cột: "Mã hãng" / "code" / "part_number" …).
Có thêm cột brand/description thì nhận domain chính xác hơn.

Biết trước loại thì gọi thẳng:

```
/naming-handtools @file.xlsx     # chắc chắn dụng cụ cầm tay
/naming-bearings  @file.xlsx     # chắc chắn vòng bi
```

### Ví dụ

**Đầu vào** (file Excel, chỉ 1 cột):

| Mã hãng |
|---|
| 423024M |
| 6205-2RS |
| 41117 |

**Đầu ra** (sheet chuẩn — rút gọn):

| Mã hãng | Tên chuẩn | category_id | Loại | TS_Hệ Dẫn Động | TS_Cỡ/Khẩu (mm) | Nguồn | status |
|---|---|---|---|---|---|---|---|
| 423024M | Đầu Tuýp 24 mm 1/2 Inch Kingtony 423024M | *(của bạn)* | Đầu Tuýp Lẻ | 1/2 Inch | 24 | kingtony.com; … | OK |
| 6205-2RS | Vòng Bi Cầu Rãnh Sâu Một Dãy 25x52x15 mm 2 Nắp Chắn Cao Su 6205-2RS | *(của bạn)* | Vòng Bi Cầu Rãnh Sâu | — | — | (bảng ISO) | OK |
| 41117 | Cờ Lê Vòng Miệng 17 mm Sata 41117 | *(của bạn)* | Cờ Lê Vòng Miệng | — | 17 | sata.vn; … | OK |

- `category_id` để trống cho tới khi bạn cấu hình `category_ids.local.json` (map *Loại → id ERP*). `Loại` luôn có.
- `status = OK` chỉ khi **≥2 nguồn khớp**; thiếu/không chắc → `REVIEW` để bạn xem lại.
- Cột `TS_*` = thông số kĩ thuật; cột không áp dụng (vd vòng bi không có hệ dẫn động) để trống.

## Cấu trúc

```
.claude-plugin/marketplace.json + plugin.json   # cài qua /plugin
.claude/skills/
├── naming/            scripts/detect_domain.py              # router nhận domain
├── naming-bearings/   scripts/ (engine, bảng kích thước, category_map) + references/
└── naming-handtools/  scripts/ (engine, extract_codes, build_sheet, category_map) + references/
INSTALLATION.md · README.md · requirements.txt · LICENSE
```

Mỗi skill: `SKILL.md` = quy trình agent làm theo; `references/` = quy ước đặt tên, bản đồ category,
schema thông số, workflow; `scripts/` = helper deterministic (Python). `category_ids.local.json`
(gitignored) = map *Loại → id ERP của bạn*.

## Ghi chú

- Tên/đầu ra bằng tiếng Việt (theo văn phong catalog).
- Cần Claude Code (skills + Agent tool) để chạy phần research đa nguồn.

## Giấy phép

MIT — xem [LICENSE](LICENSE).
