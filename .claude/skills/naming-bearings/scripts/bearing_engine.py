# -*- coding: utf-8 -*-
"""
Bearing naming/standardizer engine.
Given a part code (+optional brand), resolve: bearing TYPE,  category id,
boundary dimensions d/D/B (mm; inch shown as fractions), seal phrase, and a
standardized SEO name in  house style.

Deterministic for standard ISO/metric designations and a curated web set.
For codes it cannot resolve, status='NEEDS_WEB' -> the agent must web-search the
dimensions, then call standardize(..., dims=(d,D,B)).

Self-contained: only depends on dimension_tables.py + category_map.json (same dir).
"""
import re, json, os
import dimension_tables as R

HERE = os.path.dirname(os.path.abspath(__file__))
CATMAP = json.load(open(os.path.join(HERE, 'category_map.json'), encoding='utf-8'))['type_to_category']
# category_id = taxonomy RIÊNG của bạn. File committed để null. Đặt id thật vào
# category_ids.local.json (đã gitignore, KHÔNG push) -> nạp đè ở đây.
_LOCAL = os.path.join(HERE, 'category_ids.local.json')
if os.path.exists(_LOCAL):
    CATMAP.update({k: v for k, v in json.load(open(_LOCAL, encoding='utf-8')).items()
                   if not k.startswith('_')})

# =================== parsing ===================
def strip_suffix(s):
    for suf in ['2RSTUBE','2RSB','2RS','RSTUBE','RSB','RS','ZZB','ZZTUBE','ZZ','TUBE',
                '4NREM','4NR','NREM','EM','E','MBW33C3','MBW33','KMBW33C3','KMBW33','CAW33C3','CAW33','W33',
                'MB','M','C3','C4','NR','N','K','D','B','-4','DDU','DD','LLU','LU','DU','2Z','Z']:
        if s.endswith(suf): s = s[:-len(suf)]
    return s

def core_digits(ma):
    m = re.match(r'^([A-Za-z]*)(\d.*)$', ma.strip())
    if not m: return None, None
    pre = m.group(1).upper()
    rest = strip_suffix(m.group(2))
    mm = re.match(r'^(\d+)', rest)
    return (pre, mm.group(1) if mm else None)

def lookup_ball(core):
    if len(core) < 4: return None
    s2, bc = core[:2], core[-2:]
    tabs = {'60':R.T60,'62':R.T62,'63':R.T63,'64':R.T64,'68':R.T68,'69':R.T69,'16':R.T16,
            '12':R.S12,'13':R.S13,'22':R.S22,'23':R.S23,'52':R.A52,'53':R.A53}
    if s2 in tabs and bc in tabs[s2]:
        D,B = tabs[s2][bc]; return (D,B,'ball:'+s2)
    return None

def lookup_angular(core):
    """Single-row angular contact 70/72/73 (+B7 Misumi): same boundary as 60/62/63."""
    if len(core) < 4: return None
    s2, bc = core[:2], core[-2:]
    tabs = {'70':R.T60,'72':R.T62,'73':R.T63}
    if s2 in tabs and bc in tabs[s2]:
        D,B = tabs[s2][bc]; return (D,B,'ang:'+s2)
    return None

def lookup_5(core):
    if len(core) != 5: return None
    s3, bc = core[:3], core[-2:]
    s13e = dict(R.S13); s13e.update(R.S13_EXT)
    tabs = {'511':R.TH511,'512':R.TH512,'513':R.TH513,'514':R.TH514,'618':R.T68,'619':R.T69,
            '302':R.TR302,'303':R.TR303,'313':R.TR313,'320':R.TR320,'322':R.TR322,'323':R.TR323,
            '330':R.TR330,'331':R.TR331,'332':R.TR332,'329':R.TR329,'163':R.T63,
            '222':R.SR222,'223':R.SR223,'213':s13e,'293':R.ST293,'294':R.ST294,
            '230':R.SR230,'231':R.SR231,'232':R.SR232,'240':R.SR240,'241':R.SR240}
    if s3 in tabs and bc in tabs[s3]:
        D,B = tabs[s3][bc]; return (D,B,'5:'+s3)
    return None

