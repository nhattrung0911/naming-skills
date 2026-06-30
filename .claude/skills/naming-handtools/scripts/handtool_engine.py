# -*- coding: utf-8 -*-
"""
Handtool Naming Engine — chuẩn hóa tên dụng cụ cầm tay .

Khác bearing: thông số dụng cụ NẰM SẴN trong description (cỡ, hệ, lực, số chi tiết).
Engine KHÔNG dựng lại tên từ con số — nó GIỮ cụm mô tả gốc, CHỈ:
  1. nhận LOẠI -> category_id  (deterministic, category_map.json)
  2. CHUẨN HÓA đơn vị (8mm->8 mm, 7Inch->7 Inch, 1/2"->1/2 Inch, 60-340Nm->60-340 Nm)
  3. tách HÃNG + MÃ ở đuôi, đặt lại form  {Mô tả} {Hãng} {Mã}
  4. Mã = mã hãng (input) — KHÔNG dùng part# có tiền tố nội bộ (KTN-, DL...).

Web-lookup theo MÃ HÃNG chỉ cần khi description thiếu thông số / cần xác minh.

Dùng:
    python handtool_engine.py "Đầu Tuýp 24 mm 1/2 Inch Kingtony 423024M" 423024M
    from handtool_engine import standardize
    rec = standardize(desc, ma_hang="423024M", brand=None)
"""
import json, re, sys
from pathlib import Path

_MAP = json.loads((Path(__file__).with_name("category_map.json")).read_text(encoding="utf-8"))
RULES = [(re.compile(r["re"], re.I | re.U), r) for r in _MAP["rules"]]
BRANDS = _MAP["brands"]
_BRAND_RE = re.compile(r"\b(" + "|".join(re.escape(b) for b in BRANDS) + r")\b", re.I)

# category_id = taxonomy RIÊNG của bạn (mỗi ERP id khác nhau). File committed KHÔNG chứa id.
# Map "tên loại -> id của bạn" đặt trong category_ids.local.json (đã gitignore, KHÔNG push).
# Thiếu file -> category_id = None, vẫn ra tên loại chuẩn.
_LOCAL = Path(__file__).with_name("category_ids.local.json")
TYPE_TO_ID = {}
if _LOCAL.exists():
    TYPE_TO_ID = {k: v for k, v in json.loads(_LOCAL.read_text(encoding="utf-8")).items()
                  if not k.startswith("_")}


def detect_type(desc):
    """-> (type_name|None, family|None, review:bool)"""
    for rx, r in RULES:
        if rx.search(desc):
            return r["type"], r["family"], bool(r.get("review"))
    return None, None, False


def category_id_of(type_name):
    """id theo taxonomy local (None nếu chưa cấu hình)."""
    return TYPE_TO_ID.get(type_name)


def normalize_units(s):
    s = re.sub(r"\s+", " ", str(s)).strip()
    # drive/length inch: 1/2", 1/2In, 1/2 In, Dr.1/2 -> 1/2 Inch ; 7Inch -> 7 Inch
    s = re.sub(r"\bDr\.?\s*", "", s, flags=re.I)
    s = re.sub(r'(\d(?:[./-]\d+)*)\s*[""″]', r"\1 Inch", s)        # 1/2" -> 1/2 Inch
    s = re.sub(r"(\d)\s*[Ii]n(ch)?\b", r"\1 Inch", s)              # 7In/7Inch -> 7 Inch
    s = re.sub(r"(\d)\s*mm\b", r"\1 mm", s)                         # 8mm -> 8 mm
    s = re.sub(r"(\d)\s*[Nn][Mm]\b", r"\1 Nm", s)                   # 100Nm -> 100 Nm
    s = re.sub(r"(\d)\s*(oz|lbs?|g)\b", lambda m: f"{m.group(1)} {m.group(2).title()}", s, flags=re.I)
    s = re.sub(r"\s*/\s*", "/", s)                                   # 7 Inch / 180 mm -> 7 Inch/180 mm
    s = re.sub(r"\s+", " ", s).strip(" -")
    return s


