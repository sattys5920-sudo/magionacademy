# LPC(Universal LPC Spritesheet Character Generator) 파츠 → 게임 캐릭터 부품
# python3 build_lpc.py <LPC 저장소 경로>
#   - 고른 파츠의 walk.png만 받아요 (sparse checkout)
#   - 4방향(아래·위·왼쪽·오른쪽) × 5프레임(서기 + 걷기 4)을 잘라 부품마다 PNG 하나 (public/art/lpc/)
#   - 색은 LPC 팔레트 그대로: 층마다 (칸, 원래 팔레트)를 적어 두면 게임이 고른 팔레트로 바꿔 칠해요
#   - 쓴 파츠 작가·라이선스는 크레딧으로 (../out/lpc_meta.json 의 credits)
import sys, os, json, glob, subprocess, re
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..', '..')
LPC = sys.argv[1]; SHEETS = os.path.join(LPC, 'spritesheets'); DEFS = os.path.join(LPC, 'sheet_definitions')
OUTP = os.path.join(ROOT, 'public', 'art', 'lpc'); OUTM = os.path.join(HERE, '..', 'out', 'lpc_meta.json')
BODIES = ['female', 'male']
BODYKEY = {'female': 'teen', 'male': 'teen'}   # 몸은 둘 다 날씬한 LPC teen 체형, 머리(얼굴)만 여자·남자
ROWS = {'down': 2, 'up': 0, 'left': 1, 'right': 3}; DIRS = ['down', 'up', 'left', 'right']
COLS = [0, 1, 3, 5, 7]                       # 서기 + 걷기 4
FILES = set(l.strip() for l in open(os.path.join(LPC, '..', 'lpc_files.txt')))
PAL = {m: json.load(open(os.path.join(LPC, 'palette_definitions', m, f'{m}_ulpc.json'))) for m in ('body', 'hair', 'eye', 'cloth')}
BASE = {'body': 'light', 'hair': 'orange', 'eye': 'blue', 'cloth': 'white'}
def jd(p): return json.load(open(os.path.join(DEFS, p)))
def defs(pattern): return sorted(glob.glob(os.path.join(DEFS, pattern), recursive=True))
# ---------- 고르기 ----------
def ok(d): return 'walk' in d.get('animations', ['walk'])
SEL = {}
SEL['body'] = [('body/body.json', None)]
SEL['face'] = [(os.path.relpath(f, DEFS), None) for f in defs('head/faces/face_*.json')]
SEL['hair'] = [(os.path.relpath(f, DEFS), None) for f in defs('hair/**/*.json')
               if not os.path.basename(f).startswith('meta') and jd(os.path.relpath(f, DEFS)).get('type_name') == 'hair']
def pick(globs, skip=()):
    out = []
    for g in globs:
        for f in defs(g):
            b = os.path.basename(f)
            if b.startswith('meta') or any(s in b for s in skip): continue
            out.append((os.path.relpath(f, DEFS), None))
    return out
SEL['top'] = pick(['torso/shirts/**/*.json', 'torso/dresses/**/*.json', 'torso/jacket/*.json', 'torso/vest/*.json'], skip=('child', 'santa', 'sleeves'))
SEL['legs'] = pick(['legs/**/*.json'], skip=('armour',))
SEL['feet'] = pick(['feet/shoes/*.json', 'feet/boots/*.json', 'feet/feet_sandals.json', 'feet/feet_slippers.json'])
SEL['hat'] = []   # 모자는 옷 가게 것만 (SHOP['hat'])
SEL_HAT = (
    ['headwear/hats/magic/*.json', 'headwear/hats/formal/*.json', 'headwear/hats/caps/*.json', 'headwear/hats/holiday/*.json', 'headwear/coverings/**/*hood*.json'])
SEL['cape'] = pick(['torso/cape/cape_solid.json', 'torso/cape/cape_tattered.json'])
SEL['neck'] = pick(['headwear/neck/*.json'])
SEL['x'] = pick(['feet/socks/feet_socks_high.json', 'torso/cape/cape_trim.json', 'torso/aprons/torso_aprons_suspenders.json', 'torso/aprons/torso_aprons_overalls.json'])   # 교복 조합에만 써요
SLOT = {'body': 'skin', 'face': 'skin', 'hair': 'hair', 'top': 'top', 'legs': 'legs', 'feet': 'feet', 'hat': 'hat', 'cape': 'top', 'neck': 'top', 'x': 'top'}
HEAD = {'female': 'head/heads/human/female/', 'male': 'head/heads/human/male/'}
DROP = {'face': ('Looking Left', 'Looking Right', 'Closing Eyes'),
        'hat': ('Second Color', 'Belt', 'Buckle', 'feather', 'Feather', 'Trim'),
        'top': ('Trim', 'Sleeves'), 'neck': ('Cape Clip', 'Cape Tie')}
