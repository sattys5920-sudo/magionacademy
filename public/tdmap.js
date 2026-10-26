// 이벤트 「용의 알 지키기」 지도 그림 — 장소 3곳을 도트로 한 번만 그려서(130×147 칸) 크게 늘려 써요 (TD.ZONES 의 길·자리와 같은 좌표)
(function (root, f) { const M = f(); if (typeof module !== 'undefined' && module.exports) module.exports = M; else root.TDMAP = M; })(this, function () {
  const W = 130, H = 147;
  const TREE1 = { trunk: '#7a4e2a', trunk2: '#5a3818', ol: '#173d24', base: '#3e9a46', dark: '#2a7436', light: '#5cba52', hi: '#8adc6a' };
  const TREE2 = { trunk: '#5a4a3e', trunk2: '#3a2e26', ol: '#12302e', base: '#3a8070', dark: '#255a50', light: '#52a68a', hi: '#7ad0aa' };
function hash(x,y,s=0){let h=(x*374761393+y*668265263+s*1274126177)|0;h=(h^(h>>13))*1274126177|0;return((h^(h>>16))>>>0)/4294967295}
function rng(seed){return()=>(seed=(seed*16807)%2147483647)/2147483647}
function mkCanvas(){const c=document.createElement('canvas');c.width=W;c.height=H;return c}
function segDist(px,py,a,b){const dx=b[0]-a[0],dy=b[1]-a[1],l=dx*dx+dy*dy;let t=l?((px-a[0])*dx+(py-a[1])*dy)/l:0;t=Math.max(0,Math.min(1,t));const x=a[0]+dx*t,y=a[1]+dy*t;return Math.hypot(px-x,py-y)}
function pathDist(px,py,pts){let m=1e9;for(let i=1;i<pts.length;i++)m=Math.min(m,segDist(px,py,pts[i-1],pts[i]));return m}
function blob(x,cx,cy,discs,pal,seed){ // 덩어리 여러 개를 합쳐 테두리 · 빛 · 그림자를 입혀요
 const x0=Math.floor(Math.min(...discs.map(d=>d[0]-d[2])))-2,x1=Math.ceil(Math.max(...discs.map(d=>d[0]+d[2])))+2,y0=Math.floor(Math.min(...discs.map(d=>d[1]-d[2])))-2,y1=Math.ceil(Math.max(...discs.map(d=>d[1]+d[2])))+2;
 const w=x1-x0+1,h=y1-y0+1,id=new Int8Array(w*h).fill(-1);
 for(let j=0;j<h;j++)for(let i=0;i<w;i++){const px=x0+i,py=y0+j;for(let k=discs.length-1;k>=0;k--){const[dx,dy,r]=discs[k];if((px-dx)**2+(py-dy)**2<=r*r){id[j*w+i]=k;break}}}
 const at=(i,j)=>i<0||j<0||i>=w||j>=h?-1:id[j*w+i];
 for(let j=0;j<h;j++)for(let i=0;i<w;i++){const k=id[j*w+i];const X=cx+x0+i,Y=cy+y0+j;
  if(k<0){if(at(i-1,j)>=0||at(i+1,j)>=0||at(i,j-1)>=0||at(i,j+1)>=0){x.fillStyle=pal.ol;x.fillRect(X,Y,1,1)}continue}
  const[dx,dy,r]=discs[k];const u=((x0+i)-dx)/r,v=((y0+j)-dy)/r;const l=-(u*.7+v*.9);
  let c=l>.62?pal.hi:l>.18?pal.light:l>-.45?pal.base:pal.dark;
  const hh=hash(X,Y,seed);if(hh<.10&&c!==pal.dark)c=pal.light;else if(hh>.93)c=pal.dark;
  // 다른 덩어리가 위를 덮은 자리 경계는 한 칸 어둡게
  if(at(i,j-1)>=0&&at(i,j-1)!==k&&at(i,j-1)>k)c=pal.dark;
  x.fillStyle=c;x.fillRect(X,Y,1,1)}}
function tree(x,cx,cy,r,pal){
 x.fillStyle='rgba(10,30,10,.30)';for(let j=0;j<4;j++)for(let i=-r;i<=r+3;i++)if((i-2)**2/((r+2)**2)+j*j/9<=1)x.fillRect(cx+i+2,cy+r-1+j,1,1);
 x.fillStyle=pal.ol;x.fillRect(cx-2,cy+r-4,5,6);x.fillStyle=pal.trunk;x.fillRect(cx-1,cy+r-4,3,5);x.fillStyle=pal.trunk2;x.fillRect(cx+1,cy+r-4,1,5);
 blob(x,cx,cy,[[-r*.55,r*.15,r*.72],[r*.55,r*.2,r*.72],[0,-r*.45,r*.8],[0,r*.35,r*.7]].map(d=>[d[0],d[1],d[2]]),pal,cx*7+cy)}
function bush(x,cx,cy,r,pal){blob(x,cx,cy,[[-r*.5,0,r*.7],[r*.5,0,r*.7],[0,-r*.35,r*.75]],pal,cx+cy*3)}
function rock(x,cx,cy,r,col,hi,ol){const pal={ol,hi,light:hi,base:col,dark:shade(col,.7)};blob(x,cx,cy,[[-r*.4,r*.1,r*.7],[r*.45,r*.15,r*.6],[0,-r*.25,r*.75]],pal,cx*3+cy)}
function shade(c,f){const n=parseInt(c.slice(1),16);const r=(n>>16&255)*f|0,g=(n>>8&255)*f|0,b=(n&255)*f|0;return '#'+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1)}
function disc(x,cx,cy,r,col){x.fillStyle=col;for(let j=-r;j<=r;j++)for(let i=-r;i<=r;i++)if(i*i+j*j<=r*r+r*.6)x.fillRect(cx+i|0,cy+j|0,1,1)}
function tuft(x,cx,cy,c1,c2){x.fillStyle=c2;x.fillRect(cx-1,cy,1,2);x.fillRect(cx+1,cy,1,2);x.fillStyle=c1;x.fillRect(cx,cy-1,1,3)}
function paintGround(x,a,b,c,seed,speck){for(let y=0;y<H;y++)for(let i=0;i<W;i++){const h=hash(i,y,seed),q=hash(i>>3,y>>3,seed+5)<.28;x.fillStyle=h<.06?c:(q?(h<.5?b:c):(h<.5?a:b));x.fillRect(i,y,1,1)}
 const r=rng(seed);for(let k=0;k<speck;k++){const i=r()*W|0,j=r()*H|0;x.fillStyle=c;x.fillRect(i,j,2,1);x.fillRect(i,j-1,1,1)}}
function drawPath(x,pts,w,pal){for(let y=0;y<H;y++)for(let i=0;i<W;i++){const d=pathDist(i,y,pts);if(d<=w/2+1.5){let col;if(d>w/2+.2)col=pal.rim;else if(d>w/2-1.2)col=pal.edge;else{const h=hash(i,y,9);col=h<.07?pal.spk:h<.5?pal.a:pal.b}x.fillStyle=col;x.fillRect(i,y,1,1)}}}
function flowers(x,pts,w,cols,n,seed){const r=rng(seed);for(let k=0;k<n;k++){const i=r()*W|0,j=r()*H|0;if(pathDist(i,j,pts)<w/2+3)continue;x.fillStyle=cols[k%cols.length];x.fillRect(i,j,2,2);x.fillStyle='#fff8';x.fillRect(i,j,1,1)}}
function place(n,pts,w,slots,seed,minD,edgeBias){const r=rng(seed),out=[];let t=0;while(out.length<n&&t++<4000){let i=r()*W|0,j=r()*(H+8)|0;if(edgeBias&&r()<.6){if(r()<.5)i=r()<.5?r()*20|0:W-r()*20|0;else j=H-r()*22|0}
 if(pathDist(i,j,pts)<w/2+7)continue;if(slots.some(s=>Math.hypot(s[0]-i,s[1]-j)<15))continue;if(out.some(o=>Math.hypot(o[0]-i,o[1]-j)<minD))continue;out.push([i,j])}return out.sort((a,b)=>a[1]-b[1])}

  const cache = [];
  // 지도 한 장 (장소 번호 0~2) — TD.ZONES 를 받아서 그려요
  function render(zi, Z){
    if (cache[zi]) return cache[zi];
    const c = mkCanvas(), x = c.getContext('2d'), P = Z.path, PW = 15, SL = Z.slots;
    if (zi === 0){ paintGround(x, '#5aa84a', '#52a044', '#3f8a3a', 3, 60); flowers(x, P, PW, ['#fff', '#c9a0ff', '#ffb35a'], 34, 5);
      drawPath(x, P, PW, { rim: '#6b4420', edge: '#8a5c32', a: '#c8995e', b: '#bd8d54', spk: '#a87a46' });
      place(18, P, PW, SL, 7, 24, true).forEach(([i, j]) => tree(x, i, j, i < 14 || j > 128 ? 11 : 9 + (hash(i, j) * 3 | 0), TREE1));
      place(14, P, PW, SL, 19, 16, false).forEach(([i, j], k) => { if (k % 2) bush(x, i, j, 5, TREE1); else tuft(x, i, j, '#6fd05a', '#2f7a3a'); });
      [[12, 40], [116, 104], [20, 110], [84, 30]].forEach(([i, j]) => rock(x, i, j, 5, '#8a8e8a', '#b8bcb4', '#2a2e2a'));
      [[20, 22], [118, 28], [14, 128], [112, 122]].forEach(([i, j]) => { disc(x, i, j, 4, '#4a2e18'); disc(x, i, j, 3, '#8a5a30'); disc(x, i, j, 2, '#b07a44'); });
      disc(x, 100, 3, 9, '#2a1450'); disc(x, 100, 3, 7, '#6a3aa8'); disc(x, 100, 3, 4, '#b48cff'); disc(x, 100, 3, 2, '#fff');
    } else if (zi === 1){ paintGround(x, '#4d6a5e', '#456357', '#33503f', 11, 80);
      drawPath(x, P, PW, { rim: '#3a3a42', edge: '#5a5a64', a: '#a8a8a4', b: '#9a9a98', spk: '#82827e' });
      place(14, P, PW, SL, 13, 22, true).forEach(([i, j], k) => { if (k % 4 == 0) tree(x, i, j, 9, TREE2); else rock(x, i, j, 5 + (hash(i, j) * 4 | 0), '#8a8e96', '#c0c5ce', '#2c2f38'); });
      place(12, P, PW, SL, 29, 16, false).forEach(([i, j], k) => { if (k % 2) bush(x, i, j, 4, TREE2); else tuft(x, i, j, '#7ad0aa', '#255a50'); });
      [[20, 40], [110, 14], [16, 118], [112, 128], [48, 20]].forEach(([i, j]) => { x.fillStyle = '#1d5a7a'; x.fillRect(i - 1, j - 5, 4, 8); x.fillStyle = '#6ad8ff'; x.fillRect(i, j - 6, 2, 8); x.fillStyle = '#d8f6ff'; x.fillRect(i, j - 6, 1, 3); });
      x.fillStyle = '#2c2f38'; x.beginPath(); x.ellipse(64, 150, 22, 18, 0, Math.PI, Math.PI * 2); x.fill(); x.fillStyle = '#0a0810'; x.beginPath(); x.ellipse(64, 150, 17, 14, 0, Math.PI, Math.PI * 2); x.fill();
    } else { paintGround(x, '#6a4638', '#5e3e32', '#46281f', 21, 70);
      const r = rng(33); for (let k = 0; k < 14; k++){ let i = r() * W | 0, j = r() * H | 0; if (pathDist(i, j, P) < PW / 2 + 4) continue; for (let t = 0; t < 14; t++){ i += (r() * 3 | 0) - 1; j += (r() * 3 | 0) - .5; x.fillStyle = t % 4 == 0 ? '#ffd060' : '#ff6a1a'; x.fillRect(i | 0, j | 0, 1, 1); } }
      drawPath(x, P, PW, { rim: '#3a2218', edge: '#7a4c36', a: '#b88460', b: '#aa7854', spk: '#8c5c3c' });
      place(13, P, PW, SL, 23, 22, true).forEach(([i, j]) => rock(x, i, j, 5 + (hash(i, j) * 5 | 0), '#6a5658', '#9a8284', '#241618'));
      place(10, P, PW, SL, 41, 16, false).forEach(([i, j]) => tuft(x, i, j, '#a8745a', '#46281f'));
      [[18, 76], [112, 20], [14, 12], [96, 138]].forEach(([i, j]) => { x.fillStyle = '#e8dcc0'; x.fillRect(i, j, 5, 1); x.fillRect(i + 1, j - 1, 1, 3); x.fillRect(i + 3, j - 1, 1, 3); });
      disc(x, 64, 122, 17, '#2a1a10'); disc(x, 64, 122, 15, '#6a4a2a'); disc(x, 64, 122, 12, '#8a6a3a'); disc(x, 64, 123, 10, '#3a2616');
      const g = x.createRadialGradient(64, 120, 2, 64, 120, 38); g.addColorStop(0, 'rgba(255,200,90,.5)'); g.addColorStop(1, 'rgba(255,170,60,0)'); x.fillStyle = g; x.fillRect(0, 84, W, 63);
    }
    return (cache[zi] = c);
  }
  return { W, H, render };
});
