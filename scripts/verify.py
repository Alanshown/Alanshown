from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
g=Image.open(R/'assets/banner.gif')
assert g.size==(1200,400) and g.n_frames==96
assert g.info['loop']==0
assert (R/'assets/banner.gif').stat().st_size<10_000_000
for p in (R/'assets').rglob('*.svg'): ET.parse(p)
assert Image.open(R/'assets/source/avatar.png').size[0]>100
print('PASS: GIF dimensions, frame count, loop, size, SVG XML, avatar source')