KO = {  # 이름 (게임 화면)
 'Afro': '아프로', 'Cornrows': '콘로', 'Dreadlocks long': '긴 드레드', 'Dreadlocks short': '짧은 드레드', 'Flat top fade': '플랫탑 페이드', 'Flat top straight': '플랫탑',
 'Natural': '내추럴', 'Twists fade': '트위스트 페이드', 'Twists straight': '트위스트', 'Balding': '대머리 직전', 'Buzzcut': '까까머리', 'High and tight': '하이앤타이트',
 'Longhawk': '긴 모히칸', 'Shorthawk': '짧은 모히칸', 'Bob': '단발', 'Bob side part': '옆 가르마 단발', 'Lob': '긴 단발', 'Relm Short': '렐름 숏', 'Bangs bun': '앞머리 똥머리',
 'Braid': '땋은 머리', 'Braid2': '땋은 머리 2', 'Half up': '반묶음', 'High ponytail': '높은 포니테일', 'Long tied': '길게 묶음', 'Ponytail': '포니테일', 'Ponytail2': '포니테일 2',
 'Relm w/Ponytail': '렐름 포니테일', 'Relm XLong': '렐름 아주 긴 머리', 'Shoulderl': '왼쪽 어깨 머리', 'Shoulderr': '오른쪽 어깨 머리', 'Long Topknot': '긴 정수리 묶음',
 'Long Topknot 2': '긴 정수리 묶음 2', 'Short Topknot': '짧은 정수리 묶음', 'Short Topknot 2': '짧은 정수리 묶음 2', 'Large Curls': '큰 웨이브', 'Large Curls XLong': '아주 긴 웨이브',
 'Curly long': '긴 곱슬', 'Curly short': '짧은 곱슬', 'Curly short 2': '짧은 곱슬 2', 'Jewfro': '복슬 곱슬', 'Bangslong': '긴 앞머리', 'Bangslong2': '긴 앞머리 2',
 'Curtains long': '긴 커튼 앞머리', 'Long': '긴 머리', 'Long center part': '가운데 가르마 긴 머리', 'Long messy': '부스스 긴 머리', 'Long messy2': '부스스 긴 머리 2',
 'Long straight': '긴 생머리', 'Loose': '풀어 내린 머리', 'Wavy': '웨이브', 'Bunches': '양갈래 묶음', 'Pigtails': '양갈래', 'Pigtails bangs': '앞머리 양갈래', 'Bangs': '앞머리',
 'Bangsshort': '짧은 앞머리', 'Bedhead': '까치집', 'Cowlick': '삐친 머리', 'Cowlick tall': '높이 삐친 머리', 'Curtains': '커튼 앞머리', 'Idol': '아이돌', 'Messy1': '헝클어진 머리',
 'Messy2': '헝클어진 머리 2', 'Messy3': '헝클어진 머리 3', 'Mop': '바가지 머리', 'Page': '페이지보이', 'Page2': '페이지보이 2', 'Parted': '가르마', 'Parted 2': '가르마 2',
 'Parted 3': '가르마 3', 'Side Parted w/Bangs': '옆 가르마 앞머리', 'Side Parted w/Bangs 2': '옆 가르마 앞머리 2', 'Pixie': '픽시컷', 'Plain': '단정한 머리', 'Single': '한 갈래',
 'Swoop': '쓸어 넘긴 머리', 'Side Swoop': '옆으로 쓸어 넘김', 'Unkempt': '덥수룩', 'Halfmessy': '반쯤 헝클어짐', 'Spiked': '삐죽 머리', 'Spiked2': '삐죽 머리 2',
 'Spiked beehive': '삐죽 벌집 머리', 'Spiked liberty': '리버티 스파이크', 'Spiked liberty2': '리버티 스파이크 2', 'Spiked porcupine': '고슴도치 머리', 'Long band': '머리띠 긴 머리',
 'Princess': '공주 머리', 'Sara': '사라 머리', 'Xlong': '아주 긴 머리', 'XLong Wavy': '아주 긴 웨이브 머리',
 'Angry': '화남', 'Angry Alt': '화남 2', 'Blush': '부끄', 'Closed Eyes': '눈 감음', 'Rolling Eyes': '흥', 'Happy': '웃음', 'Happy Alt': '웃음 2', 'Neutral': '무표정',
 'Sad': '슬픔', 'Sad Alt': '슬픔 2', 'Shame': '민망', 'Shock': '깜짝', 'Tears': '눈물',
 'Longsleeve': '긴팔', 'Longsleeve 2': '긴팔 2', 'Longsleeve 2 Buttoned': '단추 긴팔', 'Cardigan': '카디건', 'Longsleeve Polo': '긴팔 폴로', 'Longsleeve 2 Scoop': '라운드 긴팔',
 'Longsleeve 2 VNeck': '브이넥 긴팔', 'Collared/Formal Longsleeve': '셔츠', 'Striped Collared/Formal Longsleeve': '줄무늬 셔츠', 'Longsleeve laced': '끈 긴팔', 'Scoop': '라운드',
 'Shortsleeve': '반팔', 'Shortsleeve Cardigan': '반팔 카디건', 'Shortsleeve Polo': '반팔 폴로', 'TShirt': '티셔츠', 'TShirt Buttoned': '단추 티셔츠', 'TShirt Scoop': '라운드 티셔츠',
 'TShirt VNeck': '브이넥 티셔츠', 'Sleeveless': '민소매', 'Original Sleeveless': '민소매 2', 'Sleeveless 2': '민소매 3', 'Sleeveless 2 Buttoned': '단추 민소매',
 'Sleeveless 2 Cardigan': '민소매 카디건', 'Sleeveless 2 Polo': '민소매 폴로', 'Sleeveless 2 Scoop': '라운드 민소매', 'Sleeveless 2 VNeck': '브이넥 민소매', 'Sleeveless laced': '끈 민소매',
 'Sleeveless striped': '줄무늬 민소매', 'Tanktop': '나시', 'Blouse': '블라우스', 'Longsleeve blouse': '긴팔 블라우스', 'Corset': '코르셋', 'Robe': '로브', 'Tunic': '튜닉', 'Sara Tunic': '사라 튜닉',
 'Bodice': '보디스 드레스', 'Sash dress': '띠 드레스', 'Slit dress': '트임 드레스', 'Kimono': '기모노', 'Kimono Oversized Sleeves': '큰 소매 기모노', 'Split Kimono': '트임 기모노',
 'Collared coat': '깃 코트', 'Frock coat': '프록코트', 'Iverness cloak': '케이프 코트', 'Tabard': '타바드', 'Trench coat': '트렌치코트', 'Vest': '조끼', 'Vest open': '열린 조끼',
 'Hose': '스타킹', 'Leggings': '레깅스', 'Leggings 2': '레깅스 2', 'Cuffed Pants': '롤업 바지', 'Formal Pants': '정장 바지', 'Striped Formal Pants': '줄무늬 바지', 'Pantaloons': '판탈롱',
 'Pants': '바지', 'Long Pants': '긴 바지', 'Shorts': '반바지', 'Short Shorts': '짧은 반바지', 'Belle skirt': '벨 치마', 'Overskirt': '덧치마', 'Straight skirt': '일자 치마',
 'Legion skirt': '조각 치마', 'Plain skirt': '치마', 'Slit skirt': '트임 치마',
 'Basic Shoes': '구두', 'Ghillies': '끈 구두', 'Revised Shoes': '구두 2', 'Sara Shoes': '사라 구두', 'Basic Boots': '부츠', 'Folded Rim Boots': '접은 부츠', 'Revised Boots': '부츠 2',
 'Rimmed Boots': '테 부츠', 'Sandals': '샌들', 'Slippers': '슬리퍼',
 'Celestial Wizard Hat': '별빛 마법사 모자', 'Celestial Wizard Moon Hat': '달빛 마법사 모자', 'Large Hat': '큰 마녀 모자', 'Wizard Hat Base': '마법사 모자', 'Formal Bowler Hat': '중절모',
 'Crown': '왕관', 'Tiara': '티아라', 'Formal Tophat': '실크햇', 'Bonnie': '보닛', 'Bonnie Alt Tilt': '기울인 보닛', 'Cavalier': '기사 모자', 'Leather Cap': '가죽 모자',
 'Christmas Hat': '산타 모자', 'Elf Trim': '요정 모자', 'Hood': '후드', 'Hijab': '히잡', 'Sack Cloth Hood': '자루 두건',
 'Bowtie': '나비넥타이', 'Bowtie 2': '나비넥타이 2', 'Cravat': '크라바트', 'Jabot': '자보', 'Necklace': '목걸이', 'Large Beaded Necklace': '큰 구슬 목걸이',
 'Small Beaded Necklace': '작은 구슬 목걸이', 'Chain Necklace': '체인 목걸이', 'Simple Necklace': '심플 목걸이', 'Necktie': '넥타이', 'Scarf': '목도리', 'Solid': '망토', 'Tattered': '해진 망토'}
# ---------- 파일 찾기 ----------
PREFER = {'Robe': ['black']}   # 팔레트로 못 바꾸는 부품은 이 색 그림으로
def walk_file(path, d):
    """층 경로 → (파일, 원래 팔레트 [(칸, 재질, 팔레트)])"""
    base = 'spritesheets/' + path
    rec = d.get('recolors')
    if base + 'walk.png' in FILES:
        mat = None
        if isinstance(rec, dict): mat = rec.get('material') or (rec.get('color_1') or {}).get('material')
        if mat is None: mat = {'hair': 'hair'}.get(d.get('type_name'), 'cloth')
        return base + 'walk.png', mat, BASE.get(mat, 'white')
    variants = d.get('variants') or []
    order = PREFER.get(d.get('name'), []) + ['white', 'gray', 'light gray'] + [v for v in variants]
    for v in order:
        f = base + f'walk/{v}.png'
        if f in FILES and v.replace(' ', '') in PAL['cloth'] or (f in FILES and v in PAL['cloth']):
            return f, 'cloth', v
    for v in variants:
        f = base + f'walk/{v}.png'
        if f in FILES: return f, None, v
    return None, None, None
def layers_of(d, body):
    out = []
    for k in sorted([k for k in d if k.startswith('layer_')]):
        L = d[k]; p = L.get(BODYKEY[body]) or L.get('female')   # teen 그림이 없으면 여자 옷 (몸 모양이 거의 같아요)
        if not p: continue
        out.append((L.get('zPos', 50), p))
    return out
