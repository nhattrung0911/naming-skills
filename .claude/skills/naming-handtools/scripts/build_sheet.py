# -*- coding: utf-8 -*-
"""
Ghép SHEET CHUẨN từ JSON kết quả nghiên cứu (do subagent trả) + file gốc.

JSON nghiên cứu = list các record (schema xem SKILL.md):
{
  "i": 0, "code": "423024M", "brand": "Kingtony", "type": "Đầu Tuýp Lẻ",
  "name_vi": "Đầu Tuýp 24 mm 1/2 Inch Kingtony 423024M",
  "specs": {"drive":"1/2 Inch","size_mm":24,"points":6,"length":null,
            "torque_min":null,"torque_max":null,"torque_unit":null,
            "pieces":null,"material":"CrV","standard":"DIN 3124","features":"6 cạnh"},
  "sources": ["https://...","https://..."], "confidence": "high"
}

Engine gán category_id từ `type`/`name_vi` (deterministic). Thông số -> cột TS_*.

Dùng:
    python build_sheet.py results.json --orig input.xlsx --code-col "Mã hãng" -o out.xlsx
"""
import argparse, json, sys, io
from pathlib import Path
import pandas as pd
from handtool_engine import detect_type, category_id_of, normalize_units

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SPEC_TO_TS = {
    "drive": "TS_Hệ Dẫn Động",
    "size_mm": "TS_Cỡ/Khẩu (mm)",
    "points": "TS_Số Cạnh",
    "length": "TS_Chiều Dài",
    "torque_min": "TS_Lực Min",
    "torque_max": "TS_Lực Max",
    "torque_unit": "TS_Đơn Vị Lực",
    "pieces": "TS_Số Chi Tiết",
    "material": "TS_Vật Liệu/Phủ",
    "standard": "TS_Tiêu Chuẩn",
    "features": "TS_Đặc Điểm Khác",
}
TS_COLS = list(SPEC_TO_TS.values())


def category_of(rec):
    """category_id + Loại từ type (ưu tiên) hoặc name_vi. id theo taxonomy local (None nếu chưa cấu hình)."""
    for key in (rec.get("type"), rec.get("name_vi")):
        if key:
            tname, _, _ = detect_type(str(key))
            if tname:
                return category_id_of(tname), tname
    return None, None


def build_row(rec):
    cid, tname = category_of(rec)
    name = normalize_units(rec.get("name_vi") or "")
    specs = rec.get("specs") or {}
    srcs = rec.get("sources") or []
    conf = (rec.get("confidence") or "").lower()
    row = {
        "Mã hãng": rec.get("code"),
        "Tên chuẩn": name,
        "category_id": cid,
        "Loại": tname,
    }
    for k, col in SPEC_TO_TS.items():
        v = specs.get(k)
        row[col] = "" if v is None else v
    row["Nguồn (URL catalog hãng)"] = "; ".join(srcs)
    # OK chỉ khi >=2 nguồn + confidence cao + có tên + category
    if cid and name and len(srcs) >= 2 and conf in ("high", "cao", ""):
        row["status"] = "OK"
    elif not cid:
        row["status"] = "UNKNOWN_TYPE"
    elif len(srcs) < 2 or conf in ("low", "thap", "thấp"):
        row["status"] = "REVIEW_LOW_SOURCE"
    else:
        row["status"] = "REVIEW"
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("--orig", default=None, help="file gốc để giữ Part ID/Part#")
    ap.add_argument("--sheet", default=0)
    ap.add_argument("--code-col", default="Mã hãng")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()

    data = json.loads(Path(a.results).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("results") or data.get("rows") or []
    out = pd.DataFrame([build_row(r) for r in data])

    if a.orig:
        sheet = a.sheet
        try:
            sheet = int(sheet)
        except (ValueError, TypeError):
            pass
        op = Path(a.orig)
        odf = pd.read_excel(op, sheet_name=sheet) if op.suffix.lower() in (".xlsx", ".xls") else pd.read_csv(op)
        if a.code_col in odf.columns:
            odf2 = odf.rename(columns={a.code_col: "Mã hãng"})
            odf2["Mã hãng"] = odf2["Mã hãng"].astype(str).str.strip()
            out["Mã hãng"] = out["Mã hãng"].astype(str).str.strip()
            merged = odf2.merge(out, on="Mã hãng", how="right")
            # cột gốc (theo thứ tự file) trước, cột chuẩn/ TS_ sau
            orig_order = [("Mã hãng" if c == a.code_col else c) for c in odf.columns]
            new_cols = [c for c in out.columns if c not in orig_order]
            out = merged[orig_order + new_cols]

    out.to_excel(a.out, index=False)
    n = len(out)
    ok = (out["status"] == "OK").sum()
    rev = out["status"].astype(str).str.startswith("REVIEW").sum()
    unk = (out["status"] == "UNKNOWN_TYPE").sum()
    print(f"Tổng {n} | OK {ok} | REVIEW {rev} | UNKNOWN_TYPE {unk}")
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
