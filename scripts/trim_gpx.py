# 公開前裁掉起點與終點附近的軌跡（保護住家／公司位置）
# 用法：python3 scripts/trim_gpx.py 原檔.gpx rides/新檔.gpx 300   （300 = 裁掉頭尾各 300 公尺）
import math, sys, xml.etree.ElementTree as ET
src, dst = sys.argv[1], sys.argv[2]
n = float(sys.argv[3]) if len(sys.argv) > 3 else 300
tree = ET.parse(src); root = tree.getroot()
uri = root.tag[1:].split('}')[0] if root.tag.startswith('{') else ''
if uri: ET.register_namespace('', uri)
ET.register_namespace('gpxtpx', 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1')
ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
tag = lambda e: e.tag.rsplit('}', 1)[-1]
pts = [(s, p) for s in root.iter() if tag(s) == 'trkseg' for p in list(s) if tag(p) == 'trkpt']
def hv(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 12742000*math.asin(math.sqrt(h))
ll = [(float(p.get('lat')), float(p.get('lon'))) for _, p in pts]
d = [0.0]
for i in range(1, len(ll)): d.append(d[-1] + hv(ll[i-1], ll[i]))
if d[-1] < 3*n: sys.exit('軌跡太短，無法裁切')
for (s, p), x in zip(pts, d):
    if x < n or x > d[-1] - n: s.remove(p)
tree.write(dst, encoding='utf-8', xml_declaration=True)
print('裁切完成：', len(pts), '→', len([1 for x in d if n <= x <= d[-1]-n]), '點')
