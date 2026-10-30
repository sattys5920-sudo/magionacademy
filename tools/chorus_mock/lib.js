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
