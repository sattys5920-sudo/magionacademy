# 새 NPC 셋을 NPC 그림(art/npcs.png · webp)에 붙여요: 15 번째 줄(spr 14) 도도 · 16 번째(spr 15) 셀린 · 17 번째(spr 16) 본
#   도도 tools/iso/out/dodo_npc.png (tools/iso/lpc/dodo_npc.py) · 셀린 · 본 tools/iso/out/newnpc_lpc.png 0 · 2 번째 줄 (tools/iso/lpc/newnpc_lpc.py)
#   npcs.png를 다시 만들면 (npc_art.py → o2mo_build.py) 그 뒤에 이 파일을 한 번 더 돌려요
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..'); ART = os.path.join(ROOT, 'public', 'art'); OUT = os.path.join(ROOT, 'tools', 'iso', 'out')
npcs = Image.open(os.path.join(ART, 'npcs.png')).convert('RGBA')
dodo = Image.open(os.path.join(OUT, 'dodo_npc.png')).convert('RGBA'); lpc = Image.open(os.path.join(OUT, 'newnpc_lpc.png')).convert('RGBA')
rows = [dodo.crop((0, 0, 1280, 64)), lpc.crop((0, 0, 1280, 64)), lpc.crop((0, 128, 1280, 192))]   # 14 도도 · 15 셀린 · 16 본
big = Image.new('RGBA', (1280, (14 + len(rows)) * 64)); big.alpha_composite(npcs.crop((0, 0, 1280, 14 * 64)), (0, 0))
for i, r in enumerate(rows): big.alpha_composite(r, (0, (14 + i) * 64))
big.save(os.path.join(ART, 'npcs.png')); big.save(os.path.join(ART, 'npcs.webp'), lossless=True, method=6, quality=100)
print('ok', big.size)