def lookup_cyl(pre, core):
    if pre not in ('N','NU','NJ','NUP','NF'): return None
    if len(core) == 3:
        s, bc = core[0], core[1:]
        tabs = {'2':R.T62,'3':R.T63,'4':R.T64}
        if s in tabs and bc in tabs[s]:
            D,B = tabs[s][bc]; return (D,B,'cyl3:'+s)
    elif len(core) == 4:
        s2, bc = core[:2], core[2:]
        tabs = {'10':R.T60,'22':R.S22,'23':R.S23}
        if s2 in tabs and bc in tabs[s2]:
            D,B = tabs[s2][bc]; return (D,B,'cyl4:'+s2)
    return None

def lookup_pillow(ma):
    m = re.match(r'^(UC[A-Z]*|UK[A-Z]*)(\d+)$', ma)
    if not m: return None
    body = m.group(2)
    if len(body) == 3:
        s, bc = body[0], body[1:]
        tab = {'2':R.UC2,'3':R.UC3}.get(s)
        if tab and bc in tab:
            D,B = tab[bc]; return (D,B,'pillow:'+s)
    return None

def lookup_special(ma):
    s = strip_suffix(ma).rstrip('-_ ')
    if s in R.SPECIAL:
        d,D,B = R.SPECIAL[s]; return (D,B,'special',d)
    return None

def lookup_axk(ma):
    m = re.match(r'^AXK(\d+)$', ma)
    if m and m.group(1) in R.AXK:
        d,D,B = R.AXK[m.group(1)]; return (D,B,'axk',d)
    return None

def lookup_web(ma):
    if ma in R.WEB:
        d,D,B = R.WEB[ma]; return (D,B,'web',d)
    return None

def resolve(ma):
    """Return (D, B, src[, d]) or None. None => not a standard code -> web-search needed."""
    ma = str(ma).strip()
    if re.match(r'^H\d', ma): return None          # adapter sleeve, not a bearing
    for fn in (lookup_web, lookup_special, lookup_axk, lookup_pillow):
        r = fn(ma)
        if r: return r
    pre, core = core_digits(ma)
    if core is None: return None
    if pre in ('N','NU','NJ','NUP','NF'):          # cylindrical prefix -> cylindrical only
        return lookup_cyl(pre, core)
    r = lookup_5(core) or lookup_angular(core) or lookup_ball(core)
    if r is None and pre == '' and core in R.MINI:
        D,B = R.MINI[core]; r = (D,B,'mini')
    return r

# prefix -> type for specialty bearings (dimensions still need web)
PREFIX_TYPE = [
    (r'^(GEG|GEH|GEEM|GE|SAL|SAR|SA|SIL|SI|POS|PHS|GAR|GAL)\d', 'Vòng Bi Mắt Trâu'),
    (r'^(NUKRE|NUKR|KRVE|KRV|KRE|KR|CFH|CFE|CF)\d',             'Vòng Bi Cam'),
    (r'^(CSK|HFL|HF|RCB|RC|TFS|AS|US)\d',                       'Vòng Bi Ly Hợp'),
    (r'^(HK|BK|BHA|BA)\d',                                      'Vòng Bi Kim Vỏ Dập'),
    (r'^(NART|NATR|NATV|RNAO|NAO|RNA|NA|TAF|TR|NKI|NKS|NK|NAS|RNU)\d', 'Vòng Bi Kim'),
]
SEAL_WORDS = {'2rs':'2 Nắp Chắn Cao Su','zz':'2 Nắp Chắn Thép',
              '1rs':'1 Nắp Chắn Cao Su','1z':'1 Nắp Chắn Thép'}
def classify_prefix(code):
    for pat, t in PREFIX_TYPE:
        if re.match(pat, code, flags=re.I): return t
    return None

# =================== type / category ===================
SRC2TYPE = {}
for k in ('ball:60','ball:62','ball:63','ball:64','ball:68','ball:69','ball:16','mini','special','5:163','5:618','5:619'):
    SRC2TYPE[k] = 'Vòng Bi Cầu Rãnh Sâu Một Dãy'
for k in ('ball:12','ball:13','ball:22','ball:23'):
    SRC2TYPE[k] = 'Vòng Bi Cầu Tự Lựa'
