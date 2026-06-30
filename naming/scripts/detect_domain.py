# -*- coding: utf-8 -*-
"""
Phân loại mỗi dòng (theo mã hãng + desc/brand nếu có) -> domain:
  "bearing" | "handtool" | "unknown"
để /naming route sang sub-skill đúng (naming-bearings / naming-handtools).

Ưu tiên tín hiệu: DESC keyword > BRAND > CODE pattern.

Dùng:
    python detect_domain.py input.xlsx [--sheet 0] [--code-col "Mã hãng"]
-> stdout JSON {code_col, n, counts, rows:[{i,code,domain,why}]}
"""
import argparse, json, re, sys, io
from pathlib import Path
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

CODE_HINTS = ["mã hãng", "ma hang", "mã hang", "code", "part number", "part_number", "part#", "mpn", "mã"]
BRAND_HINTS = ["brand", "hãng", "hang", "nhãn", "thương hiệu"]
DESC_HINTS = ["description", "mô tả", "mo ta", "tên", "ten", "name"]

DESC_BEARING = re.compile(r"vòng bi|bạc đạn|gối đỡ|bearing|mắt trâu|tang trống|đũa côn|cầu rãnh", re.I)
DESC_HANDTOOL = re.compile(
    r"cờ lê|mỏ lết|\bkìm\b|tua vít|tuốc nơ|đầu tuýp|lục giác|\bcảo\b|cần siết|cần nổ|"
    r"\bbúa\b|\bđục\b|thước|kéo cắt|dao rọc|mũi vít|mỏ hàn|bút thử|tay vặn", re.I)

BRAND_BEARING = re.compile(r"\b(SKF|FAG|INA|NSK|NTN|KOYO|JTEKT|NACHI|TIMKEN|C&U|CUB|ASAHI|IKO|ZWZ|HCH|TR|DYZV|PBC|KYS)\b", re.I)
BRAND_HANDTOOL = re.compile(r"\b(SATA|STANLEY|BOSCH|ANEX|TSUNODA|MILWAUKEE|MITUTOYO|KINGTONY|KING TONY|INSIZE|MAKITA|TOTAL|YATO|ENDURA|CROSSMAN|TOP|FULCO|NBK)\b", re.I)

CODE_BEARING = [
    r"^6\d{2,3}([\-/].*)?$", r"^6[0-4]/\d", r"^(60|62|63|64|68|69|16)\d{2}",
    r"^(N|NU|NJ|NUP|NF|NN|NNU|RNU)\d", r"^(70|72|73|B7)\d{2}",
    r"^(12|13|22|23|24)\d{2}", r"^(302|303|313|320|322|323|329|330|331|332)\d",
    r"^3\d{4}$", r"^(UC|UK)[PFLT]?\d?", r"^(SNL?|SN)\d", r"^(HK|BK|NA|RNA|NK|NKI|TAF|AXK)\d",
    r"^(GE|SA|SI|POS|CF|KR|NUKR|CSK|HF)\d", r"^S?S?6\d{2,3}",
]
CODE_BEARING = [re.compile(p, re.I) for p in CODE_BEARING]


def pick(cols, hints):
    low = {str(c).strip().lower(): c for c in cols}
    for h in hints:
        if h in low:
            return low[h]
    for h in hints:
        for lc, orig in low.items():
            if h in lc:
                return orig
    return None


def classify(code, brand, desc):
    code = str(code or "").strip()
    desc = str(desc or "")
    brand = str(brand or "")
    if desc:
        if DESC_BEARING.search(desc):
            return "bearing", "desc:bearing-kw"
        if DESC_HANDTOOL.search(desc):
            return "handtool", "desc:handtool-kw"
    if BRAND_BEARING.search(brand) or BRAND_BEARING.search(desc):
        return "bearing", "brand:bearing"
    if BRAND_HANDTOOL.search(brand) or BRAND_HANDTOOL.search(desc):
        return "handtool", "brand:handtool"
    for rx in CODE_BEARING:
        if rx.match(code):
            return "bearing", f"code:{rx.pattern[:18]}"
    return "unknown", "no-signal"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("--sheet", default=0)
    ap.add_argument("--code-col", default=None)
    a = ap.parse_args()
    p = Path(a.inp)
    sheet = a.sheet
    try:
        sheet = int(sheet)
    except (ValueError, TypeError):
        pass
    df = pd.read_excel(p, sheet_name=sheet) if p.suffix.lower() in (".xlsx", ".xls") else pd.read_csv(p)

    code_col = a.code_col or pick(df.columns, CODE_HINTS)
    if not code_col:
        print(json.dumps({"error": "Không thấy cột mã", "columns": list(map(str, df.columns))}, ensure_ascii=False))
        sys.exit(1)
    brand_col = pick([c for c in df.columns if c != code_col], BRAND_HINTS)
    desc_col = pick([c for c in df.columns if c != code_col], DESC_HINTS)

    rows, counts = [], {"bearing": 0, "handtool": 0, "unknown": 0}
    for i, r in df.iterrows():
        code = r.get(code_col)
        if pd.isna(code) or str(code).strip() == "":
            continue
        dom, why = classify(code, r.get(brand_col) if brand_col else None,
                            r.get(desc_col) if desc_col else None)
        counts[dom] += 1
        rows.append({"i": int(i), "code": str(code).strip(), "domain": dom, "why": why})
    print(json.dumps({"code_col": str(code_col), "brand_col": str(brand_col) if brand_col else None,
                      "desc_col": str(desc_col) if desc_col else None, "sheet": sheet,
                      "n": len(rows), "counts": counts, "rows": rows}, ensure_ascii=False))


if __name__ == "__main__":
    main()
