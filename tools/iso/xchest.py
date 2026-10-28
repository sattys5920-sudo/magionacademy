from PIL import Image
import sys
OUT=sys.argv[1]
O=(26,16,36,255)          # 외곽선
W1,W2,W3,W4=(186,124,70,255),(158,100,56,255),(126,78,42,255),(96,56,30,255)   # 나무 밝음→어둠
I1,I2,I3=(122,122,150,255),(84,84,108,255),(58,58,78,255)   # 쇠띠
G1,G2,G3=(255,240,168,255),(255,214,92,255),(206,150,46,255) # 금
L1,L2=(255,250,214,255),(255,232,140,255)
IN=(46,26,40,255)          # 안쪽 어둠
def canvas(w=40,h=40): return Image.new('RGBA',(w,h),(0,0,0,0))
def px(im,x,y,c):
    if 0<=x<im.width and 0<=y<im.height: im.putpixel((x,y),c)
def rect(im,x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1): px(im,x,y,c)
def shadow(im,cx,y,rx):
    for x in range(cx-rx,cx+rx+1):
        d=abs(x-cx)/rx
        a=int(90*(1-d*d))
        if a>0: px(im,x,y,(10,6,20,a)); px(im,x,y+1,(10,6,20,a//2))
def body(im,x0,y0,x1,y1):
    # 몸통: 가로 판자 + 쇠띠 + 금 자물쇠
    rect(im,x0,y0,x1,y1,O)
    for y in range(y0+1,y1):
        k=(y-y0-1)%4
        c=[W2,W2,W3,W4][k]
        rect(im,x0+1,y,x1-1,y,c)
    rect(im,x0+1,y0+1,x1-1,y0+1,W1)                # 윗면 빛
    rect(im,x0+1,y1-1,x1-1,y1-1,W4)
    for bx in (x0+5,x1-6):                          # 쇠띠
        rect(im,bx,y0+1,bx+1,y1-1,I2); rect(im,bx,y0+1,bx,y1-1,I1); rect(im,bx+1,y1-2,bx+1,y1-1,I3)
        for ry in range(y0+3,y1-1,4): px(im,bx,ry,G2); px(im,bx+1,ry,G3)   # 리벳
    # 모서리 금장
    for (cx,cy,dx,dy) in ((x0+1,y1-1,1,-1),(x1-1,y1-1,-1,-1)):
        px(im,cx,cy,G2); px(im,cx+dx,cy,G3); px(im,cx,cy+dy,G3)
def lock(im,cx,y):
    rect(im,cx-3,y,cx+2,y+6,O); rect(im,cx-2,y+1,cx+1,y+5,G2); rect(im,cx-2,y+1,cx+1,y+1,G1); rect(im,cx-2,y+5,cx+1,y+5,G3)
    px(im,cx-1,y+3,O); px(im,cx,y+3,O); px(im,cx-1,y+4,O)   # 열쇠 구멍
def closed():
    im=canvas(); x0,x1=4,35
    shadow(im,20,37,15)
    # 둥근 뚜껑
    top=8
    prof={0:5,1:3,2:2,3:1,4:1}
    for y in range(top,top+9):
        inset=prof.get(y-top,0)
        rect(im,x0+inset,y,x1-inset,y,O if y==top else W2)
        px(im,x0+inset,y,O); px(im,x1-inset,y,O)
    for y in range(top+1,top+9):
        inset=prof.get(y-top,0)
        c=W1 if y<=top+2 else (W2 if y<top+6 else W3)
        rect(im,x0+inset+1,y,x1-inset-1,y,c)
    rect(im,x0+4,top+1,x0+10,top+1,L2)             # 뚜껑 반짝
    for bx in (x0+5,x1-6):
        for y in range(top+1,top+9): px(im,bx,y,I1 if y<top+4 else I2); px(im,bx+1,y,I2 if y<top+6 else I3)
    rect(im,19,top+1,20,top+8,G2); rect(im,19,top+1,19,top+8,G1)  # 가운데 금띠
    rect(im,x0,top+9,x1,top+10,O); rect(im,x0+1,top+9,x1-1,top+9,G3); rect(im,x0+1,top+10,x1-1,top+10,(70,40,22,255))  # 뚜껑 이음
    body(im,x0,top+11,x1,top+26)
    rect(im,19,top+11,20,top+25,G2); rect(im,19,top+11,19,top+25,G1)
    lock(im,20,top+8)
    return im
def opened(glow):
    im=canvas(); x0,x1=4,35
    shadow(im,20,37,15)
    top=19
    # 뒤로 젖힌 뚜껑 (안쪽 면이 보여요)
    lt=6
    rect(im,x0+1,lt,x1-1,lt+7,O)
    rect(im,x0+2,lt+1,x1-2,lt+2,W3); rect(im,x0+2,lt+3,x1-2,lt+6,(78,44,26,255))
    for bx in (x0+6,x1-7): rect(im,bx,lt+1,bx+1,lt+6,I3)
    rect(im,x0+2,lt+1,x1-2,lt+1,W2)
    # 안쪽
    rect(im,x0,top-5,x1,top,O)
    if glow:
        rect(im,x0+1,top-4,x1-1,top,L2); rect(im,x0+3,top-4,x1-3,top-3,L1)
        for (gx,gy) in ((9,top-2),(14,top-3),(22,top-2),(27,top-3),(18,top-1)): rect(im,gx,gy,gx+2,gy+1,G2); px(im,gx,gy,G1)
    else:
        rect(im,x0+1,top-4,x1-1,top,IN); rect(im,x0+1,top-4,x1-1,top-4,(70,50,90,255))
        for (gx,gy) in ((10,top-2),(23,top-2)): rect(im,gx,gy,gx+2,gy+1,(120,100,150,255))
    if glow:   # 안에서 솟는 빛줄기 (아래가 밝고 위로 흐려져요)
        for (bx,w,a) in ((11,2,150),(17,4,200),(25,2,150),(7,1,90),(31,1,90)):
            for y in range(0,top-4):
                fa=int(a*(.3+.7*(y/(top-4))))
                for x in range(bx,bx+w):
                    r,g,b,al=im.getpixel((x,y)); k=fa/255
                    if al==0: px(im,x,y,(255,240,170,fa))
                    else: px(im,x,y,(int(r+(255-r)*k*.8),int(g+(240-g)*k*.8),int(b+(170-b)*k*.8),255))
    rect(im,x0,top+1,x1,top+2,O); rect(im,x0+1,top+1,x1-1,top+1,G3)
    body(im,x0,top+3,x1,top+16)
    rect(im,19,top+3,20,top+15,G2); rect(im,19,top+3,19,top+15,G1)
    lock(im,20,top+1)
    if glow:   # 반짝이
        for (sx,sy) in ((6,4),(33,9),(15,1),(36,15),(3,12)):
            px(im,sx,sy,L1); px(im,sx-1,sy,L2); px(im,sx+1,sy,L2); px(im,sx,sy-1,L2); px(im,sx,sy+1,L2)
    return im
closed().save(OUT+'/chest_closed.png'); opened(True).save(OUT+'/chest_open.png'); opened(False).save(OUT+'/chest_open_dim.png')
prev=Image.new('RGBA',(140,48),(27,20,48,255))
for i,n in enumerate(['chest_closed','chest_open','chest_open_dim']):
    a=Image.open(OUT+f'/{n}.png'); prev.paste(a,(4+i*46,4),a)
prev.resize((prev.width*6,prev.height*6),Image.NEAREST).save(OUT+'/preview.png')