for k in ('ball:52','ball:53'):
    SRC2TYPE[k] = 'Vòng Bi Cầu Tiếp Xúc Góc Hai Dãy'
for k in ('5:302','5:303','5:313','5:320','5:322','5:323','5:329','5:330','5:331','5:332'):
    SRC2TYPE[k] = 'Vòng Bi Đũa Côn 1 Dãy'
for k in ('cyl3:2','cyl3:3','cyl3:4','cyl4:10','cyl4:22','cyl4:23'):
    SRC2TYPE[k] = 'Vòng Bi Đũa Trụ 1 Dãy'
for k in ('5:222','5:223','5:213','5:230','5:231','5:232','5:240','5:241'):
    SRC2TYPE[k] = 'Vòng Bi Tang Trống Tự Lựa'
for k in ('5:293','5:294'):
    SRC2TYPE[k] = 'Vòng Bi Tang Trống Chặn Trục'
for k in ('5:511','5:512','5:513','5:514'):
    SRC2TYPE[k] = 'Vòng Bi Cầu Chặn Trục'
SRC2TYPE['axk'] = 'Vòng Bi Kim Chặn'

PILLOW_TYPE = [
    (r'^UCFL|^UCFA', 'Gối Đỡ Vòng Bi Mặt Bích Hình Thoi'),
    (r'^UCFC',       'Gối Đỡ Vòng Bi Mặt Bích Tròn'),
    (r'^UCF|^UKF',   'Gối Đỡ Vòng Bi Mặt Bích Hình Vuông'),
    (r'^UCT',        'Gối Đỡ Vòng Bi Tăng Đưa Băng Tải'),
    (r'^UCHA|^UKHA', 'Gối Đỡ Vòng Bi Treo'),
    (r'^UCP|^UKP|^UCPH|^UCPA', 'Gối Đỡ Vòng Bi'),
    (r'^UC\d|^UK\d', 'Vòng Bi Cầu Cho Gối Đỡ'),
]

def classify_type(ma):
    ma = str(ma).strip()
    if re.match(r'^H\d', ma): return 'Phụ Kiện (Măng Xông)'
    if re.match(r'^(UC[A-Z]*|UK[A-Z]*)\d', ma):   # pillow by prefix (even if dims need web)
        for pat, t in PILLOW_TYPE:
            if re.match(pat, ma): return t
        return 'Gối Đỡ Vòng Bi'
    p = classify_prefix(ma)            # specialty prefix (CSK/GE/HK...) wins over embedded code
    if p: return p
    res = resolve(ma)
    if res is None: return None
    src = res[2]
    if src.startswith('ang'): return 'Vòng Bi Cầu Tiếp Xúc Góc Một Dãy'
    if src.startswith('pillow'):
        for pat, t in PILLOW_TYPE:
            if re.match(pat, ma): return t
        return 'Gối Đỡ Vòng Bi'
    if src == 'web':
        if '/' in ma: return 'Vòng Bi Đũa Côn 1 Dãy'
        if ma == '7909': return 'Vòng Bi Cầu Tiếp Xúc Góc Một Dãy'
        if ma in ('98305','R122RSTUBE'): return 'Vòng Bi Cầu Rãnh Sâu Một Dãy'
        return 'Vòng Bi Đũa Côn 1 Dãy'
    return SRC2TYPE.get(src)

def category_of(bearing_type):
    return CATMAP.get(bearing_type)

# =================== seal / material ===================
def seal_phrase(ma):
    s = ma.upper()
    s = re.sub(r'(TUBE|EM|MBW33C3|MBW33|KMBW33|CAW33|W33|C3|C4|NR)$','',s)
    if '2RS' in s or 'DDU' in s or 'LLU' in s: return '2 Nắp Chắn Cao Su'
    if 'ZZ' in s or '2Z' in s or re.search(r'DD$',s): return '2 Nắp Chắn Thép'
    if re.search(r'(?<!2)RS$',s) or s.endswith('DU') or s.endswith('LU'): return '1 Nắp Chắn Cao Su'
    if re.search(r'(?<!Z)Z$',s) and not s.endswith('ZZ'): return '1 Nắp Chắn Thép'
    return ''   # open / non-ball

