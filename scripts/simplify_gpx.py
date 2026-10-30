# 縮小 GPX 檔（GitHub Pages 不會 gzip .gpx，網頁也最多只用 700 個重取樣點）
#  - 移除每點的 <extensions>（速度、溫度…網頁沒用到）
#  - 座標取 6 位小數（約 0.1 m）、海拔取 1 位
#  - 用 Douglas-Peucker（含海拔，容差 EPS 公尺）去掉直線上的多餘點，
#    但每隔 MAXGAP 公尺至少保留一點，讓速度／時間資料仍然足夠細
# 用法：python3 scripts/simplify_gpx.py rides/*.gpx                 （原地覆寫，請先 commit 原檔）
#       python3 scripts/simplify_gpx.py --eps 1 --gap 25 in.gpx
import math, sys, xml.etree.ElementTree as ET
args = sys.argv[1:]; EPS, MAXGAP = 1.0, 25.0
while args[:1] in (['--eps'], ['--gap']):
    if args[0] == '--eps': EPS = float(args[1])
    else: MAXGAP = float(args[1])
    args = args[2:]
tag = lambda e: e.tag.rsplit('}', 1)[-1]
def child(p, name):
    for c in p:
        if tag(c) == name: return c
def keep_idx(X):
    n = len(X); keep = [False]*n; keep[0] = keep[-1] = True; st = [(0, n-1)]
    while st:
        a, b = st.pop(); A, B = X[a], X[b]; d = [B[k]-A[k] for k in range(3)]; L2 = sum(v*v for v in d) or 1e-12
        best, bi = -1.0, -1
        for i in range(a+1, b):
            P = X[i]; t = max(0, min(1, sum((P[k]-A[k])*d[k] for k in range(3))/L2))
            e = math.sqrt(sum((P[k]-A[k]-t*d[k])**2 for k in range(3)))
            if e > best: best, bi = e, i
        if best > EPS: keep[bi] = True; st += [(a, bi), (bi, b)]
    last = 0; acc = 0.0
    for i in range(1, n):
        acc += math.dist(X[i-1][:2], X[i][:2])
        if keep[i]: last, acc = i, 0.0
        elif acc >= MAXGAP: keep[i] = True; last, acc = i, 0.0
    return keep
for f in args:
    tree = ET.parse(f); root = tree.getroot()
    uri = root.tag[1:].split('}')[0] if root.tag.startswith('{') else ''
    if uri: ET.register_namespace('', uri)
    before = after = 0
    for seg in [s for s in root.iter() if tag(s) in ('trkseg', 'rte')]:
        pts = [p for p in list(seg) if tag(p) in ('trkpt', 'rtept')]
        if len(pts) < 3: continue
        la0 = float(pts[0].get('lat')); kx = 111320*math.cos(math.radians(la0))
        X = []
        for p in pts:
            e = child(p, 'ele')
            try: z = float(e.text)
            except (AttributeError, TypeError, ValueError): z = 0.0
            X.append(((float(p.get('lon'))-float(pts[0].get('lon')))*kx, (float(p.get('lat'))-la0)*110540, z))
        keep = keep_idx(X); before += len(pts)
        for p, k in zip(pts, keep):
            if not k: seg.remove(p); continue
            after += 1
            p.set('lat', f"{float(p.get('lat')):.6f}"); p.set('lon', f"{float(p.get('lon')):.6f}")
            for c in list(p):
                if tag(c) == 'extensions': p.remove(c)
                elif tag(c) == 'ele' and c.text:
                    try: c.text = f'{float(c.text):.1f}'
                    except ValueError: pass
    for e in root.iter():
        if len(e): e.text = '\n'
        e.tail = '\n'
    tree.write(f, encoding='utf-8', xml_declaration=True)
    print(f, before, '→', after, 'points')
