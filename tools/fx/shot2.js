const {chromium}=require('/opt/node-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const pg=await b.newPage({viewport:{width:800,height:400}});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
for(const s of process.argv.slice(2)){const [name,rows]=s.split('=');await pg.goto('file:///home/user/magionacademy/tools/fx/preview_sk.html?r='+encodeURIComponent(rows.split('|')[0])+'&f='+encodeURIComponent(rows.split('|')[1]||''));await pg.waitForTimeout(300);await (await pg.$('#c')).screenshot({path:`/tmp/sk_${name}.png`});}
console.log('errs',errs);await b.close()})();
