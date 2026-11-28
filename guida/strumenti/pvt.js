const {chromium}=require('playwright');const path=require('path');
(async()=>{const [dir,html,out,ts]=process.argv.slice(2);const br=await chromium.launch({args:['--disable-gpu']});const p=await br.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.join(dir,html));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);
for(const t of ts.split(',')){await p.evaluate(t=>render(t),+t);await p.waitForTimeout(150);await p.screenshot({path:path.join(dir,out,`t${(+t).toFixed(2).padStart(6,'0')}.jpg`),type:'jpeg',quality:88})}
await br.close()})();
