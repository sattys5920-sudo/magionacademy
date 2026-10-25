"""시작 화면 배경(art/cover.png): 별이 박힌 보라 밤하늘 + 둥둥 유령. 다시 만들려면 python3 tools/iso/cover_bg.py"""
from PIL import Image, ImageDraw
import math, os
W, H = 100, 207
im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
top, bot = (34, 24, 84), (58, 40, 112)
for y in range(H):
    b = min(27, int(y / H * 28)); t = b / 27
    d.line([(0, y), (W, y)], fill=tuple(round(a + (c - a) * t) for a, c in zip(top, bot)))
seed = 5
def rnd():
    global seed; seed = seed * 16807 % 2147483647; return seed / 2147483647
for i in range(34):
    x, y = int(rnd() * W), int(rnd() * 200)
    if 92 < y < 150 and 8 < x < 92: continue   # 제목·안내 글자 자리는 비워 둬요
    c = (216, 204, 255) if i % 5 == 0 else (255, 244, 200)
    d.point((x, y), fill=c)
    if i % 9 == 0:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]: d.point((x + dx, y + dy), fill=c)
def ghost(x, y):
    R = lambda c, a, b, w, h: d.rectangle([x + a, y + b, x + a + w - 1, y + b + h - 1], fill=c)
    R((26, 16, 48), -4, -1, 10, 10); R((244, 240, 255), -3, 0, 8, 8); R((244, 240, 255), -4, 1, 10, 6)
    for a in (-3, 1, 4): R((244, 240, 255), a, 8, 2 if a != 4 else 1, 1)
    R((42, 28, 74), -1, 2, 1, 2); R((42, 28, 74), 3, 2, 1, 2); R((255, 184, 208), -2, 4, 1, 1); R((255, 184, 208), 4, 4, 1, 1)
for x, y in [(20, 38), (82, 62), (16, 164), (60, 180), (86, 144)]: ghost(x, y)
d.rectangle([0, 197, W, H], fill=(42, 28, 82)); d.line([(0, 197), (W, 197)], fill=(58, 42, 106))
out = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'art', 'cover.png'); im.save(out)
