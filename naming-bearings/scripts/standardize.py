# -*- coding: utf-8 -*-
"""
Batch driver: read a CSV/XLSX with a code column (+optional brand), run the engine,
write a standardized CSV and a separate NEEDS_WEB list for codes lacking dimensions.

Usage:
  python standardize.py input.csv --code-col part_number [--brand-col brand] [-o out.csv]
  python standardize.py input.xlsx --code-col part_number --sheet Sheet1

Output columns: part_number, brand, code, type, category, d, D, B, seal, name, status, note
"""
import sys, os, csv, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bearing_engine as E

def read_rows(path, code_col, brand_col, sheet):
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.xlsx', '.xlsm'):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        ws = wb[sheet] if sheet else wb.active
        it = ws.iter_rows(values_only=True)
        hdr = [str(h) if h is not None else '' for h in next(it)]
        ci = hdr.index(code_col); bi = hdr.index(brand_col) if brand_col and brand_col in hdr else None
        for r in it:
            if r is None or ci >= len(r) or r[ci] in (None, ''): continue
            yield str(r[ci]), (str(r[bi]) if bi is not None and bi < len(r) and r[bi] else None)
    else:
        with open(path, encoding='utf-8-sig', newline='') as f:
            rd = csv.DictReader(f)
            for r in rd:
                code = r.get(code_col)
                if not code: continue
                yield str(code), (r.get(brand_col) if brand_col else None)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input')
    ap.add_argument('--code-col', required=True)
    ap.add_argument('--brand-col', default=None)
    ap.add_argument('--sheet', default=None)
    ap.add_argument('-o', '--output', default=None)
    a = ap.parse_args()
    out = a.output or (os.path.splitext(a.input)[0] + '.standardized.csv')
    needs = os.path.splitext(out)[0] + '.NEEDS_WEB.csv'

    cols = ['part_number','brand','code','type','category','d','D','B','seal','name','status','note']
    stat = {}
    nrows = []
    with open(out, 'w', encoding='utf-8-sig', newline='') as fo:
        w = csv.DictWriter(fo, fieldnames=cols); w.writeheader()
        for code, brand in read_rows(a.input, a.code_col, a.brand_col, a.sheet):
            rec = E.standardize(code, brand)
            rec['note'] = '' if rec['status'] == 'OK' else 'CAN_REVIEW' if rec['status'] in ('UNKNOWN_TYPE','SLEEVE') else ''
            w.writerow({k: rec.get(k, '') for k in cols})
            stat[rec['status']] = stat.get(rec['status'], 0) + 1
            if rec['status'] in ('NEEDS_WEB', 'UNKNOWN_TYPE'):
                nrows.append(rec)

    if nrows:
        with open(needs, 'w', encoding='utf-8-sig', newline='') as fn:
            w = csv.DictWriter(fn, fieldnames=['part_number','brand','code','type','status']); w.writeheader()
            for rec in nrows:
                w.writerow({k: rec.get(k,'') for k in ['part_number','brand','code','type','status']})

    print('SAVED', out)
    for k, v in sorted(stat.items()): print(f'  {k}: {v}')
    if nrows: print('WEB-research list ->', needs, f'({len(nrows)} codes)')

if __name__ == '__main__':
    main()
