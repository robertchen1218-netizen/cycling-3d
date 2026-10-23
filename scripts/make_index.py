# 掃描 rides/*.gpx，產生 rides/index.json（最新的在最前面）
import glob, json, os, re
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rides')
out = []
for f in glob.glob(os.path.join(base, '*.gpx')):
    t = open(f, encoding='utf-8', errors='ignore').read()
    n = re.search(r'<trk>.*?<name>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</name>', t, re.S)
    d = re.search(r'<trkpt.*?<time>(.*?)</time>', t, re.S)
    stem = os.path.splitext(os.path.basename(f))[0]
    out.append({'name': (n.group(1).strip() if n and n.group(1).strip() else stem),
                'file': os.path.basename(f),
                'date': d.group(1).strip() if d else ''})
out.sort(key=lambda r: r['date'], reverse=True)
with open(os.path.join(base, 'index.json'), 'w', encoding='utf-8') as w:
    json.dump(out, w, ensure_ascii=False, indent=2)
print(len(out), 'rides')
