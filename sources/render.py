"""Offline original Hamster Hour motion graphics. Run from repository root."""
import sys
import pathlib, zipfile
# Vendored wheel is unpacked into disposable scratch; no install or network needed.
_deps = pathlib.Path('test/scratch/pillow')
if not (_deps / 'PIL/Image.py').exists():
    _deps.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(next(pathlib.Path('sources/deps').glob('*.whl'))) as z:
        z.extractall(_deps)
sys.path.insert(0, str(_deps))
from PIL import Image, ImageDraw, ImageFont
import math, subprocess, os, wave, array, random, json
from functools import lru_cache

W=1080; FPS=24; DURATION=40
BG='#0b0d0b'; GREEN='#39ff6a'; TEXT='#f2f0e6'; MUTED='#91ae94'; LINE='#23432a'; SURFACE='#111b13'
@lru_cache(None)
def font(size): return ImageFont.truetype('sources/IBMPlexMono-Regular.ttf',size)
ART={k:Image.open('sources/hamster-'+k+'.png').convert('RGBA') for k in ['happy','asleep','wheel','thumbs']}

def label(draw, text, xy, size=40, color=TEXT, anchor='mm'):
    draw.text(xy,text,font=font(size),fill=color,anchor=anchor,stroke_width=0)
def lines(draw, rows, y, size=54, color=TEXT, leading=1.22):
    for i,s in enumerate(rows): label(draw,s,(540,y+i*size*leading),size,color)
def box(d,rect,fill=SURFACE,outline=LINE,width=2): d.rounded_rectangle(rect,radius=10,fill=fill,outline=outline,width=width)
def paste(im,art,cx,cy,size):
    src=ART[art]; h=int(size*src.height/src.width)
    a=src.resize((int(size),h),Image.Resampling.LANCZOS); im.paste(a,(int(cx-size/2),int(cy-h/2)),a)
def cap(im,cx,cy,size):
    # Green cap overlay keeps the recurring site character in the requested outfit.
    d=ImageDraw.Draw(im); x=cx-size*.23; y=cy-size*.35
    d.rectangle((int(x),int(y),int(cx+size*.21),int(y+size*.085)),fill='#226e36')
    d.rectangle((int(x+size*.04),int(y-size*.045),int(cx+size*.16),int(y)),fill=GREEN)
    d.rectangle((int(cx-size*.31),int(y+size*.08),int(cx+size*.24),int(y+size*.12)),fill=GREEN)
def mascot(im,art,cx,cy,size,hat=True):
    paste(im,art,cx,cy,size)
    if hat and art!='wheel': cap(im,cx,cy,size)

def robot(d,cx,cy,idx,verified):
    c=GREEN if verified else MUTED
    d.line((cx,cy-78,cx,cy-108),fill=c,width=4);d.ellipse((cx-7,cy-118,cx+7,cy-104),fill=c)
    box(d,(cx-92,cy-76,cx+92,cy+65),outline=c,width=3)
    d.rectangle((cx-58,cy-35,cx-32,cy-10),fill=c);d.rectangle((cx+32,cy-35,cx+58,cy-10),fill=c)
    d.line((cx-45,cy+26,cx+45,cy+26),fill=c,width=5)
    label(d,'AI '+str(idx),(cx,cy+105),25,MUTED)
    if verified:
        box(d,(cx-100,cy+143,cx+100,cy+188),fill=GREEN,outline=GREEN)
        label(d,'SIGNED',(cx,cy+166),26,BG)


def scene(t):
    if t<4:return 0,t
    if t<9:return 1,t-4
    if t<14:return 2,t-9
    if t<18:return 3,t-14
    if t<23:return 4,t-18
    if t<30:return 5,t-23
    if t<35:return 6,t-30
    return 7,t-35

