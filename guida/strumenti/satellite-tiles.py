import math,os,subprocess,concurrent.futures as cf
from PIL import Image,ImageEnhance
Image.MAX_IMAGE_PIXELS=None
T='/tmp/claude-0/-home-user-sound-system-diaries/f877bfba-9577-5bfb-b24c-4cf9ac9e71c8/scratchpad/s2/t'
N='/tmp/claude-0/-home-user/f877bfba-9577-5bfb-b24c-4cf9ac9e71c8/scratchpad/nmap/'
def tx(lon,z):return (lon+180)/360*2**z
def ty(lat,z):r=math.radians(lat);return (1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*2**z
def get(a):
  z,x,y=a;f=f'{T}/{z}_{x}_{y}.jpg'
  if not os.path.exists(f) or os.path.getsize(f)==0:
    subprocess.run(['curl','-s','-f','--retry','3','-o',f,f'https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg'])
for z,f,out in [(7,1,'sat7s.jpg')]:
  x0,x1=int(tx(3.5,z)),int(tx(20.5,z));y0,y1=int(ty(52,z)),int(ty(29,z))
  J=[(z,x,y) for x in range(x0,x1+1) for y in range(y0,y1+1)]
  with cf.ThreadPoolExecutor(12) as ex:list(ex.map(get,J))
  ts=int(256*f);M=Image.new('RGB',((x1-x0+1)*ts,(y1-y0+1)*ts))
  for (_,x,y) in J:
    p=f'{T}/{z}_{x}_{y}.jpg'
    if os.path.exists(p) and os.path.getsize(p)>0:M.paste(Image.open(p).convert('RGB').resize((ts,ts)),((x-x0)*ts,(y-y0)*ts))
  M=ImageEnhance.Contrast(ImageEnhance.Color(M).enhance(0.8)).enhance(1.08);M.save(N+out,quality=86)
  print(z,x0,y0,M.size)
