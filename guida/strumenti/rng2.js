const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const [dir,html,out,a,b]=process.argv.slice(2);const br=await chromium.launch({args:['--disable-gpu']});const p=await br.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.join(dir,html));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);
for(let w=Math.max(0,+a-75);w<+a;w++){await p.evaluate(t=>render(t),w/30)}for(let k=+a;k<+b;k++){const f=path.join(dir,out,`f${String(k).padStart(5,'0')}.jpg`);if(fs.existsSync(f))continue;await p.evaluate(t=>render(t),k/30);await p.screenshot({path:f,type:'jpeg',quality:90})}
await br.close()})();