# =================== dimensions ===================
def _gcd(a,b):
    while b: a,b = b,a%b
    return a

def fmt(v):
    if v is None: return None
    if abs(v-round(v)) < 1e-6: return str(int(round(v)))
    return ('%g'%v)

def inch_frac(mm, tol=0.06):
    if mm is None: return None
    x = mm/25.4; n = round(x*64)
    if abs(x-n/64)*25.4 > tol: return None
    whole, rem = n//64, n-(n//64)*64
    if rem == 0: return str(whole)
    g = _gcd(rem,64); rem//=g; den = 64//g
    return (f'{whole}-{rem}/{den}' if whole else f'{rem}/{den}')

def inch_dims(d,D,B):
    if None in (d,D,B): return None
    fs = [inch_frac(d), inch_frac(D), inch_frac(B)]
    return fs if all(fs) else None

def bore_of(ma, res):
    """Best bore d: from web/special/axk 4th element, else from bore code."""
    if res and len(res) > 3: return res[3]
    if '/' in str(ma): return None                 # inch cone/cup: d only from WEB, never code*5
    m = re.match(r'^H(2[0-9]|3[0-9])(\d\d)$', str(ma))   # adapter sleeve H23xx/H30xx -> shaft size
    if m:
        ser = '2' if m.group(1).startswith('2') else '3'
        return R.UK_SHAFT.get(ser + m.group(2))
    pre, core = core_digits(ma)
    if not core: return None
    if pre.startswith('UK'):                       # adapter-sleeve mount: shaft bore ≠ code*5
        return R.UK_SHAFT.get(core)                # searched per product; None -> must search
    if pre in ('N','NU','NJ','NUP','NF') or pre.startswith('UC'):
        return R.bore_from_code(core[-2:]) if len(core) >= 3 else None   # cyl/UC set-screw: code*5
    if len(core) >= 4:
        return R.bore_from_code(core[-2:])
    if len(core) == 3 and core in R.MINI:
        return int(core[-1])
    return None

# =================== name ===================
_BRAND_CANON = {'ntn':'NTN','skf':'SKF','fag':'FAG','nsk':'NSK','koyo':'KOYO','koy':'KOYO',
    'nachi':'NACHI','nac':'NACHI','iko':'IKO','ina':'INA','timken':'TIMKEN','misumi':'Misumi',
    'msm':'Misumi','asahi':'Asahi','ash':'Asahi','thk':'THK','fyh':'FYH','nmb':'NMB','ezo':'EZO',
    'tsubaki':'Tsubaki','fsq':'FSQ','kys':'KYS','fbj':'FBJ','dyz':'DYZ','fnd':'FND','yar':'YAR',
    'ksu':'KSU','lk':'LK','zwz':'ZWZ','hch':'HCH','ucc':'UCC','c&u':'C&U','cub':'C&U',
    'dyzv':'DYZV','dyz':'DYZ','nhbb':'NHBB','pbc':'PBC','iwata':'Iwata','nankaiseikojo':'Nankaiseikojo'}
BRANDS = '|'.join(sorted(_BRAND_CANON.keys(), key=len, reverse=True))
def detect_brand(part_number):
    m = re.search(r'(?<![A-Za-z])('+BRANDS+r')(?![A-Za-z])', str(part_number), flags=re.I)
    return _BRAND_CANON.get(m.group(1).lower()) if m else None
def _strip_brand(c, brand=None):
    c = re.sub(r'(?<![A-Za-z])('+BRANDS+r')(?![A-Za-z])','',c,flags=re.I)
    if brand:
        c = re.sub(r'(?<![A-Za-z])'+re.escape(brand)+r'(?![A-Za-z])','',c,flags=re.I)
    return c.strip(' -_')

def clean_code(part_number, brand=None):
    """Normalized code for table lookup: brand + structural prefix + separators removed."""
    c = _strip_brand(str(part_number).strip(), brand)
    c = re.sub(r'^(4T|EC|ET|HR|U)-','',c,flags=re.I)
    c = c.replace(' ','').strip('-_ ')
    if '/' not in c:
        c = c.replace('-','')
    return c