# ---------- 모으기 ----------
items = {c: [] for c in SEL}; need = set(); credits = []
for cat, lst in SEL.items():
    for rel, _ in lst:
        d = jd(rel)
        if not ok(d): continue
        if any(w in d.get('name', '') for w in DROP.get(cat, ())): continue
        entry = dict(id=os.path.basename(rel)[:-5], name=d.get('name', ''), L={})
        for body in BODIES:
            Ls = []
            for z, p in layers_of(d, body):
                if '${head}' in p: p = p.replace('${head}', body)
                f, mat, src = walk_file(p, d)
                if not f: continue
                Ls.append((z, f, mat, src, None))
            if Ls: entry['L'][body] = Ls
        if not entry['L']: continue
        items[cat].append(entry); credits += d.get('credits', [])
        for body, Ls in entry['L'].items():
            for z, f, mat, src, _ in Ls: need.add(f)
for body in BODIES:
    f = 'spritesheets/' + HEAD[body] + 'walk.png'; need.add(f)
# ---------- 교복 ----------
# 옷은 교복만: 흰 셔츠·블라우스 + 학교 색(남색) 조끼·카디건·재킷 + 기숙사 색 넥타이·망토 안감
#   (부품 id, 칸, z) 칸 (튜플이면 층마다), 'sch' = 학교 색, 'top' = 기숙사 색, 'sock' = 흰 양말, 'w' = 그대로, None = 부품 원래 칸, z None = 원래 z
SH = 'torso_clothes_longsleeve2_buttoned'   # 흰 셔츠
SOCK = ('feet_socks_high', 'sock', None)
COMBO = {
 'top': [('블레이저', [(SH, 'w', None), ('fx_blazer', 'sch', 36), ('fx_emblem', 'top', 37)]),
         ('셔츠', [(SH, 'w', None)]),
         ('블라우스', [('torso_clothes_blouse_longsleeve', 'w', None)]),
         ('반팔 블라우스', [('torso_clothes_blouse', 'w', None)]),
         ('교복 원피스', [(SH, 'w', None), ('fx_dress', 'sch', None)]),
         ('띠 원피스', [('torso_clothes_blouse', 'w', None), ('fx_dress2', 'sch', None)]),
         ('멜빵 원피스', [('torso_clothes_blouse_longsleeve', 'w', None), ('torso_clothes_corset', 'sch', None)]),
         ('반팔 셔츠', [('torso_clothes_shortsleeve_polo', 'w', None)]),
         ('니트 조끼', [(SH, 'w', None), ('torso_clothes_sleeveless2_vneck', 'sch', 36)]),
         ('카디건', [(SH, 'w', None), ('torso_clothes_longsleeve2_cardigan', 'sch', 36)]),
         ('반팔 카디건', [('torso_clothes_shortsleeve_polo', 'w', None), ('torso_clothes_shortsleeve_cardigan', 'sch', 36)]),
         ('스웨터', [(SH, 'w', None), ('torso_clothes_longsleeve2_vneck', 'sch', 36)]),
         ('마법사 로브', [('torso_clothes_robe', 'w', None)])],
 'feet': [('로퍼 + 무릎 양말', [SOCK, ('feet_shoes_ghillies', None, None)]),
          ('구두 + 무릎 양말', [SOCK, ('feet_shoes_revised', None, None)]),
          ('로퍼', [('feet_shoes_ghillies', None, None)]),
          ('구두', [('feet_shoes_basic', None, None)]),
          ('부츠', [('feet_boots_basic', None, None)]),
          ('접은 부츠', [('feet_boots_fold', None, None)])],
 'legs': [('체크 치마', [('fx_pleat', None, None)]),
          ('일자 치마', [('fx_short', None, None)]),
          ('교복 바지', [('legs_pants', None, None)]),
          ('긴 바지', [('legs_pants2', None, None)]),
          ('반바지', [('legs_shorts', None, None)])],
 'cape': [('교복 망토', [('cape_solid', ('sch', 'top'), None), ('cape_trim', 'top', None)]),
          ('기숙사 색 망토', [('cape_solid', 'top', None)])]}
