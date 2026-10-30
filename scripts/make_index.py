# 掃描 rides/*.gpx，產生 rides/index.json（日期新的在最前面；網頁預設載入第一筆）
# 日期來源優先順序：檔名開頭的 YYYYMMDD → 第一個軌跡點的 <time> → <metadata><time>
#   （AllTrails 匯出的路線沒有軌跡點時間，metadata 時間是匯出日而不是騎乘日，所以檔名優先）
# 名稱：沿用 index.json 裡已有的名稱（可手動改成中文），新檔才用 GPX 的 <trk><name> 或檔名
import glob, json, os, re
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rides')
idx = os.path.join(base, 'index.json')
old = {}
if os.path.exists(idx):
    try: old = {r['file']: r for r in json.load(open(idx, encoding='utf-8'))}
    except (ValueError, KeyError, TypeError): old = {}
out = []
for f in glob.glob(os.path.join(base, '*.gpx')):
    fn = os.path.basename(f); stem = os.path.splitext(fn)[0]
    t = open(f, encoding='utf-8', errors='ignore').read()
    m = re.match(r'(20\d{2})(\d{2})(\d{2})', stem)
    if m: date = '-'.join(m.groups())
    else:
        d = re.search(r'<(?:trkpt|rtept)\b.*?<time>(.*?)</time>', t, re.S) or re.search(r'<metadata>.*?<time>(.*?)</time>', t, re.S)
        date = d.group(1).strip()[:10] if d else ''
    n = re.search(r'<trk>.*?<name>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</name>', t, re.S)
    name = old.get(fn, {}).get('name') or (n.group(1).strip() if n and n.group(1).strip() else stem)
    out.append({'name': name, 'file': fn, 'date': date})
out.sort(key=lambda r: (r['date'], r['file']), reverse=True)
with open(idx, 'w', encoding='utf-8') as w:
    json.dump(out, w, ensure_ascii=False, indent=2); w.write('\n')
print(len(out), 'rides')
