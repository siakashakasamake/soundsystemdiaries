const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{
const SITE=path.resolve('site');const list=JSON.parse(fs.readFileSync('og_list5.json','utf8'));
const fontcss=fs.readFileSync('fonts/fonts.css','utf8').replace(/\/fonts\//g,'fonts/');
const tpl=(o)=>`<!doctype html><html><head><meta charset="utf-8"><style>${fontcss}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1200px;height:630px;overflow:hidden;background:#0c0c0b}
.ph{position:absolute;left:0;top:0;width:630px;height:630px;object-fit:cover}
.r{position:absolute;left:630px;top:0;right:0;bottom:0;padding:60px 54px;display:flex;flex-direction:column;justify-content:center;background:radial-gradient(ellipse at 80% 20%,rgba(171,10,5,.25),transparent 60%),#0c0c0b}
.chip{align-self:flex-start;font-family:'Space Mono';font-weight:700;font-size:20px;letter-spacing:.2em;color:#e4d19f;background:#ab0a05;padding:8px 14px;text-transform:uppercase}
.n{font-family:Anton;text-transform:uppercase;color:#e4d19f;line-height:.95;margin-top:26px}
.p{font-family:'Space Mono';font-size:22px;letter-spacing:.16em;text-transform:uppercase;color:#dc9605;margin-top:20px}
.u{position:absolute;left:54px;bottom:46px;font-family:'Space Mono';font-size:18px;letter-spacing:.2em;color:rgba(228,209,159,.6)}
.bar{position:absolute;left:0;right:0;bottom:0;height:12px;background:linear-gradient(to right,#ab0a05 0 33.3%,#dc9605 33.3% 66.6%,#0a5a0a 66.6%)}
.big{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:rgba(12,12,11,.78)}
.grid{position:absolute;inset:0;display:grid;grid-template-columns:repeat(6,1fr);grid-auto-rows:210px;filter:grayscale(.3) brightness(.55)}
.grid img{width:100%;height:100%;object-fit:cover}
</style></head><body>${o}<div class="bar"></div></body></html>`;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});
const shot=async(html,out)=>{fs.writeFileSync(path.join(SITE,'_og.html'),html);await p.goto('file://'+path.join(SITE,'_og.html'));await p.evaluate(()=>document.fonts.ready);
 await p.evaluate(()=>Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r}))));
 await p.evaluate(()=>{const n=document.querySelector('.n');if(!n)return;let fs=96;n.style.fontSize=fs+'px';while((n.scrollHeight>300||n.scrollWidth>n.clientWidth+1)&&fs>40){fs-=4;n.style.fontSize=fs+'px'}});
 await p.screenshot({path:out,type:'jpeg',quality:85});};
for(const o of list){
 const img=o.img?o.img.replace(/^\//,''):'';
 await shot(tpl(`<img class="ph" src="${img}"><div class="r"><span class="chip">Sound System Diaries</span><div class="n">${o.name}</div><div class="p">● ${o.place||'Italia'}</div><div class="u">SOUNDSYSTEMDIARIES.IT</div></div>`),path.join(SITE,'og',o.id+'.jpg'));
}
fs.unlinkSync(path.join(SITE,'_og.html'));await b.close();console.log('og done',list.length+1)})();