# ---------- 옷 가게 (사복 'cas'·잠옷 'pj') ----------
# 교복 뒤에 붙여요 (부품 번호가 안 바뀌게). 칸 'cas' = 플레이어가 고른 옷 색 (topC)
TEE = 'torso_clothes_tshirt'
L2 = 'torso_clothes_longsleeve2'
ONESIE = lambda ears, tail: [(L2, 'cas', None), ('legs_pants2', 'cas', 21), ('raw_hood', 'cas', None)] + ears + tail
SHOP = {
 'top': [('후드티', [(L2, 'cas', None), ('fx_hoodie', 'cas', 36), ('fx_hoodstr', 'w', 37)], 'cas', 140),
         ('후드티 (모자 씀)', [(L2, 'cas', None), ('fx_hoodie', 'cas', 36), ('fx_hoodstr', 'w', 37), ('raw_hood', 'cas', None)], 'cas', 160),
         ('고양이 후드티', [(L2, 'cas', None), ('fx_hoodie', 'cas', 36), ('fx_hoodstr', 'w', 37), ('raw_hood', 'cas', None), ('raw_catears', 'cas', 131)], 'cas', 200),
         ('꽈배기 니트', [(L2, 'cas', None), ('fx_cable', 'cas', 36)], 'cas', 150),
         ('노르딕 니트', [(L2, 'cas', None), ('fx_nordic', 'w', 36)], 'cas', 170),
         ('하트 니트', [(L2, 'cas', None), ('fx_cable', 'cas', 36), ('fx_heart', 'w', 37)], 'cas', 180),
         ('셔츠 + 니트 조끼', [(SH, 'w', None), ('torso_clothes_sleeveless2_vneck', 'cas', 36), ('fx_vest_cable', 'cas', 37)], 'cas', 150),
         ('티 + 카디건', [(TEE, 'w', None), ('torso_clothes_longsleeve2_cardigan', 'cas', 36)], 'cas', 140),
         ('색 셔츠', [('torso_clothes_longsleeve2_buttoned', 'cas', None)], 'cas', 110),
         ('체크 셔츠', [('torso_clothes_longsleeve2_buttoned', 'cas', None), ('fx_check', 'cas', 36)], 'cas', 130),
         ('줄무늬 셔츠', [('torso_clothes_longsleeve2_buttoned', 'cas', None), ('fx_shirt_stripe', 'w', 36)], 'cas', 130),
         ('코트', [(SH, 'w', None), ('fx_coat', 'cas', 36)], 'cas', 220),
         ('티셔츠', [(TEE, 'cas', None)], 'cas', 80), ('줄무늬 티', [(TEE, 'cas', None), ('fx_tee_stripe', 'w', 36)], 'cas', 100),
         ('땡땡이 티', [(TEE, 'cas', None), ('fx_tee_dots', 'w', 36)], 'cas', 100),
         ('멜빵 반바지 + 줄무늬 티', [(TEE, 'w', None), ('fx_tee_stripe', 'cas', 35), ('fx_overall_short', 'cas', None)], 'cas', 170),
         ('땡땡이 미니 원피스', [('fx_dress_mini', 'cas', None), ('fx_dress_dots', 'w', 31)], 'cas', 180),
         ('검은 로브', [('raw_robe_black', 'w', None)], 'cas', 200), ('보라 로브', [('raw_robe_purple', 'w', None)], 'cas', 200),
         ('파란 로브', [('raw_robe_blue', 'w', None)], 'cas', 200), ('빨간 로브', [('raw_robe_red', 'w', None)], 'cas', 200),
         ('후드 로브', [('raw_robe_black', 'w', None), ('raw_hood', 'fix:black', None)], 'cas', 240),
         ('곰 잠옷', ONESIE([('fx_bearears', 'cas', 131)], [('fx_puff', 'cas', 125)]), 'pj', 220),
         ('고양이 잠옷', ONESIE([('raw_catears', 'cas', 131)], [('raw_cattail', 'cas', None)]), 'pj', 240),
         ('토끼 잠옷', ONESIE([('fx_bunnyears', 'cas', 131)], [('fx_puff', 'w', 125)]), 'pj', 240),
         ('여우 잠옷', ONESIE([('raw_wolfears', 'cas', 131)], [('raw_foxtail', 'cas', None)]), 'pj', 260),
         ('잠옷 상의', [('torso_clothes_longsleeve2_buttoned', 'cas', None)], 'pj', 70),
         ('땡땡이 잠옷', [('torso_clothes_longsleeve2_buttoned', 'cas', None), ('fx_pj_dots', 'w', 36)], 'pj', 90),
         ('잠옷 원피스', [('dress_sash', 'cas', None)], 'pj', 120)],
 'legs': [('코트 셋업 치마', [('fx_mini', 'cas', None)], 'cas', 80), ('코트 셋업 바지', [('legs_pants', 'cas', None)], 'cas', 90),
          ('미니 치마', [('fx_mini', None, None)], 'cas', 80), ('주름 미니 치마', [('fx_mini_pleat', None, None)], 'cas', 100),
          ('짧은 반바지', [('legs_shorts_short', None, None)], 'cas', 70), ('레깅스', [('legs_leggings', None, None)], 'cas', 70),
          ('롤업 바지', [('legs_cuffed', None, None)], 'cas', 100),
          ('잠옷 바지', [('legs_pants2', 'cas', None)], 'pj', 60), ('땡땡이 잠옷 바지', [('legs_pants2', 'cas', None), ('fx_pants_dots', 'w', 21)], 'pj', 80)],
 'feet': [('줄무늬 양말 + 구두', [SOCK, ('fx_sock_stripe', 'cas', 14.5), ('feet_shoes_revised', None, None)], 'cas', 90),
          ('흰 양말 + 리본 구두', [SOCK, ('feet_shoes_sara', None, None)], 'cas', 90),
          ('리본 구두', [('feet_shoes_sara', None, None)], 'cas', 80), ('테 부츠', [('feet_boots_rim', None, None)], 'cas', 120),
          ('슬리퍼', [('feet_slippers', None, None)], 'pj', 40)],
 'hat': [('비니', [('fx_beanie', 'hat', None)], 'cas', 70), ('방울 비니', [('fx_beanie', 'hat', None), ('fx_pompom', 'w', 131)], 'cas', 90),
         ('곰 비니', [('fx_beanie', 'hat', None), ('fx_bearears_b', 'hat', 131)], 'cas', 110),
         ('고양이 비니', [('fx_beanie', 'hat', None), ('raw_catears', 'hat', 131)], 'cas', 110),
         ('토끼 비니', [('fx_beanie', 'hat', None), ('fx_bunnyears_b', 'hat', 131)], 'cas', 120),
         ('고양이 귀', [('raw_catears', 'hat', None)], 'cas', 90), ('늑대 귀', [('raw_wolfears', 'hat', None)], 'cas', 90),
         ('머리띠', [('raw_headband', 'hat', None)], 'cas', 50), ('두건', [('raw_bandana', 'hat', None)], 'cas', 60),
         ('후드', [('raw_hood', 'hat', None)], 'cas', 80),
         ('마녀 모자', [('raw_witch', None, None)], 'cas', 150), ('마법사 모자', [('raw_wizard', 'hat', None)], 'cas', 150),
         ('별빛 모자', [('raw_celestial', 'hat', None)], 'cas', 170), ('산타 모자', [('raw_santa', None, None)], 'cas', 100)]}
COMBO['hat'] = []
for cat, lst in SHOP.items(): COMBO[cat] = [(n, c, 'uni', 0) for n, c in COMBO[cat]] + lst
pool = {e['id']: e for es in items.values() for e in es}
# 직접 손본 그림 (fx:종류:원본): 블레이저(카디건 + 깃·길이), 가슴 배지, 주름치마·짧은 치마 (무릎 위)
def fxent(base, kind, sl=None):
    return dict(L={b: [(z, 'fx:%s:%s' % (kind, f), mat, src, sl) for z, f, mat, src, _ in Ls] for b, Ls in pool[base]['L'].items()})
pool['fx_blazer'] = fxent('torso_clothes_longsleeve2_cardigan', 'blazer')
pool['fx_emblem'] = fxent('torso_clothes_longsleeve2_cardigan', 'emblem')
pool['fx_pleat'] = fxent('legs_skirts_plain', 'pleat')
pool['fx_short'] = fxent('legs_skirt_straight', 'short')
pool['fx_dress'] = fxent('dress_bodice', 'short')
pool['fx_dress2'] = fxent('dress_sash', 'short')
# 옷 가게용: 줄무늬·땡땡이 무늬 (흰 무늬 층을 위에 겹쳐요), 미니 기장
FXNEW = {'fx_tee_stripe': (TEE, 'stripe'), 'fx_tee_dots': (TEE, 'dots'), 'fx_long_stripe': ('torso_clothes_longsleeve2', 'stripe'),
         'fx_overall_short': ('torso_aprons_overalls', 'short'), 'fx_dress_mini': ('dress_sash', 'short'), 'fx_dress_dots': ('dress_sash', 'dotsshort'),
         'fx_bodice_mini': ('dress_bodice', 'short'), 'fx_pj_dots': ('torso_clothes_longsleeve2_buttoned', 'dots'),
         'fx_mini': ('legs_skirts_plain', 'mini'), 'fx_mini_pleat': ('legs_skirts_plain', 'minipleat'), 'fx_pants_dots': ('legs_pants2', 'dots'),
         'fx_sock_stripe': ('feet_socks_high', 'stripe')}
for k, (base, kind) in FXNEW.items(): pool[k] = fxent(base, kind)
# LPC 파일 직접 (모자·귀·꼬리·로브). 털 그림(hair 팔레트)은 fx:tocloth 로 천 팔레트로 바꿔서 옷 색으로 칠해요
SP_ = 'spritesheets/'
RAW = {'raw_hood': [(130, 'hat/cloth/hood/adult/walk.png')], 'raw_headband': [(125, 'hat/headband/thick/adult/walk.png')],
       'raw_bandana': [(120, 'hat/cloth/bandana/adult/walk.png')], 'raw_santa': [(130, 'hat/holiday/christmas/adult/walk/red.png')],
       'raw_witch': [(130, 'hat/magic/large/adult/walk/brown.png')], 'raw_wizard': [(130, 'hat/magic/wizard/base/adult/walk.png')],
       'raw_celestial': [(130, 'hat/magic/celestial/adult/walk.png')],
       'raw_catears': [(130, 'fx:tocloth:' + SP_ + 'head/ears/cat/adult/fg/walk.png'), (8, 'fx:tocloth:' + SP_ + 'head/ears/cat/adult/bg/walk.png')],
       'raw_wolfears': [(130, 'fx:tocloth:' + SP_ + 'head/ears/wolf/adult/fg/walk.png'), (8, 'fx:tocloth:' + SP_ + 'head/ears/wolf/adult/bg/walk.png')],
       'raw_cattail': [(125, 'fx:tocloth:' + SP_ + 'body/tail/cat/adult/fg/walk/white.png'), (5, 'fx:tocloth:' + SP_ + 'body/tail/cat/adult/bg/walk/white.png')],
       'raw_foxtail': [(125, 'fx:tocloth:' + SP_ + 'body/tail/fluffy/adult/fg/walk/white.png'), (5, 'fx:tocloth:' + SP_ + 'body/tail/fluffy/adult/bg/walk/white.png')]}
