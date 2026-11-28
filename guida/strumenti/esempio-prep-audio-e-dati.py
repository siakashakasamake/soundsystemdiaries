import json,subprocess,numpy as np,wave,re
P='/tmp/claude-0/-home-user/f877bfba-9577-5bfb-b24c-4cf9ac9e71c8/scratchpad/nmap'
R='/home/user/sound-system-diaries/'
E=[e for e in json.load(open(R+'data/events.json'))['items'] if '2026-11-27'<=e['date']<='2026-11-29']
from PIL import Image
import os
os.makedirs(P+'/fl2',exist_ok=True)
E.sort(key=lambda e:(e['date'],-e['lat']))
for i,e in enumerate(E):
  src=R+('static'+e['flyer'] if e['flyer'].startswith('/img') else e['flyer'][1:]);im=Image.open(src).convert('RGB');im.thumbnail((700,900));im.save(f'{P}/fl2/{i}.jpg',quality=90)
EV=[dict(fl=f"fl2/{i}.jpg",t=e['title'],v=e['venue'],c=e['city'],h=e['time'],l=e['lineup'],en=e['entry'],d=e['date'],lat=e['lat'],lon=e['lon']) for i,e in enumerate(E)]
DOTS=[[s['lat'],s['lon']] for s in json.load(open(R+'data/sounds.json'))['items'] if s['lat']]
a=open('/tmp/claude-0/-home-user-sound-system-diaries/f877bfba-9577-5bfb-b24c-4cf9ac9e71c8/scratchpad/atl/data.js').read()
POLY=re.search(r'const POLY=(\[.*?\]);const LV',a).group(1)
IN=3;PER=2.5;OUT=4;NB=IN+len(EV)*PER+OUT;B=0.894;DUR=NB*B;SR=44100;off=1.574+230*B
raw=subprocess.run(['ffmpeg','-v','0','-ss',str(off),'-t',str(DUR+0.2),'-i','/tmp/claude-0/-home-user-sound-system-diaries/f877bfba-9577-5bfb-b24c-4cf9ac9e71c8/scratchpad/stasera/a.wav','-ac','2','-ar',str(SR),'-f','s16le','-'],capture_output=True).stdout
mus=np.frombuffer(raw,np.int16).reshape(-1,2).astype(np.float32)/32768
n=len(mus);t=np.arange(n)/SR;fx=np.zeros(n,np.float32);rng=np.random.default_rng(6)
def whoosh(a,b,g=0.14):
  s=slice(int(a*SR),min(n,int(b*SR)));L=s.stop-s.start;z=np.convolve(rng.normal(0,1,L),np.ones(30)/30,'same');fx[s]+=(z*np.sin(np.pi*np.linspace(0,1,L))**1.5*g*3).astype(np.float32)
def ping(a,fs=(880,1320),g=0.12,d=0.6):
  s=slice(int(a*SR),min(n,int((a+d)*SR)));L=s.stop-s.start;k=np.arange(L)/SR;fx[s]+=(sum(np.sin(2*np.pi*f*k)*np.exp(-k*(6+i*3)) for i,f in enumerate(fs))*g).astype(np.float32)
for i in range(len(EV)):
  b=IN+i*PER;whoosh((b-0.2)*B,(b+0.8)*B);ping(b*B+0.95,(784+i*40,1175+i*40))
whoosh((IN+len(EV)*PER-0.2)*B,(IN+len(EV)*PER+1)*B,0.2)
out=mus*0.85+np.stack([fx,fx],1);out=out/np.max(np.abs(out))*0.95;out*=np.clip((DUR-t)/1.3,0,1)[:,None];out*=np.clip(t/0.2,0,1)[:,None]
w=wave.open(P+'/tune.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
mm=np.abs(np.convolve(mus[:,0],np.ones(400)/400,'same'))[::1470][:int(DUR*30)+2]
LV=(mm/np.percentile(mm,98)).clip(0,1).round(3).tolist()
open(P+'/data.js','w').write('const EV='+json.dumps(EV,ensure_ascii=False)+';const DOTS='+json.dumps(DOTS)+';const POLY='+POLY+';const LV='+json.dumps(LV)+';const B=0.894;const NB='+str(NB)+',IN='+str(IN)+',PER='+str(PER)+',OUT='+str(OUT)+';')
print(NB,round(DUR,1),int(DUR*30)+1,[(e['c'],e['d']) for e in EV])