BASE={}
def frame(t,vertical=False):
    H=1920 if vertical else 1080
    if H not in BASE:
        im=Image.new('RGB',(1080,H),BG);d=ImageDraw.Draw(im)
        for x in range(0,1080,40): d.line((x,0,x,H),fill='#102016')
        for y in range(0,H,40): d.line((0,y,1080,y),fill='#102016')
        BASE[H]=im
    im=BASE[H].copy();d=ImageDraw.Draw(im)
    # All primary content is designed separately for portrait and square.
    top=325 if vertical else 160
    mid=950 if vertical else 570
    bottom=1530 if vertical else 925
    header=155 if vertical else 54
    mascot(im,'happy',82,header,67)
    label(d,'HAMSTER HOUR',(140,header),26,GREEN,'lm')
    label(d,'ONE WHEEL. EVERY HOUR.',(1030,header),20,MUTED,'rm')
    d.line((50,header+48,1030,header+48),fill=LINE,width=2)
    idx,u=scene(t)
    if idx==0:
        lines(d,['this hamster is','the whole protocol'],top,62)
        # The site wheel still bobs, while a separate ring visibly turns.
        paste(im,'wheel',540,mid+5+4*math.sin(t*15),900)
        wx=540-450+900*206/360; wy=mid+5-350+700*128/280
        for k in range(8):
            a=t*2.9+k*math.pi/4
            x=wx+257*math.cos(a);y=wy+257*math.sin(a)
            d.ellipse((x-5,y-5,x+5,y+5),fill=GREEN)
        box(d,(110,bottom-42,970,bottom+61))
        label(d,'Squeektoshi / real hamster / livestream',(540,bottom-6),31,GREEN)
        label(d,'A sensor counts every wheel pass.',(540,bottom+35),29,MUTED)
    elif idx==1:
        lines(d,['every hour:','OVER or UNDER the line?'],top,55)
        # Moving graph, intentionally illustrative rather than fake live data.
        gy=mid-180
        box(d,(85,gy,995,gy+345))
        label(d,'WHEEL PASSES  /  ILLUSTRATION',(120,gy+32),22,MUTED,'lm')
        for k in range(4):d.line((120,gy+85+k*65,960,gy+85+k*65),fill=LINE,width=1)
        liney=gy+190;d.line((120,liney,960,liney),fill=GREEN,width=3)
        label(d,'THE LINE',(930,liney-24),25,GREEN,'rm')
        pts=[]
        for i in range(int(min(u/3,1)*96)+1):
            x=120+i*8.5;y=gy+290-i*2.1+14*math.sin(i*.18)
            pts.append((x,y))
        if len(pts)>1:d.line(pts,fill=TEXT,width=6)
        label(d,'OVER',(300,gy+390),44,GREEN);label(d,'UNDER',(790,gy+390),44,TEXT)
        label(d,'One hour. One betting window.',(540,bottom),32,TEXT)
    elif idx==2:
        lines(d,['or bet SLEEPING.'],top,65,GREEN)
        lines(d,['half the day,','it is the right call.'],top+86,43)
        # A seamless breathing loop, also used for the GIF.
        size=460+8*math.sin(2*math.pi*u/3)
        mascot(im,'asleep',520,mid+20,size)
        for k in range(3):
            a=(u/3+k/3)%1
            label(d,'z',(745+a*90,mid-70-a*160),int(30+a*26),GREEN)
        box(d,(238,bottom-49,842,bottom+55),outline=GREEN)
        label(d,'SLEEPING = ZERO PASSES',(540,bottom+3),34,GREEN)
    elif idx==3:
        lines(d,['EXACT: guess the number.'],top,52,GREEN)
        lines(d,['closest three','share the pool.'],top+85,48)
        for k,(val,pos) in enumerate([('1,247',280),('1,248',540),('1,249',800)]):
            yy=mid+(0 if k==1 else 34)
            box(d,(pos-116,yy-90,pos+116,yy+110),outline=GREEN if k==1 else LINE,width=3)
            label(d,val,(pos,yy-22),42,GREEN if k==1 else TEXT)
            label(d,'#'+str(k+1),(pos,yy+65),28,MUTED)
        label(d,'THREE CLOSEST GUESSES',(540,mid+190),29,GREEN)
        label(d,'The tiny spreadsheet division.',(540,bottom),30,MUTED)
        label(d,'Illustrative guesses',(540,bottom+48),20,MUTED)
    elif idx==4:
        lines(d,['pick a side. bet $IMD.'],top,56)
        lines(d,['Bets close when the hour starts.'],top+86,32,GREEN)
        by=mid-190
        label(d,'NEXT HOUR STARTS IN',(540,by-60),25,MUTED)
        countdown=max(0,4-int(u))
        label(d,'00:00:0'+str(countdown),(540,by+3),62,GREEN)
        for k,name in enumerate(['OVER','UNDER','SLEEPING']):
            x=72+k*318;selected=(u>=1 and k==2)
            box(d,(x,by+78,x+300,by+258),fill='#1a3821' if selected else SURFACE,outline=GREEN if selected else LINE,width=3)
            label(d,name,(x+150,by+130),32,GREEN)
            label(d,['> LINE','< LINE','0 PASSES'][k],(x+150,by+182),25,MUTED)
            if selected: label(d,'SELECTED',(x+150,by+226),20,TEXT)
        state='BETS CLOSED' if u>=4 else ('DEMO BET PLACED' if u>=2.1 else 'BET 10 $IMD')
        box(d,(155,by+305,925,by+392),fill=GREEN,outline=GREEN)
        label(d,state,(540,by+349),36,BG)
        label(d,'UI recreation / demo bet / no transaction',(540,bottom),23,MUTED)
    elif idx==5:
        lines(d,['verified by','the IMD oracle.'],top,60)
        # First seconds show wheel data flowing to agents; final seconds show signatures.
        label(d,'PUBLISHED WHEEL DATA',(540,mid-245),29,GREEN)
        d.line((210,mid-190,870,mid-190),fill=LINE,width=3)
        for k,cx in enumerate([220,540,860]):
            d.line((cx,mid-190,cx,mid-120),fill=GREEN,width=3)
            a=(u*.7+k*.25)%1;d.ellipse((cx-5,mid-190+a*60-5,cx+5,mid-190+a*60+5),fill=TEXT)
            robot(d,cx,mid,k+1,u>1.7+k*.55)
        if u<3.6:
            lines(d,['A panel of AI agents checks','the published wheel data.'],bottom-20,32)
        else:
            lines(d,['Agents sign the result on Ethereum.','No admin presses a button.'],bottom-20,32,GREEN)
    elif idx==6:
        lines(d,['winners split the pool.'],top,56)
        label(d,'PARI-MUTUEL / BETS IN $IMD',(540,top+83),28,MUTED)
        # Animated 91/9 bar never implies fixed odds or a guaranteed return.
        p=min(1,u/1.2)
        box(d,(90,mid-100,990,mid+40))
        d.rectangle((100,mid-90,100+int(880*.91*p),mid+30),fill=GREEN)
        if p>0.99:d.rectangle((906,mid-90,980,mid+30),fill='#53775c')
        label(d,'91%',(420,mid-30),84,BG if p>.5 else TEXT)
        label(d,'TO WINNERS',(420,mid+100),40,GREEN)
        label(d,'9%: stakers, oracle reserve + team',(540,mid+196),29,MUTED)
        mascot(im,'thumbs',170,bottom,100)
        label(d,'One pool. Many tiny victory laps.',(605,bottom),27,TEXT)
    else:
        mascot(im,'happy',540,mid-80,330)
        lines(d,['bet on the hamster'],top,59,GREEN)
        label(d,'hamsterhour.fun',(540,mid+190),65,TEXT)
        # The X URL appears only on this end card.
        label(d,'https://x.com/hamsterhourgame',(540,mid+260),26,MUTED)
        label(d,'Lose a bet. Earn $HAMSTER.',(540,bottom),37,GREEN)
        label(d,'lose to earn / coming soon',(540,bottom+62),28,MUTED)
    # Chapter marks and timeline supply a persistent, quiet motion cue.
    d.line((50,H-55,1030,H-55),fill=LINE,width=3)
    d.line((50,H-55,50+980*t/40,H-55),fill=GREEN,width=3)
    label(d,f'{idx+1:02d} / 08',(1030,H-27),17,MUTED,'rm')
    # A short cut-flash makes scene changes legible without obscuring captions.
    if u<.14 and t>.2:
        d.rectangle((0,0,1080,7),fill=GREEN)
    return im


