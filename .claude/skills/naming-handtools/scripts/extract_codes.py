# -*- coding: utf-8 -*-
"""
Đọc file Excel/CSV chứa cột MÃ HÃNG -> in JSON list để agent chia việc.
Tự dò cột mã (Mã hãng / ma_hang / code / part_number...) + cột brand/description nếu có.

Tối ưu chi phí: ĐÁNH DẤU mã trùng (KHÔNG gộp — giữ đủ dòng) + --cache (bỏ mã đã tra trước).
-> agent CHỈ research mã `need_research=true` (lần đầu xuất hiện, chưa cache). Mã trùng/đã cache
   dùng lại kết quả, KHÔNG search lại — nhưng vẫn còn nguyên dòng trong output.

Dùng:
    python extract_codes.py input.xlsx [--sheet 0] [--code-col "Mã hãng"] [--cache cache.json]
-> stdout: {"code_col":..., "n":.., "n_todo":.., "n_cached":..,
            "rows":[{"i":0,"code":"...","brand":..,"desc":..,"need_research":true|false}]}
"""
import argparse, json, sys, io
from pathlib import Path
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

CODE_HINTS = ["mã hãng", "ma hang", "mã hang", "mahang", "code", "part number",
              "part_number", "part#", "mpn", "mã", "ma"]
BRAND_HINTS = ["brand", "hãng", "hang", "nhãn", "thương hiệu"]
DESC_HINTS = ["description", "mô tả", "mo ta", "tên", "ten", "name"]


def pick(cols, hints):
    low = {str(c).strip().lower(): c for c in cols}
    for h in hints:
        for lc, orig in low.items():
            if lc == h:
                return orig
    for h in hints:
        for lc, orig in low.items():
            if h in lc:
                return orig
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("--sheet", default=0)
    ap.add_argument("--code-col", default=None)
    ap.add_argument("--cache", default=None, help="cache.json đã tra trước -> bỏ qua mã đã có")
    a = ap.parse_args()
    cache = {}
    if a.cache and Path(a.cache).exists():
        cache = json.loads(Path(a.cache).read_text(encoding="utf-8"))
    p = Path(a.inp)
    sheet = a.sheet
    try:
        sheet = int(sheet)
    except (ValueError, TypeError):
        pass
    if p.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(p, sheet_name=sheet)
    else:
        df = pd.read_csv(p)

    code_col = a.code_col or pick(df.columns, CODE_HINTS)
    if not code_col:
        print(json.dumps({"error": "Không tìm thấy cột mã hãng", "columns": list(map(str, df.columns))},
                         ensure_ascii=False))
        sys.exit(1)
    brand_col = pick([c for c in df.columns if c != code_col], BRAND_HINTS)
    desc_col = pick([c for c in df.columns if c != code_col], DESC_HINTS)

    rows, seen = [], set()
    for i, r in df.iterrows():
        code = r.get(code_col)
        if pd.isna(code) or str(code).strip() == "":
            continue
        code = str(code).strip()
        is_dup = code in seen                      # ĐÁNH DẤU trùng, KHÔNG bỏ dòng
        seen.add(code)
        rows.append({
            "i": int(i),
            "code": code,
            "brand": (str(r.get(brand_col)).strip() if brand_col and not pd.isna(r.get(brand_col)) else None),
            "desc": (str(r.get(desc_col)).strip() if desc_col and not pd.isna(r.get(desc_col)) else None),
            "dup": is_dup,                          # True = mã trùng (dòng lặp)
            # research 1 lần/mã: chỉ lần đầu xuất hiện + chưa cache
            "need_research": (not is_dup) and (code not in cache),
        })
    todo = sum(1 for r in rows if r["need_research"])
    print(json.dumps({"code_col": str(code_col), "brand_col": str(brand_col) if brand_col else None,
                      "desc_col": str(desc_col) if desc_col else None, "sheet": sheet,
                      "n": len(rows), "n_unique": len(seen), "n_todo": todo,
                      "n_dup": sum(1 for r in rows if r["dup"]),
                      "rows": rows}, ensure_ascii=False))


if __name__ == "__main__":
    main()
