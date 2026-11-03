import sys,json; sys.path.insert(0,'/tmp/claude-0/-home-user/d683bb50-b1f3-59a3-8e5f-5f21e64e8c5a/scratchpad/kr')
from kr import *
from PIL import ImageFont
M=all_minis(); FT=ImageFont.truetype(S+'/g11b.ttf',14)
sh=Image.open('public/art/npcs.webp').convert('RGBA')
FRONT={'batri':(1,(41,45)),'nabi':(0,(43,41)),'mandi':(4,(46,31)),'otumo':(13,(48,29)),'kappa':(2,(19,21)),'jipsin':(5,(46,26)),'aula':(3,(40,47)),'sera':('sera',(38,47)),'madeleine':('madeleine',(38,47)),'stella':('stella',(38,47)),'leo':('leo',(38,47))}
OVR=json.load(open(S+'/ovr.json')) if __import__('os').path.exists(S+'/ovr.json') else {}
def bbox(fr): return fr.getbbox()
def anchors(nm):
    r,(ax,ay)=FRONT[nm]; src=Image.open(f'{S}/av_{r}.png').convert('RGBA') if isinstance(r,str) else sh.crop((0,r*64,1280,r*64+64))
    f=src.crop((0,0,64,64)); x0,y0,x1,y1=bbox(f); fx=(ax-x0)/(x1-x0); fy=(ay-y0)/(y1-y0); A={}
    MIR={'nabi':{5:1,10:0,15:1},'kappa':{5:0,10:0,15:1}}.get(nm,{5:1,10:1,15:0})
    FXS={'otumo':{10:.9,15:.1}}.get(nm,{})
    for col in (0,5,10,15):
        mir=MIR.get(col,0); g=src.crop((col*64,0,col*64+64,64)); b=bbox(g); ff=FXS.get(col,(1-fx) if mir else fx); X=b[0]+ff*(b[2]-b[0]); Y=b[1]+fy*(b[3]-b[1])
        A[col]=[round(X),round(Y)]
    A[0]=[ax,ay]
    for k,v in OVR.get(nm,{}).items(): A[int(k)]=v
    return src,A
if __name__=='__main__':
    keys=list(M.keys()); Z=3; ALL={}
    out=Image.new('RGBA',(4*64*Z+70,len(FRONT)*64*Z),(30,24,48,255)); d=ImageDraw.Draw(out)
    for i,nm in enumerate(FRONT):
        src,A=anchors(nm); ALL[nm]=A
        for j,col in enumerate([0,5,10,15]):
            fr=src.crop((col*64,0,col*64+64,64)).copy(); ax,ay=A[col]; fr.alpha_composite(M[keys[i]],(ax-7,ay-1))
            out.alpha_composite(fr.resize((64*Z,64*Z),Image.NEAREST),(70+j*64*Z,i*64*Z))
        d.text((4,i*64*Z+8),nm,fill=(255,233,160,255),font=FT)
    out.save(S+'/dirs_kr.png'); json.dump(ALL,open(S+'/anchors.json','w')); print(out.size)
