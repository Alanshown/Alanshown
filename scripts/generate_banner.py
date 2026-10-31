"""Deterministic, image-derived CYBERWIND renderer. No network needed."""
from pathlib import Path
import base64, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assets'
(A/'source').mkdir(parents=True, exist_ok=True)
if not (A/'source/avatar.png').exists():
    (A/'source/avatar.png').write_bytes(base64.b64decode((A/'source/avatar.b64').read_text()))
W,H=1200,400
rng=np.random.default_rng(42)
# Luminous atmospheric depth, brightest behind the skyline.
Y,X=np.mgrid[0:H,0:W]
haze=np.exp(-((X-760)/570)**2-((Y-210)/175)**2)
a=np.zeros((H,W,3),dtype=np.uint8)
for channel,(base,gain) in enumerate([(4,8),(26,73),(65,130)]): a[:,:,channel]=base+haze*gain
city=Image.fromarray(a); d=ImageDraw.Draw(city)
for layer,base,count in [(0,245,36),(1,300,24),(2,390,16)]:
    for j in range(count):
        x=int(j*W/count+rng.integers(-15,15)); bw=int(rng.integers(24,65)); top=int(base-rng.integers(60,160))
        col=[(12,51,100),(8,39,83),(7,29,65)][layer]
        d.polygon([(x,base),(x,top+12),(x+bw//3,top),(x+bw,top+8),(x+bw,base)],fill=col)
        d.line([(x,top+12),(x+bw//3,top),(x+bw,top+8),(x+bw,base)],fill=(32,135+layer*30,245),width=1)
        for yy in range(top+20,base-5,11):
            for xx in range(x+5,x+bw-3,8):
                if rng.random()>.35: d.rectangle((xx,yy,xx+2,yy+3),fill=(25,75+layer*20,int(rng.integers(120,200))))
        if j%4==0: d.line((x+bw//3,top,x+bw//3,top-17),fill='#317da0')
for k in range(16):
    y=310+k*6
    d.line([(0,y),(390,y-35),(720,y-10),(1200,y-60)],fill=(14,50+k*3,80+k*5),width=1)
# Perspective boulevard and reflected neon establish the city vanishing point.
for x in range(-1000,2400,150):
    d.line([(730,255),(x,400)],fill=(17,103,188),width=1)
for y in [280,301,330,370,399]: d.line((0,y,W,y),fill=(16,91,166),width=1)
light=Image.new('RGB',(W,H)); ld=ImageDraw.Draw(light)
for k in range(7):
    pts=[(x,int(290+k*9-48*math.sin(x/450+k*.08))) for x in range(W)]
    ld.line(pts,fill=(20,120+k*15,255),width=2 if k%2 else 3)
from PIL import ImageChops
city=ImageChops.add(city,light.filter(ImageFilter.GaussianBlur(12)))
city=ImageChops.add(city,light)
city.save(A/'source/city.png')
avatar=Image.open(A/'source/avatar.png').convert('RGB').resize((310,310))
scene=city.copy(); scene.paste(avatar,(55,55))
# Actual color, brightness, gradient, alpha, coordinates, region and depth.
small=np.asarray(scene.resize((200,67))).astype(float)
lum=small@np.array([.2126,.7152,.0722]); gy,gx=np.gradient(lum); edge=np.hypot(gx,gy)
yy,xx=np.indices(lum.shape); region=(xx<62)&(xx>8)&(yy>8)&(yy<61)
alpha=np.where(region,np.clip(1-((xx-35)/28)**8,0,1),1)
depth=np.clip(yy/67,0,1)
np.savez_compressed(A/'source/pixel-grid.npz',color=small.astype('uint8'),brightness=lum,gradient=edge,alpha=alpha,x=xx,y=yy,region=region,depth=depth)
def font(size):
    for p in ['C:/Windows/Fonts/consolab.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf']:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default(size=size)
def label(im):
    q=ImageDraw.Draw(im)
    q.rounded_rectangle((423,68,1175,249),radius=8,fill='#082953',outline='#166aab',width=1)
    q.text((450,78),'CYBERWIND   /   OPEN SOURCE ATELIER',font=font(13),fill='#42bfff')
    q.text((445,108),'ALANSHOWN',font=font(62),fill='#ddf8ff')
    q.text((450,187),'Building tools, systems,',font=font(19),fill='#b3d2e5')
    q.text((450,214),'and interactive worlds.',font=font(19),fill='#b3d2e5')
    q.text((55,25),'01 / IDENTITY IN MOTION',font=font(12),fill='#63e9ff')
    q.text((450,351),'TYPE / SYSTEMS / PHYSICS / WORLDS',font=font(13),fill='#63e9ff')
    return im
frames=[]
for f in range(96):
    t=f/96
    # Reversible envelope makes both sides of the loop identical, without a blackout.
    strength=math.sin(math.pi*t)**2
    phase=min(t,1-t)*2
    out=city.copy(); q=ImageDraw.Draw(out)
    for y in range(67):
        for x in range(200):
            av=region[y,x]; e=min(edge[y,x]/50,1); b=lum[y,x]/255
            delay=(.1+.45*(1-e)+.15*(1-b)) if av else (.3+.3*depth[y,x]+.15*(1-e))
            settled=np.clip((phase-delay)*5,0,1)
            if av: settled=.65+.35*settled
            color=small[y,x]*settled
            if not av: color=small[y,x]*(.78+.22*settled)
            drift=(1-settled)*strength
            dx=int(drift*(120+70*math.sin(y*.1+x*.04)))
            dy=int(drift*(-25+20*math.sin(x*.08)))
            if f in (70,71) and y%13==0: dx+=10
            px=x*6+dx; py=y*6+dy
            q.rectangle((px,py,px+5,py+5),fill=tuple(int(c) for c in color)) if av or (e>.35 and strength>.35) else None
    for k in range(90):
        x=k%45+12; y=(k*17)%49+10; v=small[y,x]; u=(t*2+k/90)%1
        px=320+int(u*700); py=245+int(35*math.sin(u*4+k*.12))-int(u*90)
        q.rectangle((px,py,px+2,py+1),fill=tuple(int(c*.5) for c in v))
    # Flowing comet streaks, with periodic motion to preserve loop continuity.
    for k in range(12):
        u=(t+k/12)%1; px=int(380+u*820); py=int(291-48*math.sin(px/450)+k*5)
        q.line((px-32,py+3,px,py),fill=(38,170,255),width=2)
        q.rectangle((px,py,px+3,py+1),fill='#b4faff')
    frames.append(label(out))
palette=frames[48].quantize(colors=256)
quant=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
quant[0].save(A/'banner.gif',save_all=True,append_images=quant[1:],duration=90,loop=0,optimize=False,disposal=1)
frames[48].save(A/'banner.png')
encoded=base64.b64encode((A/'banner.png').read_bytes()).decode()
(A/'banner.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}"><title>ALANSHOWN — CYBERWIND</title><image width="{W}" height="{H}" xlink:href="data:image/png;base64,{encoded}"/></svg>',encoding='utf-8')
print(json.dumps({'size':(A/'banner.gif').stat().st_size,'frames':len(frames),'dimensions':[W,H]}))
