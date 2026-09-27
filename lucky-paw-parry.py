# title: Lucky Cat: Paw Parry
# desc: Time the raised paw to bounce paper lanterns into the bowl.
import pyxel,math,random
# Shared Lucky Cat maneki-neko mark. Warm paper, charcoal ink, restrained red, gold coin.
# The figurine silhouette (raised paw, coin, collar, whiskers) follows Jacob's brand brief.

INK=1; PAPER=7; RED=8; GOLD=10

def cat(cx,cy,scale=1,wave=0):
    # all geometry integer-scaled; no invented mascot or gradient
    def rect(x,y,w,h,c):pyxel.rect(cx+x*scale,cy+y*scale,w*scale,h*scale,c)
    def line(x,y,xx,yy,c):pyxel.line(cx+x*scale,cy+y*scale,cx+xx*scale,cy+yy*scale,c)
    def circ(x,y,r,c):pyxel.circ(cx+x*scale,cy+y*scale,max(1,r*scale),c)
    # body and tucked tail
    circ(-13,18,5,INK);circ(-13,18,3,PAPER)
    rect(-12,5,25,28,INK);rect(-10,5,21,26,PAPER)
    circ(0,7,13,INK);circ(0,8,11,PAPER)
    # pointed ears and round face
    pyxel.tri(cx-12*scale,cy+1*scale,cx-10*scale,cy-12*scale,cx-1*scale,cy-7*scale,INK)
    pyxel.tri(cx+3*scale,cy-7*scale,cx+12*scale,cy-12*scale,cx+12*scale,cy+1*scale,INK)
    pyxel.tri(cx-10*scale,cy-1*scale,cx-9*scale,cy-8*scale,cx-5*scale,cy-5*scale,RED)
    pyxel.tri(cx+6*scale,cy-5*scale,cx+10*scale,cy-8*scale,cx+10*scale,cy-1*scale,RED)
    circ(-5,7,1,INK);circ(5,7,1,INK);circ(0,10,1,RED)
    line(-3,12,0,13,INK);line(0,13,3,12,INK)
    for y in (9,12):line(-10,y,-16,y-1,INK);line(10,y,16,y-1,INK)
    # red collar, bell; gold only appears on the koban
    rect(-9,17,18,3,RED);circ(0,20,2,INK)
    circ(0,27,5,INK);circ(0,27,4,GOLD);line(-2,27,2,27,INK)
    # iconic raised right paw, gently animated
    up=int(bool(wave));rect(11,-2-up*3,6,19,INK);rect(12,-1-up*3,4,16,PAPER)
    circ(14,-4-up*3,4,INK);circ(14,-4-up*3,2,PAPER)

W,H=256,192
random.seed(29)
class Game:
 def __init__(self):
  pyxel.init(W,H,title='Lucky Cat Paw Parry',fps=30)
  self.reset();pyxel.sounds[0].mml('T250 O4 C8 G8');pyxel.sounds[1].mml('T130 O3 C8 R8 C8');pyxel.run(self.update,self.draw)
 def reset(self):
  self.state='title';self.frame=0;self.score=0;self.combo=0;self.hearts=4;self.objects=[];self.parry=0;self.shake=0;self.wave=0;self.step=0;self.spawn_timer=0;self.saved=0
  self.patterns=('CCFCCFCCFC','CFCCFCCFCF','CCFCCFCFCC')
 def next_wave(self):
  self.wave+=1;self.step=0;self.spawn_timer=0;self.objects=[];self.parry=0;self.state='playing'
 def update(self):
  if self.state!='playing':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
    if self.state=='clear':self.next_wave()
    else:self.reset();self.state='playing'
   return
  self.frame+=1
  if self.parry:self.parry-=1
  if self.shake:self.shake-=1
  self.spawn_timer+=1
  if self.step<len(self.patterns[self.wave]) and self.spawn_timer>=51:
   kind='coin' if self.patterns[self.wave][self.step]=='C' else 'fish'
   self.objects.append({'x':256.,'y':94+(-7,5,0,9,-4)[self.step%5],'kind':kind,'speed':3.05+self.wave*.2})
   self.step+=1;self.spawn_timer=0
  if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):self.parry=9
  for obj in list(self.objects):
   obj['x']-=obj['speed']
   if 64<obj['x']<91 and self.parry>0:
    if obj['kind']=='coin':
     self.score+=100+min(500,self.combo*35);self.combo+=1;self.saved+=1;pyxel.play(0,0)
    else:self.hearts-=1;self.combo=0;self.shake=8;pyxel.play(0,1)
    self.objects.remove(obj)
   elif obj['x']<28:
    if obj['kind']=='coin':self.hearts-=1;self.combo=0;self.shake=8;pyxel.play(0,1)
    self.objects.remove(obj)
   if self.hearts<=0:self.state='over';return
  if self.step==len(self.patterns[self.wave]) and not self.objects:
   self.state='won' if self.wave==2 else 'clear'
 def draw(self):
  pyxel.cls(PAPER)
  pyxel.rect(0,0,W,28,INK);pyxel.text(8,7,'LUCKY CAT / PAW PARRY',PAPER)
  pyxel.text(8,18,'FORTUNE %04d'%self.score,GOLD);pyxel.text(117,18,'WAVE %d/3'%(self.wave+1),PAPER);pyxel.text(211,18,'H%d'%self.hearts,RED)
  # Paper-garden framing and a fixed red timing zone. Fish are red X marks: let them pass.
  pyxel.rect(0,29,W,4,(5,13,12)[self.wave]);pyxel.rect(0,166,W,7,(5,13,12)[self.wave])
  for i in range(8):
   x=8+i*34;pyxel.line(x,155,x+16,155,INK);pyxel.line(x+6,157,x+10,160,5)
  pyxel.rect(65,69,25,75,13);pyxel.rectb(65,69,25,75,RED)
  pyxel.text(9,38,'THE PAW',INK);pyxel.text(17,47,'WINDOW',RED)
  cat(46,108,2,self.parry>0)
  pyxel.rect(172,145,55,9,INK);pyxel.rect(175,146,49,6,GOLD);pyxel.text(182,159,'BOWL',INK)
  for obj in self.objects:
   x,y=int(obj['x']),int(obj['y'])
   if obj['kind']=='coin':
    pyxel.circ(x,y,7,INK);pyxel.circ(x,y,5,GOLD);pyxel.line(x-2,y,x+2,y,INK)
   else:
    pyxel.line(x-7,y-4,x+8,y+5,RED);pyxel.line(x+8,y-4,x-7,y+5,RED);pyxel.circ(x,y,3,INK)
  pyxel.rect(0,174,W,18,INK);pyxel.text(8,180,'TAP AT RED BAND / LET RED X PASS',PAPER)
  if self.state!='playing':
   pyxel.rect(13,50,230,95,PAPER);pyxel.rectb(13,50,230,95,INK)
   cat(43,80,1,1)
   pyxel.text(85,66,{'title':'PAW PARRY','clear':'GARDEN CLEAR','won':'THREE GARDENS SAVED','over':'THE FORTUNE SLIPPED'}[self.state],INK)
   pyxel.text(84,86,{'title':'CATCH GOLD / AVOID RED X','clear':'THE NEXT WAVE IS READY','won':'FORTUNE %04d'%self.score,'over':'TRY THE TIMING AGAIN'}[self.state],RED)
   pyxel.text(85,120,'TAP / SPACE TO '+('START' if self.state=='title' else ('NEXT' if self.state=='clear' else 'REPLAY')),INK)
Game()