def split_brand(desc, brand_hint=None):
    """tìm hãng trong chuỗi -> (brand_canon|None, idx_start|None)"""
    if brand_hint:
        for b in BRANDS:
            if b.lower() == str(brand_hint).strip().lower():
                m = re.search(re.escape(b), desc, re.I)
                return b, (m.start() if m else None)
    m = _BRAND_RE.search(desc)
    if m:
        canon = next((b for b in BRANDS if b.lower() == m.group(1).lower()), m.group(1))
        return canon, m.start()
    return None, None


def clean_descriptive(desc, brand, ma):
    """phần mô tả: cắt từ Hãng trở đi + (số lượng) + mã nhúng còn sót."""
    s = str(desc)
    qty = ""
    mq = re.search(r"\(([^)]*(?:Bộ|Cái|Set)[^)]*)\)", s, re.I)
    if mq:
        qty = mq.group(1).strip()
    if brand:
        s = re.split(re.escape(brand), s, flags=re.I)[0]
    s = re.sub(r"\([^)]*\)", "", s)                 # bỏ mọi ngoặc
    if ma:
        s = re.sub(re.escape(str(ma)), "", s, flags=re.I)
    return normalize_units(s), qty


def parse_specs_draft(desc):
    """Thông số GỢI Ý từ mô tả (DRAFT — CHƯA xác minh).
    KHÔNG phải nguồn chân lý: bắt buộc xác minh bằng search mã hãng (xem workflow.md).
    """
    s = normalize_units(desc)
    d = {}
    m = re.search(r"\b(1/4|3/8|1/2|3/4|1)\s*Inch\b", s)
    if m:
        d["he_dan_dong_draft"] = m.group(1) + " Inch"
    m = re.search(r"(\d+(?:\.\d+)?)\s*mm\b", s)
    if m:
        d["co_mm_draft"] = m.group(1)
    m = re.search(r"(\d+(?:[.\-/]\d+)?)\s*Inch\b(?!\s*[FfMm])", s)
    if m:
        d["chieu_dai_draft"] = m.group(1) + " Inch"
    m = re.search(r"(\d+)\s*[-–]\s*(\d+)\s*(Nm|ft-lb|Ft-Lb)", s, re.I)
    if m:
        d["luc_min_draft"], d["luc_max_draft"], d["don_vi_luc_draft"] = m.group(1), m.group(2), m.group(3)
    m = re.search(r"(\d+)\s*(?:Cái|Chi Tiết)\b", s, re.I)
    if m:
        d["so_chi_tiet_draft"] = m.group(1)
    return d


def standardize(desc, ma_hang=None, brand=None):
    desc = str(desc)
    tname, family, review = detect_type(desc)
    cid = category_id_of(tname)
    b, _ = split_brand(desc, brand)
    code = str(ma_hang).strip() if ma_hang not in (None, "", "nan") else None
    if code is None and b:                          # cố lấy mã sau hãng nếu không có mã hãng
        m = re.search(re.escape(b) + r"\s+([\w./\-]+)", desc, re.I)
        code = m.group(1) if m else None
    body, qty = clean_descriptive(desc, b, code)
    parts = [body]
    if b:
        parts.append(b)
    if code:
        parts.append(code)
    name = " ".join(p for p in parts if p)
    if qty:
        name += f" ({qty})"
    # NGUYÊN TẮC CỨNG: thông số PHẢI search từ mã hãng (catalog hãng), có nguồn.
    # Engine chỉ cho LOẠI/CATEGORY/FORM + thông số DRAFT chưa xác minh.
    # -> status mặc định NEEDS_WEB; KHÔNG bao giờ tự set OK.
    if not tname:
        status = "UNKNOWN_TYPE"
    elif review:
        status = "REVIEW_TYPE+NEEDS_WEB"
    else:
        status = "NEEDS_WEB"
    out = {
        "name": re.sub(r"\s+", " ", name).strip(),
        "category_id": cid,
        "type": tname,
        "family": family,
        "brand": b,
        "code": code,
        "nguon": "",          # URL catalog hãng — điền sau khi search
        "status": status,
    }
    out.update(parse_specs_draft(desc))
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Dùng: python handtool_engine.py "<description>" [mã hãng] [hãng]')
        sys.exit(0)
    desc = sys.argv[1]
    ma = sys.argv[2] if len(sys.argv) > 2 else None
    br = sys.argv[3] if len(sys.argv) > 3 else None
    r = standardize(desc, ma, br)
    for k, v in r.items():
        print(f"{k:12}: {v}")