def audio(path):
    rate=32000; n=rate*40; samples=array.array('f',[0])*n
    rng=random.Random(240)
    def add(start,dur,fn,gain):
        a=int(start*rate); count=min(int(dur*rate),n-a)
        for k in range(max(0,count)):
            x=k/rate; samples[a+k]+=gain*fn(x,dur)
    def tone(freq):
        return lambda x,d: math.sin(2*math.pi*freq*x)*min(1,x/.008)*math.exp(-x*5)
    # Original 80 BPM chiptune / lo-fi bed, one repeating four-bar progression.
    beat=.75
    roots=[130.8128,103.8262,155.5635,116.5409]
    for b in range(54):
        start=b*beat; root=roots[(b//4)%4]
        add(start,.45,tone(root/2),.15)
        if b%2==0:add(start,.19,lambda x,d:math.sin(2*math.pi*(54*x+5*(1-math.exp(-x*28))))*math.exp(-x*23),.18)
        else:add(start,.12,lambda x,d:(rng.random()*2-1)*math.exp(-x*38),.07)
        add(start+.375,.065,lambda x,d:(rng.random()*2-1)*math.exp(-x*75),.025)
        for factor in [1,1.189207,1.498307]:add(start,1.1,tone(root*factor*2),.022)
        melody=root*[4,3,2.378414,3,4,2.996614,2.378414,2][b%8]
        add(start+.05,.36,lambda x,d,f=melody:(math.sin(2*math.pi*f*x)+.20*math.sin(6*math.pi*f*x))*math.exp(-x*9)*min(1,x/.012),.055)
    # Wheel squeaks, soft UI clicks, sleepy snore, signing stamps, cash register.
    for start in [.6,1.65,2.7]:add(start,.16,lambda x,d:math.sin(2*math.pi*(1050*x+170*x*x))*math.sin(math.pi*x/d)**2,.045)
    for start in [9.5,11.7]:add(start,1.2,lambda x,d:(math.sin(2*math.pi*83*x)+.5*math.sin(2*math.pi*169*x))*(.5+.5*math.sin(2*math.pi*8*x))*math.sin(math.pi*x/d)**2,.08)
    for start in [19,20.1,24.7,25.25,25.8]:add(start,.09,lambda x,d:math.sin(2*math.pi*420*x)*math.exp(-x*55),.12)
    for start,freq in [(30.6,1318.51),(30.73,1760),(30.88,2093)]:add(start,.7,tone(freq),.11)
    data=array.array('h')
    for i,s in enumerate(samples):
        fade=min(1,i/(rate*.25),(n-i)/(rate*.6))
        data.append(int(max(-.94,min(.94,s*1.3*fade))*32767))
    with wave.open(path,'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(data.tobytes())


def render(out,vertical=False):
    H=1920 if vertical else 1080
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'1080x{H}','-r',str(FPS),'-i','pipe:0','-i','test/scratch/sound.wav','-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','22','-maxrate','2400k','-bufsize','4800k','-pix_fmt','yuv420p','-af','loudnorm=I=-18:TP=-1.5:LRA=7','-c:a','aac','-b:a','128k','-ar','48000','-movflags','+faststart','-t','40',out]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(FPS*DURATION):
        p.stdin.write(frame(i/FPS,vertical).tobytes())
        if i%120==0: print(out, i/FPS,flush=True)
    p.stdin.close()
    if p.wait():raise RuntimeError('ffmpeg failed')

if __name__=='__main__':
    os.makedirs('test/scratch',exist_ok=True);os.makedirs('artifacts',exist_ok=True)
    if '--stills' in sys.argv:
        for t in [1.5,6,11,15.5,20,27,32,37]:
            frame(t).save(f'test/scratch/scene-{t}.png')
            frame(t,True).save(f'test/scratch/vertical-{t}.png')
    else:
        audio('test/scratch/sound.wav')
        render('artifacts/video.mp4')
        os.makedirs('media',exist_ok=True)
        render('media/video-vertical.mp4',True)
        # Exactly 3 seconds with matching endpoints: 15 fps, 480 px, breathing + z loop.
        gif=[]
        for i in range(45):
            im=frame(9+i/15).resize((480,480),Image.Resampling.LANCZOS)
            # Crop progress footer away so it cannot jump across the loop.
            ImageDraw.Draw(im).rectangle((0,450,480,480),fill=BG)
            ImageDraw.Draw(im).rectangle((0,0,480,4),fill=BG)
            gif.append(im)
        palette=gif[0].quantize(colors=64)
        gif=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in gif]
        gif[0].save('media/sleeping.gif',save_all=True,append_images=gif[1:],duration=[70,70,60]*15,loop=0,optimize=True,disposal=1)
