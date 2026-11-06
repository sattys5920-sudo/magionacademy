# 시계탑에 기대는 긴 사다리 (원본 8 줄 주기 가로대를 늘려 씀)
from PIL import Image
src = Image.open('out/clock_ladder.png').convert('RGBA')
H = 112
out = Image.new('RGBA', (20, H))
out.paste(src.crop((0, 0, 20, 10)), (0, 0))
y = 10
while y < H - 6:
    out.paste(src.crop((0, 10, 20, 18)), (0, y)); y += 8
out.paste(src.crop((0, 58, 20, 64)), (0, H - 6))
out.save('out/clock_ladder_long.png')
