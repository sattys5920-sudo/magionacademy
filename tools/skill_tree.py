# 탐사 스킬 트리 데이터(직업 12 × 줄기 3 × 스킬 5) → index.html의 XT 상수 + public/art/skills.png (15칸 × 12줄, 28px 타일 ×2)
# 사용: python3 tools/skill_tree.py   (코드 표: d 단일딜 D 광역딜 c 차지딜 h 단일힐 H 광역힐 r 부활 B 아군 공격↑ b 나 공격↑ G 아군 피해↓ g 나 피해↓
#        X 아군 가속 x 나 가속 S 적 느리게 s 적 하나 느리게 W 적 하나 약화 w 적 전체 약화 F 지속피해 f 전체 지속피해 Z 기절 M 마력 회복 P:키 패시브)
import json, math, re
from PIL import Image, ImageDraw
T = {
 'warrior': [('차지', [('강타','d','sword'),('차지 베기','c','sword'),('대지 가르기','D','swirl'),('분노의 일격','d','fist'),('극한 차지','c','bolt')]),
             ('근성', [('단단한 피부','P:def','shield'),('되받아치기','d','fist'),('불굴','P:hp','heart'),('피의 갈증','P:vamp','drop'),('전장의 포효','b','up')]),
             ('도끼술', [('회전 베기','D','axe'),('투척 도끼','d','axe'),('파쇄','W','axe'),('학살자','d','skull'),('폭풍 도끼','D','axe')])],
 'black': [('화염', [('불꽃탄','d','fire'),('화염구','D','fire'),('불씨','F','fire'),('지옥불','D','fire'),('메테오','D','burst')]),
           ('냉기와 번개', [('서리 화살','d','ice'),('얼음 창','d','ice'),('번개','d','bolt'),('연쇄 번개','D','bolt'),('눈보라','S','ice')]),
           ('암흑', [('마력 흡수','M','moon'),('약점 간파','w','eye'),('암흑 구체','d','moon'),('공허의 손','Z','swirl'),('마력 폭주','P:mag','star')])],
 'thief': [('연속', [('찌르기','d','dagger'),('이중 베기','d','dagger'),('칼춤','D','dagger'),('연환','d','swirl'),('난도질','c','dagger')]),
           ('급소', [('약점 노리기','P:crit','eye'),('출혈','F','drop'),('급소 찌르기','c','dagger'),('처형자','d','skull'),('피 웅덩이','f','drop')]),
           ('그림자', [('재빠른 발','P:spd','wing'),('연막','w','ghost'),('그림자 걸음','x','wing'),('훔치기','d','fist'),('뒤잡기','Z','dagger')])],
 'bard': [('전투가', [('용기의 노래','B','note'),('승리의 행진','B','note'),('전장의 북소리','X','note'),('불꽃의 변주','D','fire'),('영웅의 서사시','B','crown')]),
          ('안식가', [('수호의 노래','G','note'),('자장가','H','note'),('평온의 선율','H','note'),('되살림의 화음','r','note'),('별빛 합창','H','star')]),
          ('풍자', [('불협화음','w','note'),('도발의 곡','s','note'),('흥겨운 춤','X','wing'),('앙코르','B','note'),('대합창','D','note')])],
 'time': [('가속', [('서두르기','x','clock'),('연속 가속','X','clock'),('시간 도약','x','bolt'),('가속 영역','X','clock'),('질주','P:spd','wing')]),
          ('감속', [('늦추기','s','clock'),('정지','Z','clock'),('늪 같은 시간','S','swirl'),('시간 정체','S','clock'),('영원한 정오','D','sun')]),
          ('시간 조작', [('되감기','h','clock'),('예지','P:def','eye'),('시계 소환','Z','clock'),('시간 균열','d','swirl'),('시간 정지','X','star')])],
 'alch': [('약화', [('산성 플라스크','d','flask'),('독 병','F','flask'),('불안정 용액','w','flask'),('부식','W','flask'),('약점 증폭','w','eye')]),
          ('혼합', [('응급 물약','h','flask'),('마력 물약','M','flask'),('혼합 약','h','flask'),('엘릭서','H','flask'),('변이약','B','flask')]),
          ('폭발물', [('폭죽탄','d','bomb'),('점착 폭탄','s','bomb'),('연쇄 반응','D','bomb'),('황금 폭발','d','burst'),('연금 대폭발','D','burst')])],
 'white': [('회복', [('치유','h','cross'),('큰 치유','h','cross'),('집단 치유','H','cross'),('신성한 비','H','drop'),('기적의 손길','h','star')]),
           ('부활', [('되살리기','r','wing'),('가호','P:hp','heart'),('완전 소생','r','wing'),('전체 소생','H','wing'),('천사의 숨결','H','wing')]),
           ('성광', [('성광탄','d','star'),('정화','H','sun'),('빛의 장막','G','sun'),('심판의 빛','D','sun'),('광휘의 후광','B','sun')])],
 'druid': [('재생', [('새싹','h','leaf'),('재생의 숲','H','leaf'),('뿌리 속박','s','leaf'),('생명의 나무','h','tree'),('만개','H','leaf')]),
           ('자연', [('자연 보호막','G','leaf'),('이슬','h','drop'),('독 제거','H','drop'),('태양의 은총','B','sun'),('대지의 축복','P:hp','heart')]),
           ('야수', [('가시 덩굴','d','leaf'),('곰의 가죽','g','paw'),('늑대의 울음','B','paw'),('독수리의 눈','P:crit','eye'),('야생의 화신','D','paw')])],
 'cleric': [('보호', [('수호의 기도','G','cross'),('성스러운 방패','g','shield'),('대신 맞기','g','shield'),('피해 흡수 막','G','shield'),('불가침','P:def','shield')]),
            ('정화', [('해제','H','cross'),('축복','B','bell'),('안식','G','bell'),('순백의 종','H','bell'),('구원의 빛','r','star')]),
            ('응징', [('철퇴','d','fist'),('응징','d','fist'),('신벌','d','bolt'),('성스러운 낙인','w','star'),('심판의 종','D','bell')])],
 'knight': [('도발', [('도발','g','shield'),('방패 치기','d','shield'),('전열','G','shield'),('불굴의 외침','b','crown'),('요새','P:def','shield')]),
            ('수호', [('막아서기','g','shield'),('방어 태세','g','shield'),('반격 태세','d','sword'),('수호의 서약','G','crown'),('철벽','P:hp','heart')]),
            ('검술', [('베기','d','sword'),('돌격','D','sword'),('방패 돌진','Z','shield'),('정의의 칼날','c','sword'),('기사의 일격','c','crown')])],
 'summon': [('정령', [('불 정령','d','fire'),('물 정령','d','drop'),('바람 정령','D','swirl'),('대지 정령','d','burst'),('정령왕','D','crown')]),
            ('야수', [('늑대 소환','d','paw'),('곰 소환','g','paw'),('독수리 소환','D','wing'),('호박 유령 소환','d','ghost'),('용 소환','D','fire')]),
            ('계약', [('소환수 강화','P:mag','star'),('마력 연결','M','moon'),('합체 공격','c','burst'),('송환','H','ghost'),('계약의 폭주','B','burst')])],
 'gadget': [('포탑', [('소형 포탑','d','gear'),('보조 포탑','G','gear'),('레이저 포탑','d','bolt'),('포탑 증설','P:atk','fist'),('요새 포대','D','bomb')]),
            ('함정', [('덫 설치','s','gear'),('지뢰','d','bomb'),('전기 그물','S','bolt'),('연쇄 함정','D','gear'),('대지 폭파','D','burst')]),
            ('폭탄', [('수류탄','d','bomb'),('접착탄','s','bomb'),('연막탄','w','ghost'),('시한폭탄','c','bomb'),('집중 포화','D','bomb')])],
}
OV = {  # 같은 직업 안에서 그림이 겹치지 않게 이름별로 모양을 바꿔요
 'warrior': {'강타':'fist','대지 가르기':'rock','분노의 일격':'fire','되받아치기':'spear','파쇄':'hammer','폭풍 도끼':'cloud','회전 베기':'swirl','전장의 포효':'trumpet'},
 'black': {'화염구':'fireball','불씨':'ember','지옥불':'skull','메테오':'rock','서리 화살':'arrow','얼음 창':'spear','연쇄 번개':'chain','암흑 구체':'orb','공허의 손':'claw'},
 'thief': {'이중 베기':'cross2','칼춤':'swirl','연환':'chain','난도질':'claw','급소 찌르기':'arrow','피 웅덩이':'bubble','연막':'cloud','그림자 걸음':'ghost','훔치기':'coin','뒤잡기':'fist'},
 'bard': {'용기의 노래':'trumpet','승리의 행진':'flag','전장의 북소리':'drum','수호의 노래':'harp','자장가':'moon','되살림의 화음':'heart','불협화음':'note1','도발의 곡':'wave','앙코르':'burst','대합창':'bell'},
 'time': {'서두르기':'arrow','연속 가속':'chain','가속 영역':'wave','늦추기':'hourglass','시간 정체':'orb','되감기':'cross','시계 소환':'bell','시간 균열':'burst'},
 'alch': {'독 병':'tube','불안정 용액':'bubble','부식':'drop','응급 물약':'cross','마력 물약':'orb','혼합 약':'swirl','엘릭서':'star','변이약':'skull','점착 폭탄':'mine','연쇄 반응':'chain','연금 대폭발':'rocket'},
 'white': {'치유':'drop','큰 치유':'cross','집단 치유':'flower','신성한 비':'cloud','완전 소생':'crown','전체 소생':'orb','천사의 숨결':'wave','성광탄':'burst','빛의 장막':'shield','심판의 빛':'spear','광휘의 후광':'bell'},
 'druid': {'재생의 숲':'tree','뿌리 속박':'chain','생명의 나무':'flower','만개':'sun','독 제거':'cross','태양의 은총':'burst','가시 덩굴':'spear','늑대의 울음':'wave','야생의 화신':'claw'},
 'cleric': {'수호의 기도':'cross','성스러운 방패':'tower','대신 맞기':'orb','피해 흡수 막':'bubble','해제':'wave','축복':'sun','안식':'moon','순백의 종':'flag','철퇴':'hammer'},
 'knight': {'도발':'trumpet','방패 치기':'fist','전열':'chain','불굴의 외침':'flag','막아서기':'tower','방어 태세':'bubble','반격 태세':'spear','돌격':'arrow','정의의 칼날':'sun','기사의 일격':'burst'},
 'summon': {'대지 정령':'rock','곰 소환':'claw','용 소환':'fireball','마력 연결':'chain','송환':'orb','계약의 폭주':'skull'},
 'gadget': {'보조 포탑':'tower','요새 포대':'rocket','덫 설치':'chain','지뢰':'mine','전기 그물':'wave','연쇄 함정':'swirl','접착탄':'bubble','연막탄':'cloud','집중 포화':'arrow'},
}
ORDER = ['warrior','black','thief','bard','time','alch','white','druid','cleric','knight','summon','gadget']
BG = {'warrior':(196,74,74),'black':(110,66,170),'thief':(70,80,110),'bard':(214,130,60),'time':(60,140,160),'alch':(90,160,90),'white':(230,190,90),'druid':(70,130,70),'cleric':(150,160,200),'knight':(80,110,190),'summon':(150,70,140),'gadget':(140,110,80)}
O = (43,27,58,255); S = 28; G = 24
def glyph(g, d, fg, ac):
    P = lambda p, f=fg: d.polygon(p, fill=f, outline=O)
    if g == 'sword': P([(12,3),(15,14),(12,16),(9,14)]); d.rectangle([7,15,16,16], fill=ac, outline=O); d.rectangle([11,17,12,21], fill=O)
    elif g == 'axe': d.line([(8,20),(15,5)], fill=O, width=3); d.line([(8,20),(15,5)], fill=ac, width=1); P([(13,4),(20,6),(19,12),(15,10)])
    elif g == 'dagger': P([(12,3),(14,13),(12,15),(10,13)]); d.rectangle([8,14,15,15], fill=ac, outline=O); d.rectangle([11,16,12,20], fill=O)
    elif g == 'shield': P([(6,5),(18,5),(18,13),(12,20),(6,13)]); P([(9,8),(15,8),(15,12),(12,16),(9,12)], ac)
    elif g == 'fire': P([(12,3),(17,10),(18,15),(12,20),(6,15),(8,9),(11,12)]); P([(12,11),(15,15),(12,18),(9,15)], ac)
    elif g == 'ice':
        for a in range(3):
            r = math.radians(a*60); d.line([(12+8*math.cos(r),12+8*math.sin(r)),(12-8*math.cos(r),12-8*math.sin(r))], fill=fg, width=2)
        d.ellipse([10,10,13,13], fill=ac, outline=O)
    elif g == 'bolt': P([(14,2),(7,13),(11,13),(9,22),(17,10),(12,10)])
    elif g == 'star': P([(12,3),(14,10),(21,12),(14,14),(12,21),(10,14),(3,12),(10,10)])
    elif g == 'heart': P([(12,20),(4,11),(5,6),(9,5),(12,8),(15,5),(19,6),(20,11)])
    elif g == 'cross': P([(10,4),(14,4),(14,10),(20,10),(20,14),(14,14),(14,20),(10,20),(10,14),(4,14),(4,10),(10,10)])
    elif g == 'leaf': P([(5,19),(6,10),(13,4),(20,5),(19,13),(12,19)]); d.line([(7,18),(17,8)], fill=O, width=1)
    elif g == 'tree': d.rectangle([11,14,13,21], fill=O); P([(12,3),(19,13),(5,13)]); P([(12,8),(20,18),(4,18)], ac)
    elif g == 'drop': P([(12,3),(18,13),(17,18),(12,21),(7,18),(6,13)])
    elif g == 'skull': d.ellipse([5,4,19,16], fill=fg, outline=O); d.rectangle([8,14,16,19], fill=fg, outline=O); d.ellipse([8,9,11,12], fill=O); d.ellipse([13,9,16,12], fill=O)
    elif g == 'note': d.ellipse([5,15,11,21], fill=fg, outline=O); d.ellipse([13,13,19,19], fill=fg, outline=O); d.rectangle([10,5,11,18], fill=O); d.rectangle([18,3,19,16], fill=O); d.rectangle([10,4,19,7], fill=ac, outline=O)
    elif g == 'clock': d.ellipse([4,4,20,20], fill=fg, outline=O, width=2); d.line([(12,12),(12,7)], fill=O, width=2); d.line([(12,12),(16,14)], fill=O, width=2)
    elif g == 'flask': P([(10,3),(14,3),(14,10),(19,19),(17,21),(7,21),(5,19),(10,10)]); P([(7,16),(17,16),(19,19),(17,20),(7,20),(5,19)], ac)
    elif g == 'gear':
        for a in range(8):
            x, y = 12+8*math.cos(a*math.pi/4), 12+8*math.sin(a*math.pi/4); d.rectangle([x-2,y-2,x+2,y+2], fill=fg, outline=O)
        d.ellipse([5,5,19,19], fill=fg, outline=O); d.ellipse([10,10,14,14], fill=ac, outline=O)
    elif g == 'paw':
        d.ellipse([7,12,17,21], fill=fg, outline=O)
        for x, y in [(4,9),(8,4),(14,4),(18,9)]: d.ellipse([x,y,x+4,y+5], fill=fg, outline=O)
    elif g == 'eye': P([(2,12),(12,5),(22,12),(12,19)]); d.ellipse([8,8,16,16], fill=ac, outline=O); d.ellipse([11,11,13,13], fill=O)
    elif g == 'wing': P([(3,18),(5,8),(12,4),(20,5),(14,9),(19,11),(12,13),(16,17),(9,16)])
    elif g == 'fist': d.rounded_rectangle([5,7,19,19], 3, fill=fg, outline=O); [d.line([(x,7),(x,12)], fill=O) for x in (9,12,15)]
    elif g == 'bomb': d.ellipse([4,8,19,22], fill=O); d.ellipse([6,10,12,15], fill=fg); d.line([(15,9),(19,4)], fill=ac, width=2); d.ellipse([18,2,22,6], fill=ac, outline=O)
    elif g == 'bell': P([(12,3),(17,8),(18,16),(21,19),(3,19),(6,16),(7,8)]); d.ellipse([10,20,14,23], fill=O)
    elif g == 'moon': d.ellipse([4,4,20,20], fill=fg, outline=O); d.ellipse([9,2,24,17], fill=(0,0,0,0))
    elif g == 'sun':
        for a in range(8):
            r = math.radians(a*45); d.line([(12+6*math.cos(r),12+6*math.sin(r)),(12+10*math.cos(r),12+10*math.sin(r))], fill=O, width=3); d.line([(12+6*math.cos(r),12+6*math.sin(r)),(12+10*math.cos(r),12+10*math.sin(r))], fill=fg, width=1)
        d.ellipse([6,6,18,18], fill=fg, outline=O)
    elif g == 'swirl':
        pts = [(12+(1+t*.55)*math.cos(t), 12+(1+t*.55)*math.sin(t)) for t in [i*.3 for i in range(0,36)]]; d.line(pts, fill=O, width=4); d.line(pts, fill=fg, width=2)
    elif g == 'burst': P([(12,2),(14,8),(20,5),(17,11),(22,13),(16,15),(19,21),(12,17),(5,21),(8,15),(2,13),(7,11),(4,5),(10,8)]); d.ellipse([9,9,15,15], fill=ac, outline=O)
    elif g == 'up': P([(12,3),(20,12),(15,12),(15,21),(9,21),(9,12),(4,12)])
    elif g == 'crown': P([(4,18),(4,8),(8,12),(12,5),(16,12),(20,8),(20,18)]); d.rectangle([4,18,20,20], fill=ac, outline=O)
    elif g == 'ghost': P([(5,20),(5,10),(8,4),(16,4),(19,10),(19,20),(16,17),(12,20),(8,17)]); d.ellipse([8,9,10,12], fill=O); d.ellipse([14,9,16,12], fill=O)
    elif g == 'trumpet': P([(3,10),(14,10),(21,5),(21,19),(14,14),(3,14)]); d.rectangle([5,14,8,18], fill=ac, outline=O)
    elif g == 'flag': d.rectangle([5,3,6,21], fill=O); P([(7,4),(20,7),(7,13)])
    elif g == 'drum': d.ellipse([4,6,20,12], fill=fg, outline=O); d.rectangle([4,9,20,18], fill=ac, outline=O); d.ellipse([4,15,20,21], fill=ac, outline=O); d.line([(8,2),(13,8)], fill=O, width=2); d.line([(17,2),(12,8)], fill=O, width=2)
    elif g == 'harp': d.line([(6,20),(6,5),(18,10),(18,20)], fill=O, width=3); d.line([(6,20),(6,5),(18,10),(18,20)], fill=fg, width=1); [d.line([(x,7+(x-6)//4),(x,19)], fill=fg) for x in (9,12,15)]
    elif g == 'note1': d.ellipse([7,15,14,22], fill=fg, outline=O); d.rectangle([13,3,14,18], fill=O); P([(14,3),(20,8),(14,10)])
    elif g == 'wave':
        for i, rr in enumerate((3, 6, 9)): d.arc([12-rr, 12-rr, 12+rr, 12+rr], -50, 50, fill=O, width=3); d.arc([12-rr, 12-rr, 12+rr, 12+rr], -50, 50, fill=fg, width=1)
        d.ellipse([3,10,6,13], fill=fg, outline=O)
    elif g == 'tube': d.rounded_rectangle([9,3,15,21], 3, fill=fg, outline=O); d.rectangle([10,12,14,20], fill=ac); d.rectangle([8,2,16,4], fill=O)
    elif g == 'bubble': d.ellipse([3,8,15,20], fill=fg, outline=O); d.ellipse([13,3,21,11], fill=fg, outline=O); d.ellipse([6,11,9,14], fill=ac)
    elif g == 'mine': d.ellipse([6,9,18,21], fill=O); d.ellipse([8,11,12,15], fill=fg); [d.line([(12+8*math.cos(a*math.pi/3),15+8*math.sin(a*math.pi/3)),(12+5*math.cos(a*math.pi/3),15+5*math.sin(a*math.pi/3))], fill=O, width=2) for a in range(6)]; d.rectangle([11,3,12,9], fill=ac)
    elif g == 'rocket': P([(12,2),(17,9),(17,17),(7,17),(7,9)]); P([(7,13),(3,19),(7,18)], ac); P([(17,13),(21,19),(17,18)], ac); P([(10,17),(14,17),(12,22)], (255,150,60,255)); d.ellipse([10,7,14,11], fill=ac, outline=O)
    elif g == 'rock': P([(4,18),(7,8),(14,4),(20,10),(21,18)]); d.line([(10,8),(12,14),(17,12)], fill=O)
    elif g == 'hammer': d.rectangle([11,9,13,21], fill=O); d.rectangle([12,9,12,21], fill=ac); P([(4,4),(20,4),(20,11),(4,11)])
    elif g == 'spear': d.line([(5,21),(17,7)], fill=O, width=3); d.line([(5,21),(17,7)], fill=ac, width=1); P([(15,3),(21,3),(21,9),(18,9)])
    elif g == 'arrow': d.line([(4,20),(18,6)], fill=O, width=3); d.line([(4,20),(18,6)], fill=fg, width=1); P([(14,3),(21,3),(21,10)]); P([(3,16),(8,21),(3,21)], ac)
    elif g == 'claw':
        for x in (6,11,16): P([(x,3),(x+4,9),(x+3,20),(x-1,12)])
    elif g == 'cloud': d.ellipse([3,10,12,19], fill=fg, outline=O); d.ellipse([8,5,18,16], fill=fg, outline=O); d.ellipse([13,10,22,19], fill=fg, outline=O); d.rectangle([7,13,17,18], fill=fg)
    elif g == 'orb': d.ellipse([4,4,20,20], fill=fg, outline=O, width=2); d.ellipse([8,7,12,11], fill=(255,255,255,255)); d.ellipse([13,13,18,18], fill=ac)
    elif g == 'ember': P([(12,6),(16,13),(12,19),(8,13)]); d.rectangle([6,4,7,5], fill=ac); d.rectangle([17,3,18,4], fill=ac); d.rectangle([4,18,5,19], fill=ac)
    elif g == 'fireball': d.ellipse([9,9,21,21], fill=fg, outline=O); d.ellipse([12,12,18,18], fill=ac); P([(10,12),(2,3),(7,14)], (255,150,60,255)); P([(12,10),(6,2),(14,9)], (255,150,60,255))
    elif g == 'hourglass': P([(6,3),(18,3),(18,6),(13,12),(18,18),(18,21),(6,21),(6,18),(11,12),(6,6)]); d.rectangle([9,17,15,20], fill=ac)
    elif g == 'flower':
        for a in range(5): r = math.radians(a*72-90); d.ellipse([12+6*math.cos(r)-4, 12+6*math.sin(r)-4, 12+6*math.cos(r)+4, 12+6*math.sin(r)+4], fill=fg, outline=O)
        d.ellipse([9,9,15,15], fill=ac, outline=O)
    elif g == 'chain': d.ellipse([3,8,13,16], outline=O, width=3); d.ellipse([11,8,21,16], outline=O, width=3); d.ellipse([3,8,13,16], outline=fg, width=1); d.ellipse([11,8,21,16], outline=fg, width=1)
    elif g == 'coin': d.ellipse([4,4,20,20], fill=ac, outline=O, width=2); d.rectangle([11,8,13,16], fill=O)
    elif g == 'tower': P([(5,4),(19,4),(19,15),(12,21),(5,15)]); d.rectangle([5,4,19,6], fill=ac, outline=O); d.line([(12,6),(12,19)], fill=O)
    elif g == 'cross2': P([(5,3),(8,3),(21,17),(18,20)]); P([(19,3),(16,3),(3,17),(6,20)])
PK = {'def':'shield','hp':'heart','atk':'fist','mag':'star','spd':'wing','vamp':'drop','crit':'eye'}
VAR = [(0,0),(1,0),(0,25),(1,25),(0,-25),(1,-25),(0,50),(1,50),(0,-50),(1,-50)]   # (좌우 뒤집기, 기울기) — 같은 모양이 겹치면 돌려서 구분
def mod(d, code, ac):   # 오른쪽 아래 작은 표시: 스킬 종류
    X, Y = 21, 19; d.ellipse([X-6, Y-6, X+6, Y+6], fill=O); k = code[0]
    W = (250,245,235,255); G = (120,230,140,255); Bl = (130,190,255,255); Pu = (210,150,255,255); Or = (255,150,70,255)
    def up(c): d.polygon([(X,Y-4),(X+4,Y),(X+1,Y),(X+1,Y+4),(X-1,Y+4),(X-1,Y),(X-4,Y)], fill=c)
    def dn(c): d.polygon([(X,Y+4),(X+4,Y),(X+1,Y),(X+1,Y-4),(X-1,Y-4),(X-1,Y),(X-4,Y)], fill=c)
    def plus(c): d.rectangle([X-1,Y-4,X+1,Y+4], fill=c); d.rectangle([X-4,Y-1,X+4,Y+1], fill=c)
    def dots(c): [d.rectangle([X+dx-1,Y+dy-1,X+dx,Y+dy], fill=c) for dx,dy in ((-3,2),(3,2),(0,-3))]
    if code.startswith('P:'): d.ellipse([X-3,Y-3,X+3,Y+3], outline=ac)
    elif k == 'd': d.polygon([(X,Y-4),(X+1,Y-1),(X+4,Y),(X+1,Y+1),(X,Y+4),(X-1,Y+1),(X-4,Y),(X-1,Y-1)], fill=W)
    elif k == 'D': dots(W)
    elif k == 'c': d.arc([X-4,Y-4,X+4,Y+4], 40, 330, fill=ac, width=2); d.rectangle([X,Y-1,X+3,Y], fill=ac)
    elif k == 'h': plus(G)
    elif k == 'H': plus(G); d.ellipse([X-5,Y-5,X+5,Y+5], outline=G)
    elif k == 'r': plus(W); d.rectangle([X-1,Y-5,X+1,Y-4], fill=ac)
    elif k in 'Bb': up(ac) if k == 'B' else up(Bl)
    elif k in 'Gg': d.polygon([(X-4,Y-4),(X+4,Y-4),(X+4,Y),(X,Y+5),(X-4,Y)], fill=Bl if k == 'G' else W)
    elif k in 'Xx': d.polygon([(X-4,Y+3),(X-2,Y-3),(X+4,Y-4),(X+1,Y),(X+3,Y+2)], fill=Bl if k == 'X' else W)
    elif k in 'Ss': dn(Bl) if k == 'S' else dn(W)
    elif k in 'Ww': dn(Pu)
    elif k in 'Ff': d.polygon([(X,Y-4),(X+3,Y+1),(X,Y+4),(X-3,Y+1)], fill=Or)
    elif k == 'Z': d.polygon([(X+1,Y-4),(X-3,Y+1),(X,Y+1),(X-1,Y+4),(X+3,Y-1),(X,Y-1)], fill=ac)
    elif k == 'M': d.ellipse([X-3,Y-3,X+3,Y+3], fill=Bl)
def tile(job, b, r, code, g, v):
    bg = BG[job]; k = (0, 28, -22)[b]; bg = tuple(max(0, min(255, c + k)) for c in bg)
    fg = (250,245,235,255); ac = (255,214,102,255)
    im = Image.new('RGBA', (S, S), (0,0,0,0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,S-1,S-1], 5, fill=O); d.rounded_rectangle([2,2,S-3,S-3], 4, fill=bg+(255,))
    if code.startswith('P:'): d.rounded_rectangle([1,1,S-2,S-2], 5, outline=ac, width=1)
    g2 = Image.new('RGBA', (G, G), (0,0,0,0)); glyph(PK[code[2:]] if code.startswith('P:') else g, ImageDraw.Draw(g2), fg, ac)
    fl, ang = VAR[v % len(VAR)]
    if fl: g2 = g2.transpose(Image.FLIP_LEFT_RIGHT)
    if ang: g2 = g2.rotate(ang, resample=Image.NEAREST)
    im.alpha_composite(g2, (2,0))
    for i in range(r+1): d.rectangle([4+i*4, 25, 6+i*4, 25], fill=ac)
    mod(d, code, ac)
    return im
sheet = Image.new('RGBA', (S*15, S*12))
seen = set()
for ji, job in enumerate(ORDER):
    cnt = {}
    for b, (bn, sks) in enumerate(T[job]):
        for r, (n, code, g) in enumerate(sks):
            g = OV.get(job, {}).get(n, g); gg = PK[code[2:]] if code.startswith('P:') else g; v = cnt.get(gg, 0); cnt[gg] = v + 1
            while True:   # 모든 아이콘이 서로 다르도록: 같은 그림이면 변형을 바꿔요
                im = tile(job, b, r, code, g, v); key = (job, b, r, im.tobytes())
                if all(k[3] != key[3] or k[0] != job for k in seen) : break
                v += 1
            seen.add(key); sheet.paste(im, ((b*5+r)*S, ji*S))
sheet.resize((S*15*2, S*12*2), Image.NEAREST).save('public/art/skills.png', optimize=True)
xt = {j: [[bn, [[n, c] for n, c, g in sks]] for bn, sks in T[j]] for j in ORDER}
js = 'const XT = ' + json.dumps(xt, ensure_ascii=False, separators=(',', ':')) + ';'
p = 'public/index.html'; s = open(p, encoding='utf-8').read()
if '/*XT*/' in s: s = re.sub(r'/\*XT\*/.*?/\*XT-END\*/', lambda m: '/*XT*/' + js + '/*XT-END*/', s, flags=re.S)
else: s = s.replace('const xRand = a =>', '/*XT*/' + js + '/*XT-END*/\nconst xRand = a =>', 1)
open(p, 'w', encoding='utf-8').write(s)
