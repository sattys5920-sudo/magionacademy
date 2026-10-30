// 꿈나라: 쉬는 동안 하루 한 번 꾸는 꿈 미니게임 12종 (밤잠 12종 · 낮잠 6종). index.html에서 Dream.run(opt) · Dream.thumb(이름, 캔버스)
// 그림은 모두 코드로 그리는 도트 (130×281 칸을 화면에 맞춰 키워요) · 시안: tools/dream_mock
(function(){
const W=130,H=281;
const R=(g,x,y,w,h,c)=>{g.fillStyle=c;g.fillRect(x|0,y|0,w|0,h|0);};
const P=(g,pts,c)=>{g.fillStyle=c;pts.forEach(([x,y])=>g.fillRect(x,y,1,1));};
const disc=(g,cx,cy,r,c)=>{g.fillStyle=c;for(let y=-r;y<=r;y++)for(let x=-r;x<=r;x++)if(x*x+y*y<=r*r+r*.6)g.fillRect(cx+x,cy+y,1,1);};
const ell=(g,cx,cy,rx,ry,c)=>{g.fillStyle=c;for(let y=-ry;y<=ry;y++)for(let x=-rx;x<=rx;x++)if((x*x)/(rx*rx)+(y*y)/(ry*ry)<=1.05)g.fillRect(cx+x,cy+y,1,1);};
const grad=(g,top,bot)=>{for(let y=0;y<H;y++){const t=y/H,a=top.map((v,i)=>Math.round(v+(bot[i]-v)*t));R(g,0,y,W,1,`rgb(${a})`);}};
const star=(g,x,y,c='#FFE070',h='#FFF8C8')=>{P(g,[[x,y-2],[x,y-1],[x-2,y],[x-1,y],[x,y],[x+1,y],[x+2,y],[x,y+1],[x,y+2]],c);P(g,[[x,y]],h);};
const shard=(g,x,y)=>{ // 꿈 조각: 반짝이는 보라 별사탕
 P(g,[[x,y-3],[x-1,y-2],[x,y-2],[x+1,y-2],[x-3,y-1],[x-2,y-1],[x-1,y-1],[x,y-1],[x+1,y-1],[x+2,y-1],[x+3,y-1],[x-2,y],[x-1,y],[x,y],[x+1,y],[x+2,y],[x-2,y+1],[x-1,y+1],[x+1,y+1],[x+2,y+1],[x-3,y+2],[x+3,y+2]],'#C890FF');
 P(g,[[x-1,y-1],[x,y-2]],'#F4E4FF');P(g,[[x+1,y],[x+2,y+1]],'#8A60D0');};
const cloud=(g,x,y,w,c='#FFFFFF',s='#D8E4FF')=>{ell(g,x+w/2,y+3,w/2,3,s);ell(g,x+w/2,y+1,w/2,3,c);disc(g,x+w*.3,y-1,3,c);disc(g,x+w*.62,y-2,4,c);};
// 학생(작은 도트): 빨간 머리, 망토
function kid(g,x,y,pose='stand',cap='#5A3496'){
 R(g,x-3,y-12,7,6,'#F6D2B0');R(g,x-4,y-14,9,3,'#D8482E');R(g,x-4,y-12,2,3,'#D8482E');R(g,x+3,y-12,2,2,'#D8482E');
 P(g,[[x-1,y-9],[x+2,y-9]],'#2A1E3A');P(g,[[x-2,y-7],[x+3,y-7]],'#F4A0A0');
 R(g,x-3,y-6,7,5,cap);R(g,x-1,y-6,3,4,'#F4F0E8');
 if(pose==='jump'){R(g,x-5,y-8,2,3,cap);R(g,x+4,y-8,2,3,cap);R(g,x-3,y-1,2,2,'#3A2E50');R(g,x+2,y-1,2,3,'#3A2E50');}
 else {R(g,x-2,y-1,2,2,'#3A2E50');R(g,x+1,y-1,2,2,'#3A2E50');}
}
function sleepy(g,x,y){ // 잠옷 + 수면모자 + 이불
 R(g,x-12,y,26,8,'#7A9CE8');R(g,x-12,y,26,2,'#A8C0F8');P(g,[[x-9,y+4],[x-3,y+3],[x+4,y+5],[x+9,y+3]],'#FFE070');
 R(g,x-14,y-6,9,6,'#F4F0E8');
 R(g,x-12,y-8,7,6,'#F6D2B0');P(g,[[x-10,y-5],[x-7,y-5]],'#2A1E3A');R(g,x-13,y-10,9,3,'#5A7AD8');P(g,[[x-4,y-11],[x-3,y-12],[x-2,y-12]],'#5A7AD8');P(g,[[x-1,y-12]],'#FFFFFF');
 P(g,[[x-9,y-3],[x-8,y-3]],'#C86A6A');
}
const D = {};
D.jump=g=>{
 grad(g,[120,150,240],[255,200,225]);
 for(let i=0;i<14;i++)P(g,[[(i*29)%W,(i*41)%120]],'#FFFFFF');
 disc(g,104,40,9,'#FFF0B0');disc(g,104,40,7,'#FFF8D8');
 [[10,230,30],[70,205,26],[30,170,24],[84,140,22],[22,108,22],[70,80,24],[40,50,20]].forEach(([x,y,w],i)=>cloud(g,x,y,w,i===3?'#FFE4F0':'#FFFFFF',i===3?'#F8B8D0':'#D8E4FF'));
 // 솜사탕 스프링 구름
 cloud(g,84,140,22,'#FFD0E8','#F0A0C8');P(g,[[92,135],[93,134],[94,135],[95,134],[96,135]],'#FF80B0');
 kid(g,62,190,'jump');P(g,[[58,193],[60,195],[64,195],[66,193]],'#FFFFFF');
 shard(g,36,160);shard(g,95,128);shard(g,30,96);shard(g,80,70);
 // 박쥐 방해꾼
 P(g,[[40,120],[41,121],[42,121],[43,122],[44,121],[45,121],[46,120],[42,122],[44,122]],'#3A2E50');P(g,[[42,121],[44,121]],'#FF6060');

};
D.candy=g=>{
 grad(g,[255,214,232],[255,240,210]);
 // 과자 집·사탕 나무 배경
 for(let i=0;i<6;i++){const x=i*24-4;R(g,x,170,22,40,i%2?'#C88A5A':'#D8A070');R(g,x,166,22,5,'#FFFFFF');P(g,[[x+3,170],[x+8,171],[x+14,170],[x+19,171]],'#FFFFFF');R(g,x+8,190,6,20,'#7A4A2A');P(g,[[x+5,178],[x+16,178]],'#FFE070');}
 [[16,150],[60,140],[104,152]].forEach(([x,y])=>{R(g,x,y,2,30,'#FFFFFF');disc(g,x+1,y-2,6,'#FF80B0');ell(g,x+1,y-2,3,3,'#FFB8D8');P(g,[[x-2,y-4],[x+3,y]],'#FFFFFF');});
 R(g,0,210,W,H-210,'#F8C8A0');for(let x=0;x<W;x+=8)R(g,x+((x/8)%2)*4,214,4,2,'#FFFFFF');
 // 떨어지는 과자들
 const donut=(x,y)=>{disc(g,x,y,4,'#E8A060');disc(g,x,y,3,'#FF90C0');disc(g,x,y,1,'#F8C8A0');P(g,[[x-2,y-1],[x+1,y-2],[x+2,y+1]],'#FFFFFF');};
 const candy=(x,y)=>{disc(g,x,y,3,'#80D0FF');P(g,[[x-1,y-1],[x+1,y+1]],'#FFFFFF');P(g,[[x-5,y-1],[x-4,y],[x-5,y+1],[x+5,y-1],[x+4,y],[x+5,y+1]],'#80D0FF');};
 const cookie=(x,y)=>{disc(g,x,y,4,'#D8A060');P(g,[[x-2,y-1],[x+1,y-2],[x+2,y+1],[x-1,y+2]],'#6A3A1A');};
 const broc=(x,y)=>{R(g,x-1,y,3,4,'#7AB850');disc(g,x-2,y-2,2,'#3A8A30');disc(g,x+2,y-2,2,'#3A8A30');disc(g,x,y-4,2,'#4A9A38');P(g,[[x-1,y-3],[x+1,y-3]],'#2A1E3A');};
 donut(30,70);candy(80,100);cookie(56,130);broc(104,60);candy(20,140);shard(g,70,50);donut(100,150);
 // 바구니 든 학생
 kid(g,62,240);R(g,57,216,2,10,'#F6D2B0');R(g,66,216,2,10,'#F6D2B0');R(g,51,210,24,8,'#C88A3A');R(g,51,210,24,2,'#E8B060');for(let x=53;x<74;x+=3)R(g,x,212,1,6,'#A06A2A');
 P(g,[[60,207],[62,206],[66,207]],'#FF90C0');
 // +1 표시
 g.fillStyle='#7A48C8';g.font='7px monospace';

};
D.sea=g=>{
 // 위가 바다 바닥(모래·산호가 하늘에), 아래가 하늘
 grad(g,[30,70,140],[120,200,240]);
 R(g,0,0,W,26,'#E8D090');for(let x=0;x<W;x+=6)P(g,[[x,25],[x+3,26]],'#C8B070');
 // 거꾸로 산호 (위에서 아래로)
 const coral=(x,len,c,h)=>{R(g,x,26,4,len,c);R(g,x-4,26+len*.4,4,3,c);R(g,x-4,26+len*.4,2,len*.3,c);R(g,x+4,26+len*.6,4,3,c);R(g,x+6,26+len*.6,2,len*.25,c);P(g,[[x+1,26+len-1],[x+2,26+len-2]],h);};
 coral(24,60,'#FF7A90','#FFC0CC');coral(92,40,'#B880F0','#E8D0FF');
 // 아래쪽에서 올라오는 해초 기둥 (하늘에서 거꾸로?) → 구름 섬
 cloud(g,80,200,30);cloud(g,10,236,34);
 R(g,94,150,4,50,'#3A9A70');R(g,90,170,4,3,'#3A9A70');R(g,98,160,4,3,'#3A9A70');
 // 거꾸로 헤엄치는 물고기·고래
 const fish=(x,y,c,flip)=>{ell(g,x,y,5,3,c);P(g,flip?[[x+5,y-2],[x+6,y-3],[x+5,y+2],[x+6,y+3],[x+6,y]]:[[x-5,y-2],[x-6,y-3],[x-5,y+2],[x-6,y+3],[x-6,y]],c);P(g,[[flip?x-3:x+3,y-1]],'#2A1E3A');};
 fish(100,110,'#FFB040',true);fish(30,190,'#80E0C0');fish(60,240,'#FF90C0',true);
 // 고래가 하늘을 날아요
 ell(g,30,120,14,7,'#5A80D8');ell(g,30,123,12,4,'#C8DCFF');P(g,[[42,119],[43,118]],'#2A1E3A');P(g,[[16,115],[15,114],[14,113],[16,125],[15,126],[14,127]],'#5A80D8');P(g,[[30,111],[29,109],[31,109],[28,108],[32,108]],'#C8F0FF');
 // 물방울
 [[70,70],[76,62],[66,56],[110,80],[48,160]].forEach(([x,y])=>{disc(g,x,y,2,'rgba(220,245,255,.8)');P(g,[[x-1,y-1]],'#FFFFFF');});
 // 물방울 헬멧 쓴 학생 (거꾸로 매달린 느낌으로 살짝 기울게)
 disc(g,62,150,9,'rgba(200,240,255,.35)');kid(g,62,158,'jump','#2A6AB8');P(g,[[56,144],[57,143]],'#FFFFFF');
 shard(g,86,132);shard(g,40,90);shard(g,104,200);

};
// 새 꿈 9종
const sheep=(g,x,y,f)=>{ell(g,x,y,7,5,'#FFFFFF');disc(g,x-4,y-3,3,'#FFFFFF');disc(g,x+3,y-4,3,'#FFFFFF');ell(g,x+7,y-1,3,3,'#4A3A5A');P(g,[[x+8,y-2]],'#FFFFFF');R(g,x-4,y+4,2,f?2:4,'#4A3A5A');R(g,x+3,y+4,2,f?4:2,'#4A3A5A');P(g,[[x+9,y],[x+8,y+1]],'#F4A0A0');};
D.stars=g=>{ // 4 별똥별 줍기
 grad(g,[14,10,40],[50,36,100]);for(let i=0;i<60;i++)P(g,[[(i*37)%W,(i*53)%220]],i%4?'#8A7AC8':'#FFF8C8');
 const fall=(x,y,c)=>{for(let k=0;k<10;k++)P(g,[[x-k,y-k]],k<4?'#FFF8C8':'rgba(255,240,180,'+(1-k/10)+')');star(g,x,y,c);};
 fall(30,60,'#FFE070');fall(90,40,'#FFB0D0');fall(70,110,'#9AD8FF');fall(110,150,'#FFE070');
 // 먹구름(피해요)
 ell(g,40,140,10,5,'#3A3050');ell(g,36,137,6,4,'#4A4060');P(g,[[36,141],[44,141]],'#FFE070');
 R(g,0,232,W,H-232,'#2A2448');for(let x=0;x<W;x+=14)disc(g,x+7,236,6,'#3A3260');
 kid(g,64,240);R(g,66,212,1,20,'#C8A060');ell(g,72,210,7,5,'rgba(220,240,255,.5)');R(g,65,210,14,1,'#C8A060');P(g,[[70,208],[73,209]],'#FFE070');
 shard(g,100,90);
};
D.sheep=g=>{ // 5 양 세기
 grad(g,[30,30,80],[120,90,170]);for(let i=0;i<30;i++)P(g,[[(i*31)%W,(i*23)%120]],'#FFF8C8');disc(g,100,40,10,'#FFF0B0');disc(g,96,37,9,'rgba(60,50,120,1)');
 R(g,0,200,W,H-200,'#5A8A6A');R(g,0,200,W,3,'#7AAA7A');
 // 울타리 + 타이밍 막대
 for(let x=52;x<80;x+=8){R(g,x,176,3,26,'#C89A6A');}R(g,48,182,36,3,'#B08050');R(g,48,192,36,3,'#B08050');
 sheep(g,24,186,0);sheep(g,64,150,1);sheep(g,108,186,0);
 P(g,[[60,140],[63,138],[66,140]],'#FFFFFF');
 R(g,20,226,90,8,'rgba(20,12,36,.6)');R(g,52,226,26,8,'#9AE07A');R(g,66,224,2,12,'#FFFFFF');
 g.fillStyle='#FFE9A0';
};
D.tiny=g=>{ // 6 작아진 나
 R(g,0,0,W,H,'#E8C8A0');for(let y=0;y<H;y+=18)R(g,0,y,W,1,'#D8B890');
 // 거대한 책상 위: 연필·찻잔·지우개가 굴러와요
 R(g,0,212,W,H-212,'#A8744A');R(g,0,212,W,3,'#C8946A');
 R(g,10,60,22,90,'#5A8AD8');R(g,10,60,22,6,'#7AAAF0');R(g,34,80,18,70,'#E86A6A');R(g,34,80,18,5,'#F08A8A');   // 거대한 책
 ell(g,98,190,16,6,'#FFFFFF');R(g,82,160,32,30,'#FFFFFF');ell(g,98,160,16,5,'#F0E8FF');ell(g,98,160,13,3,'#B87A4A');R(g,114,168,6,3,'#FFFFFF');R(g,118,168,3,12,'#FFFFFF');
 P(g,[[94,150],[96,146],[98,150],[100,146]],'rgba(255,255,255,.7)');
 R(g,6,200,40,8,'#F2C450');R(g,2,201,5,6,'#F4B0A0');R(g,44,202,6,4,'#E8D8C0');   // 굴러오는 연필
 kid(g,64,212);P(g,[[58,212],[70,212]],'#8A5A36');
 R(g,70,120,12,8,'#FFB0D0');R(g,70,120,12,2,'#FFD0E8');   // 떨어지는 지우개
 P(g,[[76,112],[76,116]],'#FFFFFF');shard(g,40,180);shard(g,112,130);
};
D.train=g=>{ // 7 별빛 기차
 grad(g,[10,14,40],[40,30,90]);for(let i=0;i<50;i++)P(g,[[(i*37)%W,(i*29)%H]],i%3?'#7A7AC8':'#FFF8C8');
 // 세 갈래 선로 (위에서 본 모습)
 [30,65,100].forEach(x=>{for(let y=40;y<H;y+=8)R(g,x-9,y,19,2,'#6A4A30');R(g,x-7,40,2,H,'#C8A060');R(g,x+6,40,2,H,'#C8A060');});
 ell(g,30,120,8,4,'#4A4060');ell(g,26,117,5,3,'#5A5070');ell(g,100,160,8,4,'#4A4060');ell(g,104,157,5,3,'#5A5070');   // 먹구름 장애물
 shard(g,65,120);shard(g,65,160);shard(g,100,90);
 // 기차 (뒤에서 본 모습)
 R(g,46,214,38,30,'#5A3A8A');R(g,46,248,38,40,'#4A2A7A');R(g,46,214,38,4,'#7A5AB0');R(g,52,222,10,8,'#FFE9A0');R(g,68,222,10,8,'#FFE9A0');R(g,50,244,30,4,'#2A2040');disc(g,54,248,3,'#3A3050');disc(g,76,248,3,'#3A3050');
 R(g,60,200,10,14,'#3A2A5A');P(g,[[64,196],[66,192],[63,188],[67,184]],'rgba(255,255,255,.7)');
 R(g,62,206,6,6,'#F6D2B0');R(g,61,204,8,3,'#D8482E');
};
D.rainbow=g=>{ // 8 무지개 미끄럼틀
 grad(g,[150,200,255],[255,230,240]);cloud(g,6,40,30);cloud(g,90,70,26);
 const cols=['#FF8A8A','#FFC070','#FFE88A','#9AE0A0','#8AC8F8','#B8A0F0'];
 for(let i=0;i<6;i++){for(let x=0;x<W;x++){const y=90+i*4+Math.round(x*.9);if(x>70&&x<84)continue;R(g,x,y,1,4,cols[i]);}}
 cloud(g,0,92,20);cloud(g,100,200,30);
 kid(g,40,128,'jump');P(g,[[34,128],[46,128]],'#FFFFFF');
 shard(g,78,140);shard(g,104,170);star(g,90,120);
 P(g,[[72,160],[74,162],[76,160],[78,162],[80,160],[82,162]],'#FFFFFF');   // 끊긴 틈
};
D.bubble=g=>{ // 9 비눗방울 톡톡
 grad(g,[180,230,250],[230,210,255]);
 const bub=(x,y,r,inner)=>{disc(g,x,y,r,'rgba(255,255,255,.25)');g.strokeStyle='rgba(255,255,255,.9)';g.lineWidth=1;g.beginPath();g.arc(x+.5,y+.5,r,0,6.3);g.stroke();P(g,[[x-r/2|0,y-r/2|0],[x-r/2+1|0,y-r/2|0]],'#FFFFFF');if(inner)inner(x,y);};
 bub(30,60,9,(x,y)=>shard(g,x,y));bub(90,90,11,(x,y)=>star(g,x,y));bub(60,140,8,(x,y)=>shard(g,x,y));bub(100,170,7);bub(24,190,10,(x,y)=>disc(g,x,y,3,'#FF90C0'));
 disc(g,70,40,9,'#3A2E50');P(g,[[67,38],[72,38]],'#FF6060');P(g,[[66,43],[68,44],[70,44],[72,44],[74,43]],'#FF6060');   // 검은 방울(누르면 안 돼요)
 // 톡! 터지는 효과
 [[50,110]].forEach(([x,y])=>{P(g,[[x,y-6],[x,y+6],[x-6,y],[x+6,y],[x-4,y-4],[x+4,y+4],[x-4,y+4],[x+4,y-4]],'#FFFFFF');});
 kid(g,64,262);R(g,70,244,2,12,'#C8A060');ell(g,71,242,4,4,'rgba(255,255,255,.6)');
};
D.toys=g=>{ // 10 장난감 상자 (짝 맞추기)
 R(g,0,0,W,H,'#F8E0C0');for(let x=0;x<W;x+=10)for(let y=0;y<H;y+=10)if((x+y)/10%2)R(g,x,y,10,10,'#F0D0B0');
 const card=(x,y,face)=>{R(g,x,y,26,34,'#2A1E3A');R(g,x+1,y+1,24,32,face?'#FFFFFF':'#8A60D0');if(!face){star(g,x+13,y+17,'#C8A0FF');return;}face(x+13,y+17);};
 const bear=(x,y)=>{disc(g,x,y,6,'#C88A5A');disc(g,x-5,y-5,2,'#C88A5A');disc(g,x+5,y-5,2,'#C88A5A');P(g,[[x-2,y-1],[x+2,y-1]],'#2A1E3A');ell(g,x,y+2,2,1,'#E8B890');};
 const ball=(x,y)=>{disc(g,x,y,6,'#FF6A6A');R(g,x-6,y-1,13,2,'#FFFFFF');disc(g,x,y,1,'#FFE070');};
 const duck=(x,y)=>{disc(g,x,y+1,5,'#FFE070');disc(g,x+2,y-4,3,'#FFE070');R(g,x+5,y-4,3,2,'#FF9A4A');P(g,[[x+2,y-5]],'#2A1E3A');};
 const pos=[[10,56],[40,56],[70,56],[100,56],[10,98],[40,98],[70,98],[100,98],[10,140],[40,140],[70,140],[100,140],[10,182],[40,182],[70,182],[100,182]];
 const faces={1:bear,6:bear,3:ball,9:duck};
 pos.forEach(([x,y],i)=>{if(x>100)return;card(x,y,faces[i]);});
 // 장난감 상자
 R(g,24,228,82,40,'#E86A6A');R(g,24,228,82,5,'#F08A8A');R(g,58,238,14,8,'#FFE070');R(g,20,222,90,7,'#C84A4A');
 kid(g,110,272);
};
D.mochi=g=>{ // 11 달토끼 떡방아
 grad(g,[20,16,60],[60,40,110]);for(let i=0;i<40;i++)P(g,[[(i*37)%W,(i*41)%180]],'#FFF8C8');
 disc(g,65,80,40,'#FFF0B0');disc(g,65,80,36,'#FFF6CC');disc(g,50,66,4,'#F0E0A0');disc(g,80,96,6,'#F0E0A0');
 R(g,0,200,W,H-200,'#4A3A70');
 // 절구 + 떡
 R(g,48,196,34,18,'#8A5A36');R(g,44,192,42,6,'#A87048');ell(g,65,192,16,4,'#FFFFFF');
 // 토끼 둘
 const bun=(x,y,flip)=>{ell(g,x,y,7,8,'#FFFFFF');R(g,x-4,y-17,3,10,'#FFFFFF');R(g,x+1,y-17,3,10,'#FFFFFF');R(g,x-3,y-15,1,6,'#FFB0C0');R(g,x+2,y-15,1,6,'#FFB0C0');P(g,[[x+(flip?-3:2),y-3]],'#2A1E3A');P(g,[[x+(flip?-4:3),y-1]],'#FFB0C0');};
 bun(28,190);bun(104,190,1);
 R(g,30,158,3,30,'#C89A6A');R(g,24,152,22,10,'#A87048');   // 들어 올린 공이
 // 박자 표시
 R(g,10,226,110,12,'rgba(20,12,36,.6)');[30,52,74,96].forEach((x,i)=>disc(g,x,232,4,i===1?'#FFE070':'#C8A0FF'));R(g,50,224,2,16,'#FFFFFF');
 P(g,[[60,182],[64,180],[68,182]],'#FFFFFF');shard(g,100,140);
};
D.bed=g=>{ // 12 날아라 침대
 grad(g,[16,14,50],[70,50,120]);for(let i=0;i<40;i++)P(g,[[(i*37)%W,(i*31)%160]],'#FFF8C8');disc(g,24,36,8,'#FFF0B0');
 // 아래로 지나가는 밤 마을 지붕·굴뚝
 for(let i=0;i<5;i++){const x=i*28-4,h=40+((i*37)%30);R(g,x,H-h,24,h,'#2A2448');R(g,x,H-h,24,3,'#4A4070');R(g,x+4,H-h+10,5,6,'#FFE9A0');R(g,x+14,H-h+10,5,6,i%2?'#FFE9A0':'#3A3460');if(i%2)R(g,x+16,H-h-12,6,12,'#3A3460');}
 // 위에서 내려오는 고드름 구름
 ell(g,100,20,16,8,'#E8E8FF');for(let k=0;k<4;k++)R(g,90+k*6,26,2,6+k%2*4,'#C8D0FF');
 // 날아다니는 침대
 R(g,40,130,40,8,'#8A5A3A');R(g,40,124,40,7,'#7A9CE8');R(g,40,124,40,2,'#A8C0F8');R(g,38,116,4,22,'#6A4A34');R(g,78,122,4,16,'#6A4A34');
 R(g,44,118,9,6,'#F4F0E8');R(g,46,115,6,6,'#F6D2B0');R(g,45,113,8,3,'#5A7AD8');P(g,[[48,118],[50,118]],'#2A1E3A');
 // 날개
 ell(g,36,118,8,4,'#FFFFFF');ell(g,34,114,6,3,'#F0F0FF');ell(g,84,118,8,4,'#FFFFFF');ell(g,86,114,6,3,'#F0F0FF');
 shard(g,104,110);shard(g,112,150);star(g,96,80);
};
// ===== 꿈 목록: [이름, 한국어 이름, 하는 법, 밤잠에서만] =====
const LIST = [
 ['jump', '구름 위 폴짝', '좌우를 눌러 구름을 밟고 올라가요', 0], ['candy', '과자 나라', '바구니로 과자를 받아요 · 브로콜리는 피해요', 0], ['tiny', '작아진 나', '떨어지는 지우개와 찻잔을 피해요', 0],
 ['rainbow', '무지개 미끄럼틀', '누르면 점프! 끊긴 틈을 뛰어넘어요', 0], ['bubble', '비눗방울 톡톡', '방울을 눌러 터뜨려요 · 검은 방울은 안 돼요', 0], ['toys', '장난감 상자', '같은 장난감 카드 두 장을 찾아요', 0],
 ['sea', '거꾸로 바다', '누르면 헤엄쳐 올라가요 · 산호를 피해요', 1], ['stars', '별똥별 줍기', '병을 움직여 별똥별을 담아요 · 먹구름은 피해요', 1], ['sheep', '양 세기', '양이 울타리에 닿을 때 맞춰 눌러요', 1],
 ['train', '별빛 기차', '좌우를 눌러 선로를 바꿔요 · 먹구름은 피해요', 1], ['mochi', '달토끼 떡방아', '박자가 선에 닿을 때 맞춰 눌러요', 1], ['bed', '날아라 침대', '누르면 날아올라요 · 굴뚝과 고드름을 피해요', 1]];
const NAME = Object.fromEntries(LIST.map(x => [x[0], x[1]]));
const rnd = (a, b) => a + Math.random() * (b - a), near = (a, b, r) => Math.abs(a.x - b.x) < r && Math.abs(a.y - b.y) < r;
const blink = st => st.inv > 0 && Math.floor(st.inv * 10) % 2;
const hurt = (st, n = 1) => { if (st.inv > 0) return false; st.inv = 1.2; st.got = Math.max(0, st.got - n); st.fx.push({ x: st.px || 65, y: st.py || 140, t: 0, s: '-' + n, c: '#FF8080' }); return true; };
const gain = (st, n, x, y) => { st.got += n; st.fx.push({ x, y, t: 0, s: '+' + n, c: '#E8D0FF' }); };
const smallTxt = (g, s, x, y, c) => { g.fillStyle = c; g.font = '7px monospace'; g.textAlign = 'center'; g.fillText(s, x, y); };
const bun = (g, x, y, flip, up) => { ell(g, x, y, 7, 8, '#FFFFFF'); R(g, x - 4, y - 17, 3, 10, '#FFFFFF'); R(g, x + 1, y - 17, 3, 10, '#FFFFFF'); R(g, x - 3, y - 15, 1, 6, '#FFB0C0'); R(g, x + 2, y - 15, 1, 6, '#FFB0C0'); P(g, [[x + (flip ? -3 : 2), y - 3]], '#2A1E3A'); P(g, [[x + (flip ? -4 : 3), y - 1]], '#FFB0C0');
 const hx = x + (flip ? -9 : 9); R(g, hx - 1, y - (up ? 26 : 8), 3, up ? 22 : 10, '#C89A6A'); R(g, hx - 6, y - (up ? 32 : 12), 13, 7, '#A87048'); };
const fishS = (g, x, y, c, flip) => { ell(g, x, y, 5, 3, c); P(g, flip ? [[x + 5, y - 2], [x + 6, y - 3], [x + 5, y + 2], [x + 6, y + 3], [x + 6, y]] : [[x - 5, y - 2], [x - 6, y - 3], [x - 5, y + 2], [x - 6, y + 3], [x - 6, y]], c); P(g, [[flip ? x - 3 : x + 3, y - 1]], '#2A1E3A'); };
const bat = (g, x, y, t) => { const f = Math.sin(t * 14) > 0; P(g, [[x - 3, y - (f ? 1 : -1)], [x - 2, y], [x - 1, y], [x, y], [x + 1, y], [x + 2, y], [x + 3, y - (f ? 1 : -1)], [x - 1, y + 1], [x + 1, y + 1]], '#3A2E50'); P(g, [[x - 1, y], [x + 1, y]], '#FF6060'); };
const dark = (g, x, y) => { ell(g, x, y, 8, 4, '#3A3050'); ell(g, x - 3, y - 3, 5, 3, '#4A4060'); P(g, [[x - 3, y + 1], [x + 3, y + 1]], '#FFE070'); };
const toyIc = (g, k, x, y) => { // 장난감 8종
 if (k === 0){ disc(g, x, y, 5, '#C88A5A'); disc(g, x - 4, y - 4, 2, '#C88A5A'); disc(g, x + 4, y - 4, 2, '#C88A5A'); P(g, [[x - 2, y - 1], [x + 2, y - 1]], '#2A1E3A'); }
 else if (k === 1){ disc(g, x, y, 5, '#FF6A6A'); R(g, x - 5, y - 1, 11, 2, '#FFFFFF'); }
 else if (k === 2){ disc(g, x, y + 1, 4, '#FFE070'); disc(g, x + 2, y - 3, 3, '#FFE070'); R(g, x + 5, y - 3, 2, 2, '#FF9A4A'); P(g, [[x + 2, y - 4]], '#2A1E3A'); }
 else if (k === 3) star(g, x, y, '#FFB040');
 else if (k === 4){ disc(g, x - 2, y - 1, 2, '#FF80B0'); disc(g, x + 2, y - 1, 2, '#FF80B0'); for (let i = 0; i < 4; i++) R(g, x - 3 + i, y + i, 7 - i * 2, 1, '#FF80B0'); }
 else if (k === 5){ disc(g, x, y, 5, '#FFE9A0'); disc(g, x + 2, y - 2, 4, '#FFFFFF'); }
 else if (k === 6){ R(g, x - 5, y - 5, 10, 10, '#7AD0F8'); R(g, x - 5, y - 5, 10, 2, '#A8E4FF'); smallTxt(g, 'A', x, y + 3, '#2A6AB8'); }
 else { R(g, x - 6, y - 2, 12, 5, '#9AE07A'); R(g, x - 3, y - 5, 6, 3, '#9AE07A'); disc(g, x - 3, y + 3, 2, '#3A2E50'); disc(g, x + 3, y + 3, 2, '#3A2E50'); } };

// ===== 꿈 12종: init(st) · step(st, dt, inp) · draw(g, st). st.got = 얻은 꿈 조각, inp = { L, R, taps: [{x, y}] } =====
const GAMES = {};
GAMES.jump = { lr: 1, dur: 30,
 init: st => { st.p = { x: 65, y: 230, vy: -170 }; st.cam = 0; st.pl = []; st.it = []; st.top = 260; while (st.top > -40) GAMES.jump.add(st); },
 add: st => { const y = st.top; st.top -= rnd(26, 36); const pink = Math.random() < .14; st.pl.push({ x: rnd(4, 100), y, w: 24, pink }); if (Math.random() < .45) st.it.push({ x: rnd(10, 120), y: y - rnd(10, 22), k: 'shard' }); if (Math.random() < .12 && y < 150) st.it.push({ x: rnd(10, 120), y: y - 14, k: 'bat', ph: rnd(0, 6) }); },
 step: (st, dt, I) => { const p = st.p, y0 = p.y; p.x += ((I.R ? 1 : 0) - (I.L ? 1 : 0)) * 80 * dt; if (p.x < -4) p.x = W + 4; if (p.x > W + 4) p.x = -4; p.vy += 300 * dt; p.y += p.vy * dt;
  if (p.vy > 0) for (const q of st.pl) if (p.x > q.x - 2 && p.x < q.x + q.w + 2 && y0 <= q.y && p.y >= q.y){ p.y = q.y; p.vy = q.pink ? -260 : -185; break; }
  if (p.y - st.cam < 120) st.cam = p.y - 120; while (st.top > st.cam - 40) GAMES.jump.add(st);
  st.pl = st.pl.filter(q => q.y - st.cam < H + 20); st.it = st.it.filter(q => q.y - st.cam < H + 20 && !q.done);
  st.px = p.x; st.py = p.y - st.cam;
  for (const q of st.it){ if (q.k === 'bat') q.x = 65 + Math.sin(st.t * 1.6 + q.ph) * 50;
   if (near({ x: p.x, y: p.y - 6 }, q, 8)){ if (q.k === 'shard'){ q.done = 1; gain(st, 1, q.x, q.y - st.cam); } else if (hurt(st)) p.vy = 80; } }
  if (p.y - st.cam > H + 10){ const q = st.pl.filter(q => q.y - st.cam < H - 10).sort((a, b) => b.y - a.y)[0]; if (q){ p.x = q.x + 12; p.y = q.y; p.vy = -185; } hurt(st); } },
 draw: (g, st) => { grad(g, [120, 150, 240], [255, 200, 225]); for (let i = 0; i < 14; i++) P(g, [[(i * 29) % W, ((i * 41 - st.cam * .2) % H + H) % H]], '#FFFFFF');
  st.pl.forEach(q => cloud(g, q.x, q.y - st.cam + 2, q.w, q.pink ? '#FFD0E8' : '#FFFFFF', q.pink ? '#F0A0C8' : '#D8E4FF'));
  st.it.forEach(q => q.k === 'shard' ? shard(g, q.x | 0, (q.y - st.cam) | 0) : bat(g, q.x | 0, (q.y - st.cam) | 0, st.t));
  if (!blink(st)) kid(g, st.p.x | 0, (st.p.y - st.cam) | 0, st.p.vy < 0 ? 'jump' : 'stand'); } };
const catcher = (o) => ({ lr: 1, dur: o.dur || 30, hp: o.hp,
 init: st => { st.bx = 65; st.it = []; st.cd = 0; },
 step: (st, dt, I) => { st.bx = Math.max(10, Math.min(W - 10, st.bx + ((I.R ? 1 : 0) - (I.L ? 1 : 0)) * 95 * dt)); st.px = st.bx; st.py = o.by - 10;
  if ((st.cd -= dt) <= 0){ st.cd = rnd(.35, .6) * (1 - Math.min(.4, st.t / 80)); st.it.push(o.spawn(st)); }
  for (const q of st.it){ q.x += (q.vx || 0) * dt; q.y += q.vy * dt; if (!q.done && q.y > o.by - 6 && q.y < o.by + 4 && Math.abs(q.x - st.bx) < 12){ q.done = 1; o.catch(st, q); } }
  st.it = st.it.filter(q => !q.done && q.y < H + 10); },
 draw: (g, st) => { o.bg(g, st); st.it.forEach(q => o.item(g, q)); o.hold(g, st); } });
GAMES.candy = catcher({ hp: 3, by: 214,
 spawn: st => { const r = Math.random(); return { x: rnd(10, 120), y: -6, vy: 55 + st.t * 2, k: r < .2 ? 'broc' : r < .32 ? 'shard' : ['donut', 'candy', 'cookie'][Math.floor(Math.random() * 3)] }; },
 catch: (st, q) => { if (q.k === 'broc'){ st.hp--; st.fx.push({ x: q.x, y: q.y, t: 0, s: '으엑', c: '#9AE07A' }); if (st.hp <= 0) st.over = 1; } else gain(st, q.k === 'shard' ? 3 : 1, q.x, q.y); },
 bg: g => { grad(g, [255, 214, 232], [255, 240, 210]); for (let i = 0; i < 6; i++){ const x = i * 24 - 4; R(g, x, 170, 22, 40, i % 2 ? '#C88A5A' : '#D8A070'); R(g, x, 166, 22, 5, '#FFFFFF'); R(g, x + 8, 190, 6, 20, '#7A4A2A'); } R(g, 0, 210, W, H - 210, '#F8C8A0'); for (let x = 0; x < W; x += 8) R(g, x, 214, 4, 2, '#FFFFFF'); },
 item: (g, q) => { const x = q.x | 0, y = q.y | 0;
  if (q.k === 'donut'){ disc(g, x, y, 4, '#E8A060'); disc(g, x, y, 3, '#FF90C0'); disc(g, x, y, 1, '#F8C8A0'); }
  else if (q.k === 'candy'){ disc(g, x, y, 3, '#80D0FF'); P(g, [[x - 5, y - 1], [x - 4, y], [x - 5, y + 1], [x + 5, y - 1], [x + 4, y], [x + 5, y + 1]], '#80D0FF'); }
  else if (q.k === 'cookie'){ disc(g, x, y, 4, '#D8A060'); P(g, [[x - 2, y - 1], [x + 1, y - 2], [x + 2, y + 1]], '#6A3A1A'); }
  else if (q.k === 'shard') shard(g, x, y);
  else { R(g, x - 1, y, 3, 4, '#7AB850'); disc(g, x - 2, y - 2, 2, '#3A8A30'); disc(g, x + 2, y - 2, 2, '#3A8A30'); disc(g, x, y - 4, 2, '#4A9A38'); } },
 hold: (g, st) => { const x = st.bx | 0; if (!blink(st)) kid(g, x, 240); R(g, x - 5, 216, 2, 10, '#F6D2B0'); R(g, x + 4, 216, 2, 10, '#F6D2B0'); R(g, x - 11, 210, 22, 8, '#C88A3A'); R(g, x - 11, 210, 22, 2, '#E8B060'); } });
GAMES.stars = catcher({ by: 212,
 spawn: st => { const r = Math.random(); return { x: rnd(20, 140), y: -6, vx: -rnd(10, 25), vy: 50 + st.t * 1.6, k: r < .18 ? 'cloud' : r < .3 ? 'gold' : 'star', c: ['#FFE070', '#FFB0D0', '#9AD8FF'][Math.floor(Math.random() * 3)] }; },
 catch: (st, q) => { if (q.k === 'cloud') hurt(st, 2); else gain(st, q.k === 'gold' ? 3 : 1, q.x, q.y); },
 bg: (g, st) => { grad(g, [14, 10, 40], [50, 36, 100]); for (let i = 0; i < 60; i++) P(g, [[(i * 37) % W, (i * 53) % 220]], (i + Math.floor(st.t * 3)) % 7 ? '#8A7AC8' : '#FFF8C8'); R(g, 0, 232, W, H - 232, '#2A2448'); for (let x = 0; x < W; x += 14) disc(g, x + 7, 236, 6, '#3A3260'); },
 item: (g, q) => { const x = q.x | 0, y = q.y | 0; if (q.k === 'cloud') return dark(g, x, y); for (let k = 1; k < 8; k++) P(g, [[x + k, y - k * 2]], `rgba(255,240,180,${1 - k / 8})`); star(g, x, y, q.k === 'gold' ? '#FFD040' : q.c); if (q.k === 'gold') star(g, x, y, '#FFE070', '#FFFFFF'); },
 hold: (g, st) => { const x = st.bx | 0; if (!blink(st)) kid(g, x - 6, 240); ell(g, x, 214, 9, 6, 'rgba(220,240,255,.55)'); R(g, x - 9, 207, 18, 2, '#C8A060'); R(g, x - 7, 222, 2, 12, '#F6D2B0'); } });
GAMES.tiny = { lr: 1, dur: 30,
 init: st => { st.x = 65; st.it = []; st.cd = 0; },
 step: (st, dt, I) => { st.x = Math.max(8, Math.min(W - 8, st.x + ((I.R ? 1 : 0) - (I.L ? 1 : 0)) * 85 * dt)); st.px = st.x; st.py = 200;
  if ((st.cd -= dt) <= 0){ st.cd = rnd(.3, .55) * (1 - Math.min(.45, st.t / 70)); const r = Math.random(); st.it.push({ x: rnd(8, 122), y: -10, vy: 60 + st.t * 2.4, k: r < .3 ? 'shard' : ['eraser', 'cup', 'clip'][Math.floor(Math.random() * 3)] }); }
  for (const q of st.it){ q.y += q.vy * dt; if (!q.done && Math.abs(q.x - st.x) < 8 && q.y > 196 && q.y < 214){ q.done = 1; if (q.k === 'shard') gain(st, 1, q.x, q.y); else hurt(st); } }
  st.it = st.it.filter(q => !q.done && q.y < 216); },
 draw: (g, st) => { R(g, 0, 0, W, H, '#E8C8A0'); for (let y = 0; y < H; y += 18) R(g, 0, y, W, 1, '#D8B890'); R(g, 10, 60, 22, 90, '#5A8AD8'); R(g, 10, 60, 22, 6, '#7AAAF0'); R(g, 98, 70, 20, 80, '#E86A6A'); R(g, 98, 70, 20, 5, '#F08A8A'); R(g, 0, 212, W, H - 212, '#A8744A'); R(g, 0, 212, W, 3, '#C8946A');
  st.it.forEach(q => { const x = q.x | 0, y = q.y | 0; if (q.k === 'shard') shard(g, x, y); else if (q.k === 'eraser'){ R(g, x - 6, y - 4, 12, 8, '#FFB0D0'); R(g, x - 6, y - 4, 12, 2, '#FFD0E8'); } else if (q.k === 'cup'){ R(g, x - 6, y - 5, 12, 10, '#FFFFFF'); R(g, x - 5, y - 5, 10, 2, '#B87A4A'); R(g, x + 6, y - 2, 2, 4, '#FFFFFF'); } else { R(g, x - 1, y - 6, 3, 12, '#9AA4B4'); R(g, x - 3, y - 6, 2, 9, '#9AA4B4'); } });
  if (!blink(st)) kid(g, st.x | 0, 212); } };
GAMES.rainbow = { dur: 30,
 init: st => { st.p = { y: 196, vy: 0, on: 1 }; st.seg = [{ x: -10, w: 160 }]; st.it = []; st.off = 0; },
 step: (st, dt, I) => { const sp = 55 + st.t * 1.2, p = st.p; st.off += sp * dt; st.seg.forEach(s => s.x -= sp * dt); st.it.forEach(q => q.x -= sp * dt);
  let last = st.seg[st.seg.length - 1]; while (last.x + last.w < W + 60){ const gap = rnd(16, 26), w = rnd(40, 80); st.seg.push({ x: last.x + last.w + gap, w }); if (Math.random() < .8) st.it.push({ x: last.x + last.w + gap / 2, y: rnd(160, 180) }); if (Math.random() < .6) st.it.push({ x: last.x + last.w + gap + w / 2, y: 186 }); last = st.seg[st.seg.length - 1]; }
  st.seg = st.seg.filter(s => s.x + s.w > -10); st.it = st.it.filter(q => q.x > -10 && !q.done);
  if (I.taps.length && p.on){ p.vy = -165; p.on = 0; }
  p.vy += 420 * dt; p.y += p.vy * dt; const ground = st.seg.some(s => 36 > s.x - 2 && 36 < s.x + s.w + 2);
  if (ground && p.y >= 196 && p.y - p.vy * dt <= 197){ p.y = 196; p.vy = 0; p.on = 1; } else if (p.y < 196 || !ground) p.on = 0;
  st.px = 36; st.py = p.y - 8;
  if (p.y > H + 10){ p.y = 150; p.vy = 0; const s = st.seg.find(s => s.x + s.w > 50); if (s && s.x > 36) st.seg.unshift({ x: 20, w: s.x - 20 + 1 }); hurt(st, 2); }
  for (const q of st.it) if (!q.done && near({ x: 36, y: p.y - 6 }, q, 8)){ q.done = 1; gain(st, 1, q.x, q.y); } },
 draw: (g, st) => { grad(g, [150, 200, 255], [255, 230, 240]); for (let i = 0; i < 4; i++) cloud(g, ((i * 50 - st.off * .3) % 180 + 180) % 180 - 30, 40 + i * 25, 26);
  const cols = ['#FF8A8A', '#FFC070', '#FFE88A', '#9AE0A0', '#8AC8F8', '#B8A0F0'];
  st.seg.forEach(s => { for (let i = 0; i < 6; i++) R(g, s.x, 197 + i * 4, s.w, 4, cols[i]); cloud(g, s.x - 6, 200, 12); cloud(g, s.x + s.w - 6, 200, 12); });
  st.it.forEach(q => shard(g, q.x | 0, q.y | 0)); if (!blink(st)) kid(g, 36, st.p.y | 0, st.p.on ? 'stand' : 'jump'); } };
GAMES.bubble = { dur: 30,
 init: st => { st.it = []; st.cd = 0; },
 step: (st, dt, I) => { if ((st.cd -= dt) <= 0){ st.cd = rnd(.3, .55); const r = Math.random(); st.it.push({ x: rnd(14, 116), y: H + 10, vy: -rnd(26, 46) - st.t * .8, r: Math.floor(rnd(7, 11)), k: r < .16 ? 'black' : r < .4 ? 'shard' : r < .6 ? 'star' : 'plain', ph: rnd(0, 6) }); }
  st.it.forEach(q => { q.y += q.vy * dt; q.x += Math.sin(st.t * 2 + q.ph) * 8 * dt; });
  for (const tp of I.taps) for (const q of st.it) if (!q.done && Math.hypot(tp.x - q.x, tp.y - q.y) < q.r + 4){ q.done = 1; if (q.k === 'black'){ st.got = Math.max(0, st.got - 3); st.fx.push({ x: q.x, y: q.y, t: 0, s: '-3', c: '#FF8080' }); } else gain(st, q.k === 'shard' ? 2 : 1, q.x, q.y); st.pop.push({ x: q.x, y: q.y, t: 0 }); break; }
  st.it = st.it.filter(q => !q.done && q.y > -20); st.pop = st.pop.filter(q => (q.t += dt) < .3); },
 draw: (g, st) => { grad(g, [180, 230, 250], [230, 210, 255]);
  st.it.forEach(q => { const x = q.x | 0, y = q.y | 0; if (q.k === 'black'){ disc(g, x, y, q.r, '#3A2E50'); P(g, [[x - 3, y - 1], [x + 3, y - 1]], '#FF6060'); return; } disc(g, x, y, q.r, 'rgba(255,255,255,.25)'); g.strokeStyle = 'rgba(255,255,255,.9)'; g.lineWidth = 1; g.beginPath(); g.arc(x + .5, y + .5, q.r, 0, 6.3); g.stroke(); P(g, [[x - (q.r >> 1), y - (q.r >> 1)]], '#FFFFFF'); if (q.k === 'shard') shard(g, x, y); else if (q.k === 'star') star(g, x, y); });
  st.pop.forEach(q => { const d = 3 + q.t * 20; P(g, [[q.x, q.y - d], [q.x, q.y + d], [q.x - d, q.y], [q.x + d, q.y]].map(([a, b]) => [a | 0, b | 0]), '#FFFFFF'); });
  kid(g, 65, 268); }, };
GAMES.toys = { dur: 45,
 init: st => { const ks = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7].sort(() => Math.random() - .5); st.c = ks.map((k, i) => ({ k, x: 12 + (i % 4) * 28, y: 54 + Math.floor(i / 4) * 40, up: 0, ok: 0 })); st.open = []; st.wait = 0; },
 step: (st, dt, I) => { if (st.wait > 0){ st.wait -= dt; if (st.wait <= 0){ const [a, b] = st.open; if (a.k === b.k){ a.ok = b.ok = 1; gain(st, 2, b.x + 13, b.y); if (st.c.every(c => c.ok)){ gain(st, 5, 65, 120); st.over = 1; } } else a.up = b.up = 0; st.open = []; } return; }
  for (const tp of I.taps){ const c = st.c.find(c => !c.up && tp.x >= c.x && tp.x < c.x + 26 && tp.y >= c.y && tp.y < c.y + 34); if (!c) continue; c.up = 1; st.open.push(c); if (st.open.length === 2){ st.wait = .55; break; } } },
 draw: (g, st) => { R(g, 0, 0, W, H, '#F8E0C0'); for (let x = 0; x < W; x += 10) for (let y = 0; y < H; y += 10) if ((x + y) / 10 % 2) R(g, x, y, 10, 10, '#F0D0B0');
  st.c.forEach(c => { R(g, c.x, c.y, 26, 34, '#2A1E3A'); R(g, c.x + 1, c.y + 1, 24, 32, c.up ? (c.ok ? '#E8FFE0' : '#FFFFFF') : '#8A60D0'); if (c.up) toyIc(g, c.k, c.x + 13, c.y + 17); else star(g, c.x + 13, c.y + 17, '#C8A0FF'); });
  R(g, 24, 228, 82, 40, '#E86A6A'); R(g, 24, 228, 82, 5, '#F08A8A'); R(g, 58, 238, 14, 8, '#FFE070'); R(g, 20, 222, 90, 7, '#C84A4A'); } };
const flappy = o => ({ dur: 30,
 init: st => { st.p = { y: 140, vy: 0 }; st.col = []; st.cd = .8; st.it = []; st.off = 0; },
 step: (st, dt, I) => { const sp = 48 + st.t * .8, p = st.p; st.off += sp * dt; if (I.taps.length) p.vy = -112; p.vy = Math.min(150, p.vy + 270 * dt); p.y += p.vy * dt; if (p.y < 30){ p.y = 30; p.vy = 0; } if (p.y > H - 14){ p.y = H - 14; p.vy = -60; hurt(st); }
  if ((st.cd -= dt) <= 0){ st.cd = rnd(1.5, 1.9); const c = rnd(90, 200), gap = 76 - Math.min(16, st.t * .5); st.col.push({ x: W + 10, t: c - gap / 2, b: c + gap / 2, w: 12 }); st.it.push({ x: W + 16, y: c }); }
  st.col.forEach(c => c.x -= sp * dt); st.it.forEach(q => q.x -= sp * dt); st.col = st.col.filter(c => c.x > -20); st.it = st.it.filter(q => q.x > -10 && !q.done);
  st.px = 40; st.py = p.y;
  for (const c of st.col) if (40 + 6 > c.x && 40 - 6 < c.x + c.w && (p.y - 5 < c.t || p.y + 5 > c.b)) hurt(st);
  for (const q of st.it) if (!q.done && near({ x: 40, y: p.y }, q, 9)){ q.done = 1; gain(st, 2, q.x, q.y); } },
 draw: (g, st) => { o.bg(g, st); st.col.forEach(c => o.col(g, c)); st.it.forEach(q => shard(g, q.x | 0, q.y | 0)); if (!blink(st)) o.me(g, 40, st.p.y | 0, st); } });
GAMES.sea = flappy({
 bg: (g, st) => { grad(g, [30, 70, 140], [120, 200, 240]); R(g, 0, 0, W, 24, '#E8D090'); for (let x = 0; x < W; x += 6) P(g, [[(x - st.off * .5 % 6 + W) % W | 0, 23]], '#C8B070'); for (let i = 0; i < 3; i++) fishS(g, ((i * 60 - st.off * .6) % 190 + 190) % 190 - 30, 90 + i * 60, ['#FFB040', '#80E0C0', '#FF90C0'][i], 1); for (let i = 0; i < 8; i++) disc(g, (i * 17 + 5) % W, ((i * 37 - st.t * 20) % H + H) % H, 1, 'rgba(220,245,255,.7)'); },
 col: (g, c) => { const x = c.x | 0; R(g, x, 24, c.w, c.t - 24, '#FF7A90'); R(g, x - 3, c.t - 6, c.w + 6, 6, '#FF9AAA'); R(g, x + 2, c.b, c.w - 4, H - c.b, '#3A9A70'); R(g, x - 2, c.b, c.w + 4, 5, '#5ABA88'); },
 me: (g, x, y) => { disc(g, x, y - 4, 9, 'rgba(200,240,255,.35)'); kid(g, x, y + 4, 'jump', '#2A6AB8'); } });
GAMES.bed = flappy({
 bg: (g, st) => { grad(g, [16, 14, 50], [70, 50, 120]); for (let i = 0; i < 40; i++) P(g, [[((i * 37 - st.off * .2) % W + W) % W | 0, (i * 31) % 160]], '#FFF8C8'); disc(g, 24, 36, 8, '#FFF0B0'); for (let i = 0; i < 7; i++){ const x = ((i * 28 - st.off * .5) % 196 + 196) % 196 - 30, h = 30 + ((i * 37) % 24); R(g, x, H - h, 24, h, '#2A2448'); R(g, x + 4, H - h + 8, 5, 6, '#FFE9A0'); } },
 col: (g, c) => { const x = c.x | 0; ell(g, x + 6, c.t - 8, 14, 9, '#E8E8FF'); R(g, x - 6, 0, 24, c.t - 12, '#E8E8FF'); for (let k = 0; k < 4; k++) R(g, x - 2 + k * 4, c.t - 4, 2, 4 + k % 2 * 3, '#C8D0FF'); R(g, x, c.b, c.w, H - c.b, '#5A4A78'); R(g, x - 2, c.b, c.w + 4, 4, '#7A6A98'); R(g, x + 3, c.b - 8, 6, 8, '#4A3A68'); },
 me: (g, x, y, st) => { const f = Math.sin(st.t * 16) > 0 ? 1 : 0; R(g, x - 14, y + 2, 28, 5, '#8A5A3A'); R(g, x - 14, y - 2, 28, 5, '#7A9CE8'); R(g, x - 15, y - 7, 3, 14, '#6A4A34'); R(g, x + 12, y - 4, 3, 11, '#6A4A34'); R(g, x - 11, y - 7, 6, 5, '#F6D2B0'); R(g, x - 12, y - 9, 8, 3, '#5A7AD8'); ell(g, x - 18, y - 2 - f * 3, 6, 3, '#FFFFFF'); ell(g, x + 18, y - 2 - f * 3, 6, 3, '#FFFFFF'); } });
GAMES.sheep = { dur: 30,
 init: st => { st.sh = []; st.cd = .6; st.hit = null; },
 step: (st, dt, I) => { if ((st.cd -= dt) <= 0){ st.cd = rnd(1.1, 1.8) * (1 - Math.min(.35, st.t / 90)); st.sh.push({ x: -12, j: 0, res: null }); }
  st.sh.forEach(s => { s.x += (42 + st.t * .6) * dt; if (s.j > 0) s.j -= dt; });
  const cand = st.sh.filter(s => !s.res).sort((a, b) => Math.abs(a.x - 65) - Math.abs(b.x - 65))[0];
  if (I.taps.length && cand){ const d = Math.abs(cand.x - 65); if (d < 5){ cand.res = 'good'; cand.j = .6; gain(st, 2, 65, 140); st.hit = { t: .5, s: '최고!' }; } else if (d < 12){ cand.res = 'ok'; cand.j = .6; gain(st, 1, 65, 140); st.hit = { t: .5, s: '좋아!' }; } else if (d < 26){ cand.res = 'miss'; st.hit = { t: .5, s: '쿵' }; } }
  st.sh.forEach(s => { if (!s.res && s.x > 80){ s.res = 'miss'; } }); st.sh = st.sh.filter(s => s.x < W + 15); if (st.hit && (st.hit.t -= dt) <= 0) st.hit = null; },
 draw: (g, st) => { grad(g, [30, 30, 80], [120, 90, 170]); for (let i = 0; i < 30; i++) P(g, [[(i * 31) % W, (i * 23) % 120]], '#FFF8C8'); disc(g, 100, 40, 10, '#FFF0B0'); disc(g, 96, 37, 9, '#3C3278');
  R(g, 0, 200, W, H - 200, '#5A8A6A'); R(g, 0, 200, W, 3, '#7AAA7A'); for (let x = 54; x < 78; x += 8) R(g, x, 176, 3, 26, '#C89A6A'); R(g, 50, 182, 32, 3, '#B08050'); R(g, 50, 192, 32, 3, '#B08050');
  st.sh.forEach(s => { const jy = s.j > 0 ? Math.sin((.6 - s.j) / .6 * Math.PI) * 34 : 0; sheep(g, s.x | 0, (190 - jy) | 0, Math.floor(st.t * 8) % 2); if (s.res === 'miss' && s.x > 60 && s.x < 76) smallTxt(g, '?', s.x, 172, '#FFFFFF'); });
  R(g, 20, 226, 90, 8, 'rgba(20,12,36,.6)'); R(g, 53, 226, 24, 8, '#5A9A4A'); R(g, 60, 226, 10, 8, '#9AE07A');
  const c = st.sh.filter(s => !s.res).sort((a, b) => Math.abs(a.x - 65) - Math.abs(b.x - 65))[0]; if (c){ const x = Math.max(20, Math.min(110, 65 + (c.x - 65) * .9)); R(g, x | 0, 223, 2, 14, '#FFFFFF'); }
  if (st.hit) smallTxt(g, st.hit.s, 65, 160, '#FFE9A0'); } };
GAMES.train = { lr: 1, dur: 30, lane: 1,
 init: st => { st.ln = 1; st.x = 65; st.it = []; st.cd = 0; st.prevL = 0; st.prevR = 0; },
 step: (st, dt, I) => { if (I.L && !st.prevL) st.ln = Math.max(0, st.ln - 1); if (I.R && !st.prevR) st.ln = Math.min(2, st.ln + 1); st.prevL = I.L; st.prevR = I.R;
  for (const tp of I.taps) st.ln = Math.max(0, Math.min(2, st.ln + (tp.x < 65 ? -1 : 1)));
  const tx = [30, 65, 100][st.ln]; st.x += (tx - st.x) * Math.min(1, dt * 14); st.px = st.x; st.py = 214;
  if ((st.cd -= dt) <= 0){ st.cd = rnd(.35, .6); const r = Math.random(); st.it.push({ ln: Math.floor(Math.random() * 3), y: 30, k: r < .32 ? 'cloud' : 'shard' }); }
  const sp = 80 + st.t * 2; st.it.forEach(q => q.y += sp * dt); st.off = (st.off || 0) + sp * dt;
  for (const q of st.it) if (!q.done && q.ln === st.ln && q.y > 204 && q.y < 226){ q.done = 1; if (q.k === 'shard') gain(st, 1, [30, 65, 100][q.ln], q.y); else hurt(st, 2); }
  st.it = st.it.filter(q => !q.done && q.y < H + 10); },
 draw: (g, st) => { grad(g, [10, 14, 40], [40, 30, 90]); for (let i = 0; i < 50; i++) P(g, [[(i * 37) % W, ((i * 29 + st.off * .3) % H) | 0]], i % 3 ? '#7A7AC8' : '#FFF8C8');
  [30, 65, 100].forEach(x => { for (let y = ((st.off || 0) % 8) - 8; y < H; y += 8) R(g, x - 9, y | 0, 19, 2, '#6A4A30'); R(g, x - 7, 0, 2, H, '#C8A060'); R(g, x + 6, 0, 2, H, '#C8A060'); });
  st.it.forEach(q => { const x = [30, 65, 100][q.ln], y = q.y | 0; q.k === 'shard' ? shard(g, x, y) : dark(g, x, y); });
  if (!blink(st)){ const x = st.x | 0; R(g, x - 12, 214, 24, 22, '#5A3A8A'); R(g, x - 12, 214, 24, 3, '#7A5AB0'); R(g, x - 8, 220, 6, 6, '#FFE9A0'); R(g, x + 2, 220, 6, 6, '#FFE9A0'); R(g, x - 12, 236, 24, 50, '#4A2A7A'); R(g, x - 4, 204, 8, 10, '#3A2A5A'); R(g, x - 3, 206, 6, 6, '#F6D2B0'); R(g, x - 4, 204, 8, 3, '#D8482E'); P(g, [[x, 198], [x + 2, 194], [x - 1, 190]], 'rgba(255,255,255,.7)'); } } };
GAMES.mochi = { dur: 30,
 init: st => { st.n = []; let t = 1.2; while (t < 30){ st.n.push({ t, res: null }); t += [.6, .6, .9, .3][Math.floor(Math.random() * 4)] + .2; } st.pound = 0; st.hit = null; },
 step: (st, dt, I) => { const LX = 34, SP = 70; st.n.forEach(n => { n.x = LX + (n.t - st.t) * SP; if (!n.res && st.t - n.t > .25) n.res = 'miss'; });
  if (st.lock > 0) st.lock -= dt; else if (I.taps.length){ st.pound = .15; const c = st.n.filter(n => !n.res).sort((a, b) => Math.abs(a.t - st.t) - Math.abs(b.t - st.t))[0], d = c ? Math.abs(c.t - st.t) : 9; if (d >= .14){ st.lock = .9; st.hit = { t: .4, s: '삐끗' }; } if (c){ if (d < .07){ c.res = 'good'; gain(st, 2, 65, 170); st.hit = { t: .4, s: '쿵떡!' }; } else if (d < .14){ c.res = 'ok'; gain(st, 1, 65, 170); st.hit = { t: .4, s: '쿵' }; } } }
  if (st.pound > 0) st.pound -= dt; if (st.hit && (st.hit.t -= dt) <= 0) st.hit = null; },
 draw: (g, st) => { grad(g, [20, 16, 60], [60, 40, 110]); for (let i = 0; i < 40; i++) P(g, [[(i * 37) % W, (i * 41) % 180]], '#FFF8C8'); disc(g, 65, 80, 40, '#FFF0B0'); disc(g, 65, 80, 36, '#FFF6CC'); disc(g, 50, 66, 4, '#F0E0A0'); disc(g, 80, 96, 6, '#F0E0A0');
  R(g, 0, 200, W, H - 200, '#4A3A70'); R(g, 48, 196, 34, 18, '#8A5A36'); R(g, 44, 192, 42, 6, '#A87048'); ell(g, 65, 192, 16, 4, '#FFFFFF');
  bun(g, 30, 190, 0, st.pound <= 0); bun(g, 100, 190, 1, st.pound > 0);
  R(g, 0, 226, W, 14, 'rgba(20,12,36,.7)'); R(g, 33, 224, 2, 18, '#FFFFFF');
  st.n.forEach(n => { if (n.x < -10 || n.x > W + 10 || n.res === 'good' || n.res === 'ok') return; disc(g, n.x | 0, 233, 4, n.res === 'miss' ? '#6A5A8A' : '#FFE070'); });
  if (st.hit) smallTxt(g, st.hit.s, 65, 160, '#FFE9A0'); } };

// ===== 연출 · 실행 =====
const sleepP = ms => new Promise(r => setTimeout(r, ms));
function run(opt){   // opt = { pool: [이름...], onStart(k), isNew(k) } → Promise<{ k, got }>
 return new Promise(async done => {
  const pool = opt.pool && opt.pool.length ? opt.pool : LIST.map(x => x[0]), k = pool[Math.floor(Math.random() * pool.length)];
  opt.onStart && opt.onStart(k);
  const ov = document.createElement('div'); ov.id = 'dreamv';
  ov.innerHTML = `<canvas class="dc" width="${W}" height="${H}"></canvas><canvas class="do" width="${W}" height="${H}"></canvas><div class="dt1">스르륵....</div><div class="dt2">꿈속으로 빠져들어요</div>
   <div class="dcard"><span>오늘의 꿈</span><b>???</b></div><div class="dhud"><span class="pill dn"></span><span class="pill dtm"></span></div><div class="dhud d2"><span class="pill dsh"></span><span class="pill dhp"></span></div>
   <div class="dtip"><span class="pill"></span></div><div class="dbtns"><button class="dl">◀</button><button class="dr">▶</button></div><div class="dgo">시작!</div><div class="dres"></div>`;
  document.body.appendChild(ov);
  const q = s => ov.querySelector(s), cv = q('.dc'), g = cv.getContext('2d'), o = q('.do').getContext('2d'), show = (s, v) => q(s).classList.toggle('on', !!v);
  // 1) 눈 감기 → 별 소용돌이 → 꿈 방울 → 오늘의 꿈 뽑기 → 방울이 퍼지며 꿈으로
  const lids = kk => { o.clearRect(0, 0, W, H); const h = Math.round(H / 2 * kk); o.fillStyle = '#0A0612'; o.fillRect(0, 0, W, h); o.fillRect(0, H - h, W, h); if (kk > 0 && kk < 1){ o.fillStyle = '#3A2A50'; o.fillRect(0, h - 1, W, 1); o.fillRect(0, H - h, W, 1); } };
  const swirl = (t, kk) => { R(g, 0, 0, W, H, '#0A0612'); for (let i = 0; i < 90; i++){ const a = i * 2.4 + t * 2.2, r = (1 - ((i / 90 + t * .35) % 1)) * 110 * (1 - kk * .3), x = W / 2 + Math.cos(a) * r, y = H / 2 + Math.sin(a) * r * 1.1, c = ['#FFF8C8', '#C8A0FF', '#9AD8FF', '#FFB0D0'][i % 4]; P(g, [[x | 0, y | 0]], c); if (i % 6 === 0) star(g, x | 0, y | 0, c); } };
  const bubble = (t, r) => { swirl(t, 1); const cx = W / 2, cy = H / 2; for (let y = -r; y <= r; y++) for (let x = -r; x <= r; x++){ const d = x * x + y * y; if (d <= r * r){ const h = (Math.atan2(y, x) / 6.28 + t * .2 + d / (r * r) * .3) % 1; g.fillStyle = `hsl(${h * 360 | 0},70%,${78 - d / (r * r) * 12}%)`; g.fillRect(cx + x, cy + y, 1, 1); } } g.strokeStyle = 'rgba(255,255,255,.9)'; g.beginPath(); g.arc(cx + .5, cy + .5, r, 0, 6.3); g.stroke(); };
  const names = LIST.filter(x => pool.includes(x[0])).map(x => x[1]);
  await new Promise(res => { let t0 = null; const fr = now => { if (!t0) t0 = now; const t = (now - t0) / 1000;
   if (t < 1.3) lids(Math.min(1, t / 1.1));
   else if (t < 3.1){ cv.style.opacity = 1; lids(0); swirl(t, (t - 1.3) / 1.8); show('.dt1', 1); show('.dt2', t > 1.8); }
   else if (t < 4.3){ show('.dt1', 0); show('.dt2', 0); bubble(t, Math.round(4 + (t - 3.1) / 1.2 * 40)); }
   else if (t < 7.3){ bubble(t, 44); show('.dcard', 1); const kk = t - 4.5; q('.dcard b').textContent = kk < 0 ? '???' : kk < 2 ? names[Math.floor(kk * kk * 3 + kk * 12) % names.length] : NAME[k]; q('.dcard').classList.toggle('hit', t > 6.5); }
   else if (t < 8.3){ show('.dcard', 0); bubble(t, Math.round(44 + Math.min(1, (t - 7.3) / .9) * 130)); }
   else return res();
   requestAnimationFrame(fr); }; requestAnimationFrame(fr); });
  // 2) 꿈 미니게임
  const Gm = GAMES[k], st = { t: 0, got: 0, inv: 0, fx: [], pop: [], hp: Gm.hp || 0, over: 0 }, I = { L: 0, R: 0, taps: [] };
  Gm.init(st); Gm.draw(g, st);
  q('.dn').textContent = NAME[k]; q('.dtip .pill').textContent = LIST.find(x => x[0] === k)[2]; show('.dhud', 1); ov.querySelectorAll('.dhud').forEach(e => e.classList.add('on')); show('.dtip', 1); if (Gm.lr) show('.dbtns', 1); if (!Gm.hp) q('.dhp').style.display = 'none';
  show('.dgo', 1); await sleepP(900); show('.dgo', 0);
  const hold = (b, key) => { const on = e => { e.preventDefault(); I[key] = 1; }, off = () => { I[key] = 0; }; b.addEventListener('pointerdown', on); b.addEventListener('pointerup', off); b.addEventListener('pointerleave', off); b.addEventListener('pointercancel', off); };
  hold(q('.dl'), 'L'); hold(q('.dr'), 'R');
  const kd = e => { if (e.key === 'ArrowLeft') I.L = e.type === 'keydown' ? 1 : 0; if (e.key === 'ArrowRight') I.R = e.type === 'keydown' ? 1 : 0; if (e.type === 'keydown' && (e.key === ' ' || e.key === 'ArrowUp')) I.taps.push({ x: 65, y: 140 }); };
  addEventListener('keydown', kd); addEventListener('keyup', kd);
  cv.addEventListener('pointerdown', e => { e.preventDefault(); const r = cv.getBoundingClientRect(), k2 = Math.min(r.width / W, r.height / H), ox = r.left + (r.width - W * k2) / 2, oy = r.top + (r.height - H * k2) / 2, x = (e.clientX - ox) / k2, y = (e.clientY - oy) / k2;   // object-fit: contain I.taps.push({ x, y });
   if (Gm.lr && k !== 'train'){ const key = x < W / 2 ? 'L' : 'R'; I[key] = 1; const up = () => { I[key] = 0; removeEventListener('pointerup', up); }; addEventListener('pointerup', up); } });
  await new Promise(res => { let last = performance.now(); const fr = now => { const dt = Math.min(.05, Math.max(0, now - last) / 1000); last = now; st.t += dt; if (st.inv > 0) st.inv -= dt;
   Gm.step(st, dt, I); I.taps = []; Gm.draw(g, st);
   st.fx = st.fx.filter(f => (f.t += dt) < .8); st.fx.forEach(f => smallTxt(g, f.s, f.x, f.y - f.t * 20, f.c));
   q('.dtm').textContent = '⌛ ' + Math.max(0, Math.ceil(Gm.dur - st.t)); q('.dsh').innerHTML = `꿈 조각 <b>${st.got}</b>`; if (Gm.hp) q('.dhp').textContent = '♥'.repeat(Math.max(0, st.hp)) + '♡'.repeat(Math.max(0, Gm.hp - st.hp));
   if (st.t >= Gm.dur || st.over) return res(); requestAnimationFrame(fr); }; requestAnimationFrame(fr); });
  removeEventListener('keydown', kd); removeEventListener('keyup', kd);
  // 3) 꿈에서 깼어요
  show('.dbtns', 0); show('.dtip', 0); const got = Math.max(1, st.got), fresh = opt.isNew ? opt.isNew(k) : false;
  q('.dres').innerHTML = `<div class="dbox"><b>꿈에서 깼어요!</b><span>「${NAME[k]}」</span><span>꿈 조각 <i>+${got}</i></span>${fresh ? '<span class="new">꿈 일기장에 새로 적었어요</span>' : ''}<button class="ok">다시 쉬러 가기</button></div>`;
  show('.dres', 1); q('.dres .ok').onclick = () => { ov.remove(); done({ k, got }); };
 });
}
function thumb(k, c){ const g = c.getContext('2d'); g.save(); g.translate(0, -80); D[k](g); g.restore(); }
window.Dream = { LIST, NAME, run, thumb, _G: GAMES };
})();
