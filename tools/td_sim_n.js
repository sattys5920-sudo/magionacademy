// 디펜스 이벤트 균형 시뮬(전체 인원): node tools/td_sim_n.js <전체 인원> <판 수> <몬스터 체력 배율>  (환경변수 GK 골드·DM 피해·BN 웨이브 보너스로 조절)
const TD=require('../public/td.js');
if(process.env.GK)TD.K.gold=+process.env.GK;if(process.env.DM)TD.K.dmg=+process.env.DM;if(process.env.BN)TD.K.bonus=+process.env.BN;const PER=+process.argv[2]||3, N=+process.argv[3]||40, HPK=+process.argv[4]||1;
const JOBS=[['warrior','black','white'],['knight','summon','druid'],['thief','gadget','cleric'],['warrior','alch','bard'],['knight','time','white'],['thief','black','druid']];
function run(seed){let r=seed;const rnd=()=>(r=(r*16807)%2147483647)/2147483647;
 const pl=[];for(let n=0;n<PER;n++){const z=n%3,i=Math.floor(n/3);pl.push({uid:z+'_'+i,zone:z,slot:i,job:JOBS[(z*3+i+seed)%6][(i+n)%3]})}
 const S=TD.newState(pl,{hpK:HPK});TD.startWave(S);let tt=0,spent=0;
 while(S.phase!=='over'&&tt<9000){TD.step(S,.1);tt+=.1;
  if((tt*10|0)%20===0)Object.values(S.players).forEach(p=>{const opts=[];for(let i=0;i<2;i++)for(const k of['pow','rng','cd']){const c=TD.upCost(p,i,k);if(c!=null&&p.gold>=c)opts.push([i,k,c])}
   if(opts.length&&rnd()<.7){const o=opts[rnd()*opts.length|0];TD.upgrade(S,p.uid,o[0],o[1]);spent+=o[2]}})}
 const earned=Object.values(S.players).reduce((a,p)=>a+p.earned,0)/pl.length;
 return {kz:S.kz,win:S.win?1:0,wave:S.wave,eggs:S.eggs.map(Math.round),earned:Math.round(earned),leaks:S.leaks,t:Math.round(tt)}}
const R=[];for(let i=1;i<=N;i++)R.push(run(i*7919));
const avg=f=>Math.round(R.reduce((a,x)=>a+f(x),0)/R.length*10)/10;
const kz=R.reduce((a,x)=>a.map((v,i)=>v+x.kz[i]),[0,0,0]),kt=kz.reduce((a,b)=>a+b)||1;console.log('처치 비율 숲길/입구/둥지앞',kz.map(v=>Math.round(v/kt*100)+'%').join(' / '));console.log('팀당',PER,'명 hpK',HPK,'승',Math.round(R.reduce((a,x)=>a+x.win,0)/R.length*100)+'%','도달 웨이브',avg(x=>x.wave),'남은 알 합',avg(x=>x.eggs.reduce((a,b)=>a+b,0)),'1인 번 골드',avg(x=>x.earned),'새어나간 수',avg(x=>x.leaks),'시간(초)',avg(x=>x.t));
