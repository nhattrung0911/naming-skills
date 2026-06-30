# 🏷️ naming-skills

> Danh sách **mã hãng** → **tên chuẩn + thông số kĩ thuật + category**.
> Chạy với **Claude Code · Codex · Gemini**. Nhanh · rẻ · không bịa · không lộ data.

```mermaid
flowchart LR
    A([📄 File mã hãng]) --> B{detect domain}
    B -->|vòng bi| C[⚙️ engine: loại/tên<br/>+ d×D×B NHÁP]
    B -->|dụng cụ| D[⚙️ engine: loại/tên]
    C --> R[🔎 search + đối chiếu<br/>≥N nguồn · có URL]
    D --> R
    CACHE[(💾 cache.json)] -. bỏ mã đã tra .-> R
    R --> E([✅ Sheet chuẩn<br/>Tên · Loại · TS_* · Nguồn · status])
```

---

## ⚡ Dùng nhanh

```mermaid
flowchart LR
    P[git clone / plugin install] --> Q[pip install -r requirements.txt] --> R["/naming @file.xlsx"] --> S([sheet chuẩn])
```

**Claude Code**
```
/plugin marketplace add nhattrung0911/naming-skills
/plugin install naming-skills@naming-skills
/naming @file.xlsx
```
**Codex / Gemini** → xem [AGENTS.md](AGENTS.md) (3 bước, cùng schema).
Chi tiết cài + gắn `category_id`: [INSTALLATION.md](INSTALLATION.md).

---

## 📥 Vào → 📤 Ra

| Mã hãng | → | Tên chuẩn | Loại | TS_* | Nguồn | status |
|---|---|---|---|---|---|---|
| `6205-2RS` | → | Vòng Bi Cầu Rãnh Sâu 25x52x15 mm 2 Nắp Chắn Cao Su 6205-2RS | Vòng Bi Cầu Rãnh Sâu | … | ISO | OK |
| `423024M` | → | Đầu Tuýp 24 mm 1/2 Inch Kingtony 423024M | Đầu Tuýp Lẻ | 1/2" · 24mm | kingtony; sata | OK |
| `41117` | → | Cờ Lê Vòng Miệng 17 mm Sata 41117 | Cờ Lê Vòng Miệng | 17 mm | sata.vn | OK |

`status = OK` ⇔ **≥2 nguồn khớp**. Thiếu/khó → `REVIEW`.

---

## 🚀 Nhanh & rẻ (đã tích hợp)

| | |
|---|---|
| 💾 **Cache** | lần sau chỉ tra mã mới → list lớn rất rẻ |
| 🏷️ **Đánh dấu trùng** | mã trùng **giữ đủ dòng** (cờ `Trùng`), chỉ research **1 lần/mã** |
| ⚙️ **Deterministic-first** | **loại/tên/category** ra free; **số liệu** (cả d×D×B) thì search |
| 🎚️ **Số nguồn tùy chỉnh** | `--min-sources N` (mặc định **2**) — client prompt thêm được |
| ⛓️ **Batch + early-stop** | gộp mã theo lô, dừng ở đủ N nguồn |

## 🔒 An toàn & chính xác
- Repo **0 id nội bộ**: `category_id` trống tới khi gắn `category_ids.local.json` (gitignored).
- Số liệu = **search + đối chiếu ≥N nguồn, có URL**. KHÔNG bịa, KHÔNG suy từ format mã.
- Vòng bi: bảng ISO chỉ là **số nháp đối chiếu** — d×D×B cuối vẫn lấy từ nguồn.

## 🧩 Gồm 3 skill
`/naming` (router) · `/naming-bearings` (vòng bi) · `/naming-handtools` (dụng cụ cầm tay).

## 📂 Cấu trúc
```
.claude-plugin/   marketplace.json · plugin.json
.claude/skills/   naming · naming-bearings · naming-handtools
AGENTS.md · GEMINI.md · INSTALLATION.md · requirements.txt
```

## 📋 Yêu cầu
Claude Code / Codex / Gemini (cho bước research) · Python 3 + `pandas` `openpyxl`.

## 📜 License
[MIT](LICENSE)
