# Cài đặt & dùng

Bạn có file Excel/CSV chứa **cột mã hãng**, muốn ra **tên chuẩn + thông số kĩ thuật + category**.
Có 2 cách dùng.

## Yêu cầu
- [Claude Code](https://claude.com/claude-code) (cần Skill + Agent tool để research đa nguồn).
- Python 3 + thư viện cho script helper:
  ```bash
  pip install -r requirements.txt
  ```

## Cách A — Cài qua plugin marketplace (khuyên dùng)

Trong Claude Code:
```
/plugin marketplace add nhattrung0911/naming-skills
/plugin install naming-skills@naming-skills
```
Xong → gõ:
```
/naming @danh_sach_ma.xlsx
```

## Cách B — Clone & dùng ngay (không cài plugin)

```bash
git clone https://github.com/nhattrung0911/naming-skills.git
cd naming-skills
pip install -r requirements.txt
```
Mở thư mục này bằng Claude Code → skill trong `.claude/skills/` tự nhận → gõ `/naming @file.xlsx`.

Hoặc copy 3 thư mục skill vào project của bạn:
```
cp -r .claude/skills/naming .claude/skills/naming-bearings .claude/skills/naming-handtools  <project>/.claude/skills/
```

## (Tuỳ chọn) Gắn category_id theo ERP của bạn

Mặc định output có **tên loại** chuẩn nhưng `category_id` = trống (vì id taxonomy mỗi nơi mỗi khác).
Muốn điền id của bạn:

1. Vào thư mục `scripts/` của skill (`naming-handtools` và/hoặc `naming-bearings`).
2. Copy file ví dụ:
   ```bash
   cp category_ids.example.json category_ids.local.json
   ```
3. Mở `category_ids.local.json`, điền `"Tên loại": <id của bạn>`.

File `category_ids.local.json` đã được **gitignore** → không bị push, không lộ taxonomy của bạn.
Không có file này thì skill vẫn chạy, chỉ là `category_id` để trống.

## Kết quả

File ra: cột gốc + **Tên chuẩn** + **category_id** (nếu có) + **Loại** + cột thông số kĩ thuật `TS_*`
+ **Nguồn (URL)** + **status**. `status = OK` chỉ khi thông số được ≥2 nguồn uy tín xác nhận.

Xem thêm: [README](README.md).
