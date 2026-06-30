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


def build_row(rec, min_sources=2):
    cid, tname = category_of(rec)
    name = normalize_units(rec.get("name_vi") or "")
    specs = rec.get("specs") or {}
    srcs = rec.get("sources") or []
    conf = (rec.get("confidence") or "").lower()
    row = {
        "Mã hãng": rec.get("code"),
        "Tên chuẩn": name,
        "category_id": cid,          # None nếu chưa cấu hình category_ids.local.json
        "Loại": tname,
    }
    for k, col in SPEC_TO_TS.items():
        v = specs.get(k)
        row[col] = "" if v is None else v
    row["Nguồn (URL catalog hãng)"] = "; ".join(srcs)
    # OK = có loại + tên + đủ SỐ NGUỒN (min_sources, client tùy chỉnh) + không low.
    # category_id KHÔNG bắt buộc (tùy taxonomy local).
    if not tname:
        row["status"] = "UNKNOWN_TYPE"
    elif not name:
        row["status"] = "REVIEW"
    elif conf in ("low", "thap", "thấp") or len(srcs) < min_sources:
        row["status"] = "REVIEW_LOW_SOURCE"
    else:
        row["status"] = "OK"
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("--orig", default=None, help="file gốc để giữ Part ID/Part#")
    ap.add_argument("--sheet", default=0)
    ap.add_argument("--code-col", default="Mã hãng")
    ap.add_argument("--cache", default=None, help="cache.json: gộp kết quả cũ + ghi kết quả mới")
    ap.add_argument("--min-sources", type=int, default=2,
                    help="số nguồn tối thiểu để status=OK (client tùy chỉnh, mặc định 2)")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()

    data = json.loads(Path(a.results).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("results") or data.get("rows") or []

    # CACHE: gộp record cũ (mã không có trong research mới) + cập nhật cache bằng research mới
    cache = {}
    if a.cache and Path(a.cache).exists():
        cache = json.loads(Path(a.cache).read_text(encoding="utf-8"))
    new_codes = {str(r.get("code")).strip() for r in data}
    if a.cache:
        for code, rec in cache.items():           # bù các mã đã cache, không research lại
            if code not in new_codes:
                data.append(rec)
        for r in data:                             # cập nhật cache bằng record mới
            c = str(r.get("code") or "").strip()
            if c:
                cache[c] = r
        Path(a.cache).write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

    # 1 record/mã (research). Bảng tra theo mã để điền cho MỌI dòng (kể cả trùng).
    by_code = {}
    for r in data:
        c = str(r.get("code") or "").strip()
        if c and c not in by_code:
            by_code[c] = build_row(r, a.min_sources)
    out = pd.DataFrame(list(by_code.values()))

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
            # GIỮ ĐỦ MỌI DÒNG gốc (kể cả mã trùng) -> merge how=left; đánh dấu cờ Trùng
            odf2["Trùng"] = odf2["Mã hãng"].duplicated(keep="first")
            out["Mã hãng"] = out["Mã hãng"].astype(str).str.strip()
            merged = odf2.merge(out, on="Mã hãng", how="left")
            orig_order = [("Mã hãng" if c == a.code_col else c) for c in odf.columns] + ["Trùng"]
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
