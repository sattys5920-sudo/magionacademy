const {chromium}=require('/opt/node-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const pg=await b.newPage({viewport:{width:700,height:400}});
const errs=[];pg.on('pageerror',e=>errs.push(e.message));
const sets=process.argv.slice(2);for(const s of sets){const [name,rows]=s.split('=');await pg.goto('file:///home/user/magionacademy/tools/fx/preview.html?r='+rows);await pg.waitForTimeout(300);await (await pg.$('#c')).screenshot({path:`/tmp/fx_${name}.png`});}
console.log('errs',errs);await b.close()})();