for c in ('black', 'purple', 'blue', 'red'): RAW['raw_robe_' + c] = [(35, 'torso/clothes/robe/female/walk/%s.png' % c)]
for k, Ls in RAW.items(): pool[k] = dict(L={b: [(z, f if f.startswith('fx:') else SP_ + f, 'cloth', 'white', None) for z, f in Ls] for b in BODIES})
RAW_DEFS = ['headwear/coverings/hoods/hat_hood_cloth.json', 'headwear/coverings/headbands/hat_headband_thick.json', 'headwear/coverings/bandana/hat_bandana.json',
            'headwear/hats/holiday/hat_holiday_christmas.json', 'headwear/hats/magic/hat_magic_large.json', 'headwear/hats/magic/hat_magic_wizard.json',
            'headwear/hats/magic/hat_magic_celestial.json', 'head/furry_ears/top/head_ears_cat.json', 'head/furry_ears/top/head_ears_wolf.json',
            'body/tails/tail_cat.json', 'body/tails/tail_wolf_fluffy.json', 'torso/shirts/torso_clothes_robe.json']
# 그려 넣는 무늬·부품 (원본 그림을 보고 위치를 잡아요)
HOODF = SP_ + 'hat/cloth/hood/adult/walk.png'
FXDRAW = {'fx_hoodie': (L2, 'hoodie'), 'fx_hoodstr': (L2, 'hoodstr'), 'fx_cable': (L2, 'cable'), 'fx_nordic': (L2, 'nordic'), 'fx_heart': (L2, 'heart'),
          'fx_vest_cable': ('torso_clothes_sleeveless2_vneck', 'cable'), 'fx_check': ('torso_clothes_longsleeve2_buttoned', 'check'),
          'fx_shirt_stripe': ('torso_clothes_longsleeve2_buttoned', 'stripe'), 'fx_coat': ('torso_clothes_longsleeve2_cardigan', 'coat'),
          'fx_puff': (L2, 'puff')}
for k, (base, kind) in FXDRAW.items(): pool[k] = fxent(base, kind)
for k, kind in (('fx_beanie', 'beanie'), ('fx_pompom', 'pompom'), ('fx_bearears', 'bearears'), ('fx_bunnyears', 'bunnyears'),
                ('fx_bearears_b', 'bearearsb'), ('fx_bunnyears_b', 'bunnyearsb')):
    pool[k] = dict(L={b: [(130, 'fx:%s:%s' % (kind, HOODF), 'cloth', 'white', None)] for b in BODIES})
FXBASE0 = {'fx_blazer': 'torso_clothes_longsleeve2_cardigan', 'fx_emblem': 'torso_clothes_longsleeve2_cardigan', 'fx_pleat': 'legs_skirts_plain', 'fx_short': 'legs_skirt_straight', 'fx_dress': 'dress_bodice', 'fx_dress2': 'dress_sash'}
for cat, lst in COMBO.items():
    out = []
    for row in lst:
        nm, comps = row[:2]
        e = dict(id='%s_%d' % (cat, len(out)), name=nm, L={})
        if len(row) > 2: e['k'], e['p'] = row[2], row[3]
        for body in BODIES:
            cs = [(i[body] if isinstance(i, dict) else i, sl, zz) for i, sl, zz in comps]
            if not all(i in pool and body in pool[i]['L'] for i, _, _ in cs): continue
            e['L'][body] = [(z if zz is None else zz, f, mat, src, sl if not isinstance(sl, tuple) else sl[k])
                            for i, sl, zz in cs for k, (z, f, mat, src, _) in enumerate(pool[i]['L'][body])]
        if e['L']: out.append(e)
    items[cat] = out
del items['x']
KEEP = {'neck': ['neck_necktie', 'neck_bowtie', 'neck_bowtie2', 'neck_cravat', 'neck_scarf']}
for cat, ids in KEEP.items():
    by = {e['id']: e for e in items[cat]}; items[cat] = [by[i] for i in ids if i in by]
need = {f for es in items.values() for e in es for Ls in e['L'].values() for _, f, _, _, _ in Ls}
for body in BODIES: need.add('spritesheets/' + HEAD[body] + 'walk.png')
used = {e['id'] for es in items.values() for e in es} | {j for lst in COMBO.values() for row in lst for i, _, _ in row[1] for j in (i.values() if isinstance(i, dict) else [i])}
FXBASE = {**FXBASE0, **{k: v[0] for k, v in FXNEW.items()}, **{k: v[0] for k, v in FXDRAW.items()}}
used |= {FXBASE[i] for i in list(used) if i in FXBASE}
credits = [c for cat, lst in SEL.items() for rel, _ in lst if os.path.basename(rel)[:-5] in used for c in jd(rel).get('credits', [])] + [c for rel in RAW_DEFS for c in jd(rel).get('credits', [])]
print({c: len(v) for c, v in items.items()}, 'files', len(need))
# 받기
FXN = {f for f in need if f.startswith('fx:')}; need = (need - FXN) | {f.split(':', 2)[2] for f in FXN}
missing = [f for f in need if not os.path.exists(os.path.join(LPC, f))]
if missing:
    subprocess.run(['git', '-C', LPC, 'sparse-checkout', 'add', '--no-cone'] + ['/' + f for f in missing], check=True, capture_output=True)
    subprocess.run(['git', '-C', LPC, 'checkout'], check=True, capture_output=True)
# ---------- 자르기 ----------
def load(f):
    im = Image.open(os.path.join(LPC, f)).convert('RGBA'); a = np.array(im)
    if a.shape[:2] != (256, 576): print('size?', f, a.shape); return None
    return a
IMG = {f: load(f) for f in sorted(need)}
# ---------- 손본 그림 ----------
WHITE = [tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) for h in PAL['cloth']['white']]
def pidx(c): return min(range(len(WHITE)), key=lambda i: sum(abs(int(c[j]) - WHITE[i][j]) for j in range(3)))
def setc(a, y, x, i): a[y, x, :3] = WHITE[max(0, min(len(WHITE) - 1, i))]; a[y, x, 3] = 255
def cells(a):
    for r in range(4):
        for c in range(9): yield r, a[r * 64:(r + 1) * 64, c * 64:(c + 1) * 64]
