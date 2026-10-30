// 실제 쉬기 화면 위에 꿈 버튼 + 꿈 시작 연출
(function(){
const box=document.querySelector('#rest .rbox'),wake=document.getElementById('rwake');
const line=document.createElement('span');line.className='s';line.innerHTML='오늘 꿀 수 있는 꿈 <b style="color:#D8B4FF">1 / 1</b>';
const btn=document.createElement('button');btn.className='btn sm go';btn.id='rdream';btn.textContent='꿈꾸기';
box.insertBefore(line,wake);box.insertBefore(btn,wake);
window.__dreamGo=()=>{
 line.innerHTML='오늘 꿀 수 있는 꿈 <b style="color:#D8B4FF">0 / 1</b>';
 const ov=document.createElement('div');ov.style.cssText='position:fixed;inset:0;z-index:999;pointer-events:none';
 ov.innerHTML=`<canvas id="dc" width="130" height="281" style="position:absolute;inset:0;width:100%;height:100%;image-rendering:pixelated;opacity:0"></canvas><canvas id="do" width="130" height="281" style="position:absolute;inset:0;width:100%;height:100%;image-rendering:pixelated"></canvas>
 <div id="dt1" style="position:absolute;left:0;right:0;top:120px;text-align:center;font-family:var(--f-pxb);font-size:24px;color:#FFE9A0;opacity:0;transition:opacity .5s">스르륵....</div>
 <div id="dt2" style="position:absolute;left:0;right:0;top:156px;text-align:center;font-family:var(--f-pxb);font-size:14px;color:#F1E9FF;opacity:0;transition:opacity .5s">꿈속으로 빠져들어요</div>
 <div id="dcard" style="position:absolute;left:50%;top:50%;width:230px;height:120px;margin:-60px 0 0 -115px;border-radius:18px;background:rgba(20,12,36,.85);border:3px solid #C8A0FF;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;opacity:0;transform:scale(.6);transition:opacity .4s,transform .4s cubic-bezier(.3,1.5,.5,1);font-family:var(--f-pxb)"><span style="font-size:14px;color:#D8B4FF">오늘의 꿈</span><b id="dnm" style="font-size:26px;color:#FFE9A0">???</b></div>
 <div id="dgo" style="position:absolute;left:0;right:0;top:360px;text-align:center;font-family:var(--f-pxb);font-size:40px;color:#FFE9A0;text-shadow:0 2px 0 #2A1E3A;opacity:0;transition:opacity .3s">시작!</div>`;
 document.body.appendChild(ov);
 const g=ov.querySelector('#dc').getContext('2d'),o=ov.querySelector('#do').getContext('2d'),q=id=>ov.querySelector('#'+id),show=(id,v)=>{q(id).style.opacity=v?1:0;};
 const NAMES=['구름 위 폴짝','과자 나라','거꾸로 바다','별똥별 줍기','양 세기','작아진 나','별빛 기차','무지개 미끄럼틀','비눗방울 톡톡','장난감 상자','달토끼 떡방아','날아라 침대'],KEYS=['jump','candy','sea','stars','sheep','tiny','train','rainbow','bubble','toys','mochi','bed'],PICK=4;
 const lids=k=>{o.clearRect(0,0,W,H);const h=Math.round(H/2*k);o.fillStyle='#0A0612';o.fillRect(0,0,W,h);o.fillRect(0,H-h,W,h);if(k>0&&k<1){o.fillStyle='#3A2A50';o.fillRect(0,h-1,W,1);o.fillRect(0,H-h,W,1);}};
 const swirl=(t,k)=>{R(g,0,0,W,H,'#0A0612');for(let i=0;i<90;i++){const a=i*2.4+t*2.2,r=(1-((i/90+t*.35)%1))*110*(1-k*.3);const x=W/2+Math.cos(a)*r,y=H/2+Math.sin(a)*r*1.1;const c=['#FFF8C8','#C8A0FF','#9AD8FF','#FFB0D0'][i%4];P(g,[[x|0,y|0]],c);if(i%6==0)star(g,x|0,y|0,c);}};
 const bubble=(t,r)=>{swirl(t,1);const cx=W/2,cy=H/2;for(let y=-r;y<=r;y++)for(let x=-r;x<=r;x++){const d=x*x+y*y;if(d<=r*r){const h=(Math.atan2(y,x)/6.28+t*.2+d/(r*r)*.3)%1;g.fillStyle=`hsl(${h*360|0},70%,${78-d/(r*r)*12}%)`;g.fillRect(cx+x,cy+y,1,1);}}g.strokeStyle='rgba(255,255,255,.9)';g.beginPath();g.arc(cx+.5,cy+.5,r,0,6.3);g.stroke();};
 let t0=null;const fr=now=>{if(!t0)t0=now;const t=(now-t0)/1000;
  if(t<1.4){lids(Math.min(1,t/1.2));}
  else if(t<3.2){q('dc').style.opacity=1;lids(0);swirl(t,(t-1.4)/1.8);show('dt1',1);show('dt2',t>1.9);}
  else if(t<4.4){show('dt1',0);show('dt2',0);bubble(t,Math.round(4+(t-3.2)/1.2*40));}
  else if(t<7.4){bubble(t,44);const c=q('dcard');c.style.opacity=1;c.style.transform='scale(1)';const k=t-4.6;q('dnm').textContent=k<0?'???':k<2?NAMES[Math.floor(k*k*3+k*12)%12]:NAMES[PICK];if(t>6.6){c.style.transform='scale(1.12)';c.style.borderColor='#FFE070';}}
  else if(t<8.6){q('dcard').style.opacity=0;const k=Math.min(1,(t-7.4)/.9);bubble(t,Math.round(44+k*130));if(k>=1)D[KEYS[PICK]](g);}
  else{D[KEYS[PICK]](g);show('dgo',t<9.8);}
  if(t<11)requestAnimationFrame(fr);};
 requestAnimationFrame(fr);
};
btn.onclick=()=>window.__dreamGo();
})();