def display_code(part_number, brand=None):
    """Code for the NAME: brand stripped, but suffix/dashes kept as input (6204-2RS, NU-324)."""
    return _strip_brand(str(part_number).strip(), brand).strip()

def is_inch_code(code):
    """True only for genuine inch designations (Timken cone/cup, R-series).
    Loại trừ mã METRIC special-bore 6X/YY (vd 62/22, 63/28) tuy có '/' nhưng là hệ mét."""
    c = str(code)
    if re.match(r'^R\d', c): return True
    if '/' in c and not re.match(r'^6\d/', c): return True   # 62/22, 63/28 -> mét, không inch
    return False

def build_name(btype, brand, code, d, D, B, seal):
    """House form (optimized internal catalog export): {Loại} {Nắp chắn} {dxDxB} mm {Hãng} {Mã}.
    Hệ inch (Timken cone/cup, R-series): house style KHÔNG ghi kích thước trong tên
    (số mm vẫn nằm ở cột d/D/B) -> tránh phân số inch xấu."""
    if is_inch_code(code):
        dimstr = ''                         # inch: bỏ dims khỏi tên (chỉ Loại + Hãng + Mã)
    elif None not in (d,D,B):
        dimstr = f'{fmt(d)}x{fmt(D)}x{fmt(B)} mm'
    elif d is not None:
        dimstr = f'd{fmt(d)} mm'
    else:
        dimstr = ''
    parts = [btype]
    if dimstr: parts.append(dimstr)
    if seal: parts.append(seal)        # nắp chắn: sau đơn vị mm, trước hãng+mã
    if brand: parts.append(brand)
    parts.append(code)
    return ' '.join(p for p in parts if p)

# =================== top-level ===================
def standardize(part_number, brand=None, dims=None):
    """
    Resolve one part. `dims`=(d,D,B) overrides lookup (use after web-search).
    Returns dict: part_number, brand, code, type, category, d,D,B, seal, name, status.
    status: OK | NEEDS_WEB | SLEEVE | UNKNOWN_TYPE
    """
    ma = str(part_number).strip()
    if brand is None: brand = detect_brand(part_number)
    code = clean_code(part_number, brand)          # normalized, for lookup
    code_disp = display_code(part_number, brand)   # keeps suffix, for the name
    btype = classify_type(code if code else ma)
    res = resolve(code if code else ma)
    seal = seal_phrase(ma)

    if dims:
        d, Dd, B = dims
    else:
        d = bore_of(code if code else ma, res)
        Dd = res[0] if res else None
        B = res[1] if res else None
        if d is not None and Dd is not None and d >= Dd:   # bad/garbage d -> recompute from code
            pre, core = core_digits(code if code else ma)
            d = R.bore_from_code(core[-2:]) if (core and len(core) >= 4) else d

    is_pillow = bool(btype) and (btype.startswith('Gối Đỡ') or btype == 'Vòng Bi Cầu Cho Gối Đỡ')
    if re.match(r'^H\d', code) or btype == 'Phụ Kiện (Măng Xông)':
        btype = btype or 'Phụ Kiện (Măng Xông)'
        status = 'SLEEVE' if d is not None else 'NEEDS_WEB'   # măng xông: chỉ cần d (trục)
    elif btype is None:
        status = 'UNKNOWN_TYPE'
    elif is_pillow:
        status = 'OK' if d is not None else 'NEEDS_WEB'        # gối đỡ: D/B không bắt buộc
    elif Dd is None or B is None:
        status = 'NEEDS_WEB'
    else:
        status = 'OK'

    cat = category_of(btype) if btype else None
    name = build_name(btype, brand, code_disp, d, Dd, B, seal) if btype else None
    return {'part_number': ma, 'brand': brand, 'code': code_disp, 'type': btype,
            'category': cat, 'd': d, 'D': Dd, 'B': B, 'seal': seal,
            'name': name, 'status': status}

if __name__ == '__main__':
    import sys
    for pn in (sys.argv[1:] or ['NTN-6204-ZZ','SKF 32216','KOYO NU2204','UCP206 Asahi','387/382','AXK1226','H2307','7909']):
        print(standardize(pn))
