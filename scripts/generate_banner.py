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
    # A single immersive CRT surface; large enough to retain texture on GitHub.
    canvas=Image.new('RGB',(1200,760),'#041226')
    q=ImageDraw.Draw(canvas)
    q.rounded_rectangle((8,8,1191,751),radius=28,fill='#082b54',outline='#208ed0',width=3)
    screen=city.resize((1140,640)).filter(ImageFilter.GaussianBlur(.4))
    canvas.paste(screen,(30,77))
    # Monochrome phosphor avatar retains actual sampled reconstruction motion.
    face=im.crop((54,54,366,366)).resize((450,450),Image.Resampling.NEAREST)
    mono=np.asarray(face.convert('L')).astype(float)/255
    rgb=np.stack([10+mono*125,40+mono*195,80+mono*175],axis=-1).clip(0,255).astype('uint8')
    canvas.paste(Image.fromarray(rgb),(65,130))
    q=ImageDraw.Draw(canvas)
    q.rectangle((62,127,518,583),outline='#54daff',width=2)
    q.rectangle((550,130,1138,580),fill='#082750')
    q.text((65,42),'CYBERWIND // PERSONAL SYSTEM',font=font(20),fill='#8aeeff')
    q.text((930,43),'SIGNAL: ONLINE',font=font(16),fill='#63e9ff')
    q.text((580,152),'ALANSHOWN',font=font(58),fill='#ddf8ff')
    q.text((582,240),'Building tools, systems,',font=font(23),fill='#a5eaff')
    q.text((582,274),'and interactive worlds.',font=font(23),fill='#a5eaff')
    for j,(key,value) in enumerate([('ROLE','INDEPENDENT DEVELOPER'),('FOCUS','INTERACTION / PHYSICS'),('STACK','TYPESCRIPT / PYTHON / C#'),('WORLD','OPEN SOURCE / 3D')]):
        y=345+j*44
        q.text((582,y),key,font=font(15),fill='#409ed3')
        q.text((680,y),value,font=font(18),fill='#b8efff')
    for k in range(42):
        h=int(10+28*(1+math.sin(k*.32+len(frames)*math.tau/96)))
        x=584+k*12
        q.rectangle((x,564-h,x+6,564),fill=(30,155+int(h),255))
    q.rectangle((62,612,1138,693),fill='#06254b',outline='#17669e')
    q.text((84,629),'> reconstruct identity  /  transmit ideas',font=font(20),fill='#74e7ff')
    q.text((84,662),'  BUILD  /  EXPLORE  /  ITERATE',font=font(16),fill='#389cd5')
    q.text((65,719),'PIXEL-DERIVED IDENTITY',font=font(13),fill='#5dc9ef')
    q.text((835,719),'01 / OPEN SOURCE ATELIER',font=font(13),fill='#5dc9ef')
    # Subpixel scanlines are visible at README width, rather than random flicker.
    shade=Image.new('RGB',canvas.size); sd=ImageDraw.Draw(shade)
    for y in range(80,710,4): sd.line((34,y,1165,y),fill=(5,12,17),width=1)
    canvas=ImageChops.subtract(canvas,shade)
    return canvas
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
(A/'banner.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 760"><title>ALANSHOWN — CYBERWIND</title><image width="1200" height="760" xlink:href="data:image/png;base64,{encoded}"/></svg>',encoding='utf-8')
print(json.dumps({'size':(A/'banner.gif').stat().st_size,'frames':len(frames),'dimensions':[1200,760]}))