def fx_pleat(a, hem=51, pleat=True):
    a = a.copy()
    for r, cl in cells(a):
        m = cl[..., 3] > 0
        cl[hem + 1:] = 0
        for x in range(64):
            if m[hem, x]: setc(cl, hem, x, 0)
        if not pleat: continue
        for y in range(46, hem):                              # 체크무늬 (2칸 격자) = 교복 치마
            for x in range(64):
                if m[y, x] and m[y, x - 1] and m[y, x + 1] and ((x // 2) + (y // 2)) % 2 == 0:
                    i = pidx(cl[y, x]); setc(cl, y, x, i - 1) if i > 1 else None
    return a
def fx_blazer(a):
    a = a.copy()
    for r, cl in cells(a):
        m = cl[..., 3] > 0
        if not m.any(): continue
        ys = np.nonzero(m.any(1))[0]; y1 = ys.max()
        # 길이: 아래 두 줄 더 (엉덩이까지)
        for x in range(64):
            if m[y1, x]:
                cl[y1 + 2, x] = cl[y1, x]; cl[y1, x] = cl[y1 - 1, x]; cl[y1 + 1, x] = cl[y1 - 1, x]
        if r != 2: continue                                   # 깃은 앞모습만
        y0 = ys.min()
        for y in range(y0, y0 + 6):
            for x in range(1, 63):
                if m[y, x] and not m[y, x + 1] and x < 32: setc(cl, y, x, 4); m[y, x - 1] and setc(cl, y, x - 1, 1)
                if m[y, x] and not m[y, x - 1] and x >= 32: setc(cl, y, x, 4); m[y, x + 1] and setc(cl, y, x + 1, 1)
    return a
def fx_emblem(a):
    o = np.zeros_like(a)                                     # 앞모습 왼쪽 가슴 2×2 (기숙사 색)
    for c in range(9):
        cl = a[2 * 64:3 * 64, c * 64:(c + 1) * 64]; m = cl[..., 3] > 0
        if not m.any(): continue
        dy = np.nonzero(m.any(1))[0].min() - 34; oc = o[2 * 64:3 * 64, c * 64:(c + 1) * 64]
        for (yy, xx), i in {(0, 0): 5, (0, 1): 4, (1, 0): 4, (1, 1): 3}.items(): setc(oc, 40 + dy + yy, 38 + xx, i)
    return o
def fx_pattern(a, kind):
    """흰 무늬 층: 옷 안쪽 픽셀(테두리 빼고)에 줄무늬(3줄마다)나 땡땡이(4칸 격자)"""
    o = np.zeros_like(a)
    for r in range(4):
        for c in range(9):
            cl = a[r * 64:(r + 1) * 64, c * 64:(c + 1) * 64]; oc = o[r * 64:(r + 1) * 64, c * 64:(c + 1) * 64]; m = cl[..., 3] > 0
            if not m.any(): continue
            y0 = np.nonzero(m.any(1))[0].min()
            for y in range(1, 63):
                for x in range(1, 63):
                    if not (m[y, x] and m[y - 1, x] and m[y + 1, x] and m[y, x - 1] and m[y, x + 1]): continue
                    i = pidx(cl[y, x])
                    if i <= 1: continue                               # 테두리·주름은 그대로
                    if kind == 'stripe' and (y - y0) % 3 == 1: setc(oc, y, x, min(5, i + 1))
                    if kind == 'dots' and (y - y0) % 4 == 1 and (x + 2 * (((y - y0) // 4) % 2)) % 4 == 0: setc(oc, y, x, 5)
    return o
# ---------- 옷 가게용 그려 넣기 ----------
HAIRC = {tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)): k for pal in PAL['hair'].values() for k, h in enumerate(pal)}
def fx_tocloth(a):
    """털·귀 그림(hair 팔레트) → 천 흰 팔레트 (같은 칸 번호) : 옷 색으로 칠할 수 있게"""
    a = a.copy(); m = a[..., 3] > 0
    for y, x in zip(*np.nonzero(m)):
        k = HAIRC.get(tuple(int(v) for v in a[y, x, :3]))
        if k is not None: a[y, x, :3] = WHITE[k]
    return a
def each(a, fn, out=None):
    """칸(방향 r, 프레임 c)마다 fn(원본 칸, 결과 칸, r, 마스크)"""
    o = np.zeros_like(a) if out is None else out
    for r in range(4):
        for c in range(9):
            cl = a[r * 64:(r + 1) * 64, c * 64:(c + 1) * 64]; m = cl[..., 3] > 0
            if m.any(): fn(cl, o[r * 64:(r + 1) * 64, c * 64:(c + 1) * 64], r, m)
    return o
def put(oc, y, x, i=None, rgb=None):
    if 0 <= y < 64 and 0 <= x < 64:
        if rgb: oc[y, x, :3] = rgb; oc[y, x, 3] = 255
        else: setc(oc, y, x, i)
def inner(m, y, x): return 0 < y < 63 and 0 < x < 63 and m[y, x] and m[y - 1, x] and m[y + 1, x] and m[y, x - 1] and m[y, x + 1]
def top_of(m): return int(np.nonzero(m.any(1))[0].min())
def span(m, y): xs = np.nonzero(m[y])[0]; return (int(xs.min()), int(xs.max())) if len(xs) else (28, 35)
def fx_hoodie(a):
    def f(cl, oc, r, m):
        t = top_of(m); l, rr = span(m, t + 1)
        if r == 0:                                            # 뒤: 후드가 등에 늘어져요
            for dy in range(0, 5):
                w = [4, 5, 5, 4, 3][dy]
                for x in range(31 - w, 33 + w):
                    edge = x in (31 - w, 32 + w) or dy == 4
                    put(oc, t + dy, x, 1 if edge else (3 if dy < 2 else 2))
        elif r == 2:                                          # 앞: 목둘레 + 캥거루 주머니
            for x in range(l + 3, rr - 2):
                if m[t + 1, x]: put(oc, t + 1, x, 2)
            py = t + 9
            for x in range(27, 37):
                if m[py, x]: put(oc, py, x, 1)
            for y in range(py, py + 3):
                for x in (27, 36):
                    if m[y, x]: put(oc, y, x, 1)
        else:                                                 # 옆: 등 쪽에 후드 혹
            bx = rr if r == 1 else l
            for dy in range(0, 4):
                for k in range(0, 3 - dy // 2):
                    x = bx - k if r == 1 else bx + k
                    put(oc, t + dy, x, 1 if k == 0 or dy == 3 else 3)
    return each(a, f)
def fx_hoodstr(a):
    def f(cl, oc, r, m):
        if r != 2: return
        t = top_of(m)
        for x in (30, 33):
            for y in (t + 3, t + 4, t + 5): put(oc, y, x, 5)
    return each(a, f)
def fx_knit(a, kind):
    def f(cl, oc, r, m):
        t = top_of(m); y1 = int(np.nonzero(m.any(1))[0].max())
        for y in range(64):
            for x in range(64):
                if not inner(m, y, x): continue
                i = pidx(cl[y, x])
                if i <= 1: continue
                if kind == 'cable':                           # 꽈배기: 세로 골 + 지그재그, 밑단 고무단
                    if (x - 32) % 4 == 0 or ((x - 32) % 4 == 2 and (y - t) % 2 == 0) or y >= y1 - 2 and x % 2 == 0: put(oc, y, x, i - 1)
                elif kind == 'check':
                    a1, b1 = (x - 32) % 4 == 0, (y - t) % 4 == 2
                    if a1 or b1: put(oc, y, x, max(1, i - (2 if a1 and b1 else 1)))
                elif kind == 'nordic':                        # 가슴에 흰 무늬 띠
                    yy = y - t
                    if yy in (4, 8) or (yy in (5, 7) and (x - 32) % 2 == 0) or (yy == 6 and (x - 32) % 4 in (1, 2)): put(oc, y, x, min(5, i + 1))
                elif kind == 'stripe':
                    if (y - t) % 3 == 1: put(oc, y, x, min(5, i + 1))
    return each(a, f)
def fx_heart(a):
    R, D = (226, 74, 110), (150, 34, 70)
    shape = ['.#.#.', '#####', '.###.', '..#..']
    def f(cl, oc, r, m):
        if r != 2: return
        t = top_of(m)
        for dy, row in enumerate(shape):
            for dx, ch in enumerate(row):
                if ch == '#': put(oc, t + 6 + dy, 34 + dx, rgb=R if dy < 2 else D)
    return each(a, f)
def fx_coat(a):
    a = a.copy()
    def f(cl, oc, r, m):
        ys = np.nonzero(m.any(1))[0]; t, y1 = int(ys.min()), int(ys.max())
        src = cl[y1 - 1].copy(); msk = m[y1 - 1].copy()
        for k in range(0, 6):                                 # 엉덩이 아래까지 길게
            for x in range(64):
                if msk[x]: cl[y1 + k, x] = src[x]
        for x in range(64):
            if msk[x]: setc(cl, y1 + 6, x, 0)
        if r == 2:
            for y in (t + 8, t + 11, t + 14): setc(cl, y, 33, 1)   # 단추
            for y in range(t, t + 6):                          # 깃
                for x in range(1, 63):
                    if m[y, x] and not m[y, x + 1] and x < 32: setc(cl, y, x, 4)
                    if m[y, x] and not m[y, x - 1] and x >= 32: setc(cl, y, x, 4)
    each(a, f, out=a)
    return a
def fx_puff(a):
    def f(cl, oc, r, m):
        y1 = int(np.nonzero(m.any(1))[0].max())
        if r == 2: return
        cx = 32 if r == 0 else (span(m, y1 - 2)[1] + 1 if r == 1 else span(m, y1 - 2)[0] - 1)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                edge = abs(dy) + abs(dx) == 2
                if not edge: put(oc, y1 - 1 + dy, cx + dx, 5 if dy < 1 else 4)
        for dy, dx in ((-2, 0), (2, 0), (0, -2), (0, 2)): put(oc, y1 - 1 + dy, cx + dx, 1)
    return each(a, f)
def fx_beanie(a, rows=7):
    a = a.copy()
    def f(cl, oc, r, m):
        t = top_of(m); cl[t + rows + 1:] = 0
        for x in range(64):
            if cl[t + rows, x, 3]: setc(cl, t + rows, x, 1)
            if cl[t + rows - 1, x, 3]: setc(cl, t + rows - 1, x, 3 if x % 2 else 2)
    each(a, f, out=a)
    return a
def fx_hatdraw(a, kind):
    def f(cl, oc, r, m):
        t = top_of(m); l, rr = span(m, t + 1); cx = (l + rr) // 2
        side = r in (1, 3)
        if kind == 'pompom':
            for dy in range(-3, 0):
                for dx in (-1, 0, 1):
                    if not (dy == -3 and dx) : put(oc, t + dy, cx + dx, 5 if dy > -3 else 4)
            return
        xs = [cx + (1 if r == 1 else -1)] if side else [cx - 5, cx + 5]
        for ex in xs:
            if kind == 'bear':                                # 동그란 곰 귀
                for dy, row in enumerate(['.##.', '#oo#', '#oi#']):
                    for dx, ch in enumerate(row):
                        if ch != '.': put(oc, t - 2 + dy, ex - 2 + dx, {'#': 1, 'o': 4, 'i': 2}[ch])
            else:                                             # 긴 토끼 귀 (속은 분홍)
                rows = ['.##.', '#oo#', '#pi#', '#pi#', '#pi#', '#pi#', '#oo#', '#oo#']
                for dy, row in enumerate(rows):
                    for dx, ch in enumerate(row):
                        if ch == '.': continue
                        y, x = t - len(rows) + 1 + dy, ex - 2 + dx
                        if ch == 'p': put(oc, y, x, rgb=(240, 160, 180))
                        elif ch == 'i': put(oc, y, x, rgb=(214, 120, 148))
                        else: put(oc, y, x, 1 if ch == '#' else 4)
    return each(a, f)
FXF = {'blazer': fx_blazer, 'emblem': fx_emblem, 'pleat': fx_pleat, 'short': lambda a: fx_pleat(a, pleat=False),
       'stripe': lambda a: fx_pattern(a, 'stripe'), 'dots': lambda a: fx_pattern(a, 'dots'),
       'dotsshort': lambda a: fx_pattern(fx_pleat(a, pleat=False), 'dots'),
       'mini': lambda a: fx_pleat(a, hem=50, pleat=False),
       'tocloth': fx_tocloth, 'hoodie': fx_hoodie, 'hoodstr': fx_hoodstr, 'cable': lambda a: fx_knit(a, 'cable'), 'check': lambda a: fx_knit(a, 'check'),
       'nordic': lambda a: fx_knit(a, 'nordic'), 'heart': fx_heart, 'coat': fx_coat, 'puff': fx_puff, 'beanie': fx_beanie,
       'pompom': lambda a: fx_hatdraw(a, 'pompom'), 'bearears': lambda a: fx_hatdraw(a, 'bear'), 'bunnyears': lambda a: fx_hatdraw(a, 'bunny'),
       'bearearsb': lambda a: fx_hatdraw(a, 'bear'), 'bunnyearsb': lambda a: fx_hatdraw(a, 'bunny'), 'minipleat': lambda a: fx_minipleat(fx_pleat(a, hem=50, pleat=False))}
def fx_minipleat(a):
    a = a.copy()                                              # 세로 주름 (2칸마다 어둡게)
    for r, cl in cells(a):
        m = cl[..., 3] > 0
        for y in range(46, 50):
            for x in range(1, 63):
                if m[y, x] and m[y, x - 1] and m[y, x + 1] and x % 2 == 0:
                    i = pidx(cl[y, x]); setc(cl, y, x, i - 1) if i > 1 else None
    return a
for f in sorted(FXN):
    _, kind, src = f.split(':', 2); IMG[f] = FXF[kind](IMG[src])
u = np.zeros((64, 64), bool)
for f, a in IMG.items():
    if a is None: continue
    for d in DIRS:
        for c in COLS: u |= a[ROWS[d] * 64:(ROWS[d] + 1) * 64, c * 64:(c + 1) * 64, 3] > 0
ys, xs = np.nonzero(u); X0, X1, Y0, Y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
FW, FH = int(X1 - X0), int(Y1 - Y0); NF = len(DIRS) * len(COLS)
print('frame', FW, FH, 'crop', X0, Y0)
# 더 날씬하게: 목 아래(64칸 기준 y≥36)에서 몸통·다리 사이 세로줄 2개를 빼고 양쪽을 1칸씩 안으로 (모든 부품 똑같이)
# 다리 모으기 + 날씬하게: 줄마다 빼는 세로줄 (원래 64칸 좌표). 뺀 만큼 양쪽에서 안으로 당겨 가운데는 그대로
#   teen 몸은 다리 사이가 2칸 벌어져 있어요 → 다리 줄(y≥51)에서 가운데 2줄(31·32)을 빼서 다리를 붙여요
#   legs4: 앞은 살짝(몸통·다리 1줄씩), 옆은 몸통 4줄·다리 3줄 (앞에선 너무 얇고 옆에선 너무 두꺼웠어요)
_N = {'left': set(), 'right': set()}
PRESET = {
 'legs':  [(51, 64, {'down': {31, 32}, 'up': {31, 32}, **_N})],
 'legs1': [(36, 51, {'down': {28, 35}, 'up': {28, 35}, **_N}), (51, 64, {'down': {28, 31, 32, 35}, 'up': {28, 31, 32, 35}, **_N})],
 'legs3': [(33, 51, {'down': {21, 26, 28, 35, 37, 42}, 'up': {21, 26, 28, 35, 37, 42}, 'left': {29, 34}, 'right': {29, 34}}),
           (51, 64, {'down': {26, 28, 31, 32, 35, 37}, 'up': {26, 28, 31, 32, 35, 37}, **_N})],
 'legs4': [(33, 51, {'down': {21, 28, 35, 42}, 'up': {21, 28, 35, 42}, 'left': {28, 31, 34, 37}, 'right': {26, 29, 32, 35}}),
           (51, 64, {'down': {28, 31, 32, 35}, 'up': {28, 31, 32, 35}, 'left': {29, 32, 35}, 'right': {28, 31, 34}})],
 'legs2': [(33, 51, {'down': {21, 28, 35, 42}, 'up': {21, 28, 35, 42}, **_N}), (51, 64, {'down': {28, 31, 32, 35}, 'up': {28, 31, 32, 35}, **_N})],
}
SLIM = PRESET[os.environ.get('LPC_BODY', 'legs4')]
def slim(cell, d, neck=True):
    o = cell.copy()
    for y0, y1, cols in SLIM:
        if not neck: y0 = max(y0, 36)        # 머리카락·머리: 어깨 줄(33~35)은 그대로 (안 그러면 머리카락이 얼굴로 파고들어요)
        C = cols[d]; keep = [x for x in range(64) if x not in C]; nl = sum(1 for c in C if c < 32)
        b = cell[y0:y1][:, keep]; o[y0:y1] = 0; o[y0:y1, nl:nl + len(keep)] = b
    return o
def strip(a, neck=True):
    o = np.zeros((FH, FW * NF, 4), np.uint8); k = 0
    for d in DIRS:
        for c in COLS:
            o[:, k * FW:(k + 1) * FW] = slim(a[ROWS[d] * 64:(ROWS[d] + 1) * 64, c * 64:(c + 1) * 64], d, neck)[Y0:Y1, X0:X1]; k += 1
    return o
os.makedirs(OUTP, exist_ok=True)
for old in glob.glob(os.path.join(OUTP, '*.png')): os.remove(old)
def hexrgb(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)])
def hit(a, pal):
    m = a[..., 3] > 0; c = a[..., :3][m].astype(int)
    if not len(c): return 0
    P = np.stack([hexrgb(h) for h in pal]); d = np.abs(c[:, None, :] - P[None]).max(-1).min(-1)
    return float((d <= 1).mean())
def maps_of(cat, f, mat, src, sl=None):
    """층 그림이 실제로 어느 팔레트로 그려졌는지 맞춰 봐요 (안 맞으면 색 그대로)"""
    a = IMG[f]
    if cat in ('body', 'face'): return [['skin', 'light'], ['eye', 'blue']]
    if sl == 'w': return []
    if sl and sl.startswith('fix:'): cat = 'top'   # 정해진 색 (예: 로브 후드)
    slot = sl or SLOT[cat]; m = {'hair': 'hair'}.get(mat, 'hair' if cat == 'hair' else 'cloth')
    cands = [src] if src in PAL[m] else []
    cands += [k for k in PAL[m] if k not in cands]
    best = max(cands, key=lambda k: hit(a, PAL[m][k]))
    return [[slot, best]] if hit(a, PAL[m][best]) >= .5 else []
meta = dict(fw=FW, fh=FH, frames=NF, dirs={d: i * len(COLS) for i, d in enumerate(DIRS)}, walk=list(range(1, len(COLS))), bodies=BODIES, parts={})
def write(cat, idx, entry, extra=None):
    rows, rowmap, L = [], {}, {}
    for body, Ls in entry['L'].items():
        L[body] = []
        for z, f, mat, src, sl in Ls:
            if IMG.get(f) is None: continue
            if f not in rowmap: rowmap[f] = len(rows); rows.append(strip(IMG[f], cat != 'hair' and 'heads/' not in f))
            L[body].append([rowmap[f], z, maps_of(cat, f, mat, src, sl)])
    if not rows: return None
    name = f'{cat}_{idx:03d}.png'; Image.fromarray(np.concatenate(rows, 0)).save(os.path.join(OUTP, name), optimize=True)
    out = dict(id=entry['id'], n=KO.get(entry['name'], entry['name']), f='art/lpc/' + name, L=L)
    if entry.get('k'): out['k'] = entry['k']; out['p'] = entry['p']     # 종류 (uni 교복·cas 사복·pj 잠옷), 값
    return out
# 몸 = 몸통 + 머리 (체형마다)
body_entry = dict(id='body', name='body', L={b: [(10, 'spritesheets/body/bodies/' + BODYKEY[b] + '/walk.png', 'body', 'light', None), (100, 'spritesheets/' + HEAD[b] + 'walk.png', 'body', 'light', None)] for b in BODIES})
meta['parts']['body'] = [write('body', 0, body_entry)]
for cat in [c for c in SEL if c not in ('body', 'x')]:
    meta['parts'][cat] = [p for p in (write(cat, i, e) for i, e in enumerate(items[cat])) if p]
for cat, nm in (('face', '기본'), ('cape', '없음'), ('neck', '없음'), ('hat', '없음')):
    meta['parts'][cat].insert(0, dict(id='none', n=nm, f=None, L={b: [] for b in BODIES}))
meta['pal'] = {'skin': PAL['body'], 'hair': PAL['hair'], 'eye': PAL['eye'], 'cloth': PAL['cloth']}
meta['pal']['bottom'] = meta['pal']['shoe'] = PAL['cloth']   # 교복 하의·신발: 천 팔레트에서 몇 색만
# 고를 수 있는 색 (순서 = 색 번호). 피부는 사람 피부 7 + 판타지 몇 가지
meta['colors'] = {'skin': ['light', 'amber', 'olive', 'taupe', 'bronze', 'brown', 'black', 'lavender', 'blue', 'pale_green', 'zombie_green'],
                  'hair': list(PAL['hair']), 'eye': list(PAL['eye']), 'cloth': list(PAL['cloth']),
                  'bottom': ['gray', 'school', 'charcoal', 'black', 'navy', 'slate', 'bluegray', 'maroon', 'brown', 'tan', 'blue', 'sky', 'forest', 'pink', 'lavender', 'white'],
                  'shoe': ['black', 'brown', 'walnut', 'leather', 'charcoal', 'maroon', 'navy', 'white']}
PAL['cloth']['school'] = ['#0A0A14', '#121426', '#1A1F38', '#232B4C', '#2D3961', '#3A4A78']   # 교복 남색 (진하게)
meta['fixed'] = {'sch': 'school', 'sock': 'white'}   # 학교 색 (교복 겉옷·망토), 양말
meta['house'] = {'dew': 'forest', 'ember': 'orange', 'dusk': 'rose', 'moon': 'purple'}   # 기숙사 → 교복 겉옷·망토·넥타이 색
# 얼굴 동그라미: 정면 서기 프레임의 머리 상자 (정사각형)
ha = strip(IMG['spritesheets/' + HEAD['female'] + 'walk.png'])[:, :FW, 3] > 0; ys, xs = np.nonzero(ha)
hs = int(max(xs.max() - xs.min(), ys.max() - ys.min()) + 5); hcx = (xs.min() + xs.max()) / 2
meta['head'] = dict(x=int(round(hcx - hs / 2)), y=int(max(0, ys.min() - 3)), s=hs)
meta['scale'] = .75
# 크레딧 (같은 파일은 한 번)
seen, cr = set(), []
for c in credits:
    k = c.get('file')
    if k in seen: continue
    seen.add(k); cr.append(dict(file=k, authors=c.get('authors', []), licenses=c.get('licenses', []), urls=c.get('urls', [])))
json.dump(cr, open(os.path.join(ROOT, 'public', 'credits.json'), 'w'), ensure_ascii=False, indent=0)   # 게임 크레딧 화면이 읽어요
json.dump(meta, open(OUTM, 'w'), ensure_ascii=False)
tot = sum(os.path.getsize(p) for p in glob.glob(os.path.join(OUTP, '*.png')))
print({c: len(v) for c, v in meta['parts'].items()}, 'png', len(glob.glob(os.path.join(OUTP, '*.png'))), 'KB', tot // 1024, 'credits', len(cr))
