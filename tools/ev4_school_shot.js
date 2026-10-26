// 유령 등불 찾기 연출 배경: 실제 게임의 학교 화면을 어둡게(lampBoost 0)·밝게(1) 찍어요. 사용: tools/ui_mock.sh 로 서버를 띄운 뒤 node tools/ev4_school_shot.js → sch_dim/lit.png 를 가운데(90,146)~(390,326)에서 잘라 public/art/ev4_school_dim/lit.png 로 저장
const {chromium}=require('/opt/node-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const pg=await b.newPage({viewport:{width:390,height:740},deviceScaleFactor:2});
const seed={players:{u0:{nick:'민준',look:2,house:'dew',coin:9,mana:3,day:4,know:5,inv:{},cr:[],eggs:[],orders:[],hints:[],found:[],fdex:{},rod:1,closet:{},fbag:{},npc:{},ex:{exp:0,d:'',n:0,job:'warrior',wp:2,sp:{},sk:{}},mq:{q:null,st:1,ph:'arrive',prog:{},done:{},named:{},dl:null}}},story:{live:{ch:1,at:1}}};
await pg.addInitScript(([s])=>{window.__seed=s;window.__uid='u0'},[seed]);
await pg.goto('http://localhost:8223/');await pg.waitForTimeout(3500);
for(const [n,v] of [['dim',0],['lit',1]]){await pg.evaluate(v=>{World.lampBoost=v},v);await pg.waitForTimeout(900);await pg.screenshot({path:'sch_'+n+'.png'})}
await b.close()})();
