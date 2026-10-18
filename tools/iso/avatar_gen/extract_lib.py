# 생성 이미지 → 원래 픽셀로 줄이고, 칸마다 분류된 배열로 저장 (다음 단계에서 조립)
import numpy as np, pickle
from PIL import Image
from down import downsample, cells
from collections import deque

def classify(a):
    """칸 하나를 픽셀 종류로: bg / dark / skin / blush / grey / white / mag / other"""
    r, g, b = [a[..., i].astype(int) for i in range(3)]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
    lum = (r * 3 + g * 6 + b) / 10
    C = np.full(a.shape[:2], 'other', dtype=object)
    C[(lum < 55) & ~((r > 110) & (b > 90) & (g < .5 * np.minimum(r, b)))] = 'dark'
    C[(mx - mn < 28) & (lum >= 55)] = 'grey'
    C[(mx - mn < 28) & (lum > 228)] = 'white'
    skin = (r > 110) & (r > g) & (g >= b) & (r - b > 30) & (r - g <= 80) & (lum >= 75)
    C[skin] = 'skin'
    C[(r > 200) & (r - g >= 70) & (g - b < 20) & (b > 100) & (lum >= 75)] = 'blush'
    C[(r > 110) & (b > 90) & (g < .55 * np.minimum(r, b))] = 'mag'
    C[(g > 150) & (r < 120) & (b < 120)] = 'bg'
    return C, lum

def outside(C):
    """칸 테두리에서 배경을 따라 들어간 바깥 영역"""
    H, W = C.shape; out = np.zeros((H, W), bool); q = deque()
    for y in range(H):
        for x in (0, W - 1):
            if C[y, x] == 'bg': out[y, x] = True; q.append((y, x))
    for x in range(W):
        for y in (0, H - 1):
            if C[y, x] == 'bg' and not out[y, x]: out[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < H and 0 <= xx < W and not out[yy, xx] and C[yy, xx] == 'bg': out[yy, xx] = True; q.append((yy, xx))
    return out

