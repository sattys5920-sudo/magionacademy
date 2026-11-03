import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/kr')
from kr import *
C=all_minis()
C['heart_s']=knit((['.1.1........','11111.......','11111.......','.111........','..1.........']+['............']*7,'#F06A8A','#FFFFFF'),'#F06A8A','#FFFFFF')
SC=len(sys.argv)>1
from PIL import ImageFont
FT=ImageFont.truetype(S+'/g11b.ttf',22)
sh=Image.open('public/art/npcs.webp').convert('RGBA')
# (spr 줄, 이름, 다는 곳 설명, 고리 위치(64 칸 안), 키링)
L=[(1,'배트리','편지 가방',(41,45),'bat'),(0,'나비','꼬리',(43,41),'heart'),(4,'맨디','머리 위 잎',(46,31),'mush'),(13,'오투모','귀 안테나',(48,29),'star'),
   (2,'캇파','낚싯대 끝',(19,21),'fish'),(5,'스트로','모자 챙',(46,26),'pumpkin'),(3,'아울라','들고 있는 책',(40,47),'owl'),('sera','세라 선생님','허리띠',(38,47),'clover'),('madeleine','마들렌','앞치마 허리',(38,47),'berry'),('stella','스텔라','허리띠',(38,47),'moon'),('leo','레오','허리띠',(38,47),'rabbit')]
Z=5; W=len(L)*64*Z//1
Z=4; out=Image.new('RGBA',(6*(64*Z+20)+20,2*(64*Z+80)),hx('#241A38')); d=ImageDraw.Draw(out)
for i,(r,nm,where,(ax,ay),ck) in enumerate(L):
    fr=(Image.open(S+f'/av_{r}.png').convert('RGBA').crop((0,0,64,64)) if isinstance(r,str) else Image.open(S+f'/sc_{r}.png').convert('RGBA').crop((0,0,64,64)) if SC else sh.crop((0,r*64,64,r*64+64))).copy()
    c=C[ck]; fr.alpha_composite(c,(ax-7,ay-1))
    x0=20+(i%6)*(64*Z+20); y0=(i//6)*(64*Z+80)
    d.rounded_rectangle([x0-6,y0+14,x0+64*Z+6,y0+64*Z+26],16,fill=hx('#33285A'))
    out.alpha_composite(fr.resize((64*Z,64*Z),Image.NEAREST),(x0,y0+20))
    d.text((x0+10,y0+64*Z+36),f"{nm} · {where}",fill=hx('#FFE9A0'),font=FT)
out.save(S+'/npc_kr.png'); print(out.size)
# 키링 12 종 (작은 것 · 실제 크기 × 8)
M=all_minis(); Zm=8
sheet=Image.new('RGBA',(10*(14*Zm+16)+16,2*(20*Zm+70)),hx('#241A38')); d2=ImageDraw.Draw(sheet)
NM={'pumpkin':'호박','ghost':'유령','star':'별','heart':'하트','moon':'달','cat':'고양이','owl':'부엉이','mush':'버섯','bat':'박쥐','fish':'물고기','snowman':'눈사람','hat':'마녀 모자','clover':'클로버','berry':'딸기','rabbit':'토끼','bear':'곰','cloud':'구름','daisy':'데이지','acorn':'도토리','duck':'오리'}
for i,(k,c) in enumerate([(k,v) for k,v in M.items() if k in NM]):
    x=16+(i%10)*(14*Zm+16); y0=(i//10)*(20*Zm+70); d2.rounded_rectangle([x-4,y0+12,x+14*Zm+4,y0+20*Zm+20],12,fill=hx('#33285A')); sheet.alpha_composite(c.resize((14*Zm,20*Zm),Image.NEAREST),(x,y0+16)); d2.text((x+8,y0+20*Zm+30),NM[k],fill=hx('#FFE9A0'),font=FT)
sheet.save(S+'/charms_mini.png')
both=Image.new('RGBA',(max(sheet.width,out.width),sheet.height+out.height),hx('#241A38')); both.alpha_composite(sheet,(0,0)); both.alpha_composite(out,(0,sheet.height)); both.save(S+('/keyring_scarf.png' if SC else '/keyring_mock.png')); print(both.size)
