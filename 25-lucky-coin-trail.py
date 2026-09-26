# title: Lucky Cat: Coin Trail
# desc: Guide the maneki-neko through a paper maze for koban coins.
import pyxel, math, random
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
random.seed(32)
# Each level is a custom grid. X marks walls; C is the first cat position.
MAPS=[
["XXXXXXXXXXXXXXXX","XC.....X.......X","X.XXX..X.XXX...X","X...X.....X.X..X","X.X.XXXXX.X.X..X","X.X.......X....X","X.XXXX.XXX.XX..X","X......X.....X.X","X.XXX..X.XXX.X.X","X...X......X...X","X.X.XXXXXX.XXX.X","X..............X","XXXXXXXXXXXXXXXX"],
["XXXXXXXXXXXXXXXX","XC...X.........X","XXX..X.XXXXXX..X","X....X...X......X","X.XXXXX.X.XXXX.X","X.......X......X","X.XXXXX.XXXXX..X","X...X.....X....X","X.X.X.XXX.X.XX.X","X.X...X...X....X","X.XXXXX.XXXXXX.X","X..............X","XXXXXXXXXXXXXXXX"],
["XXXXXXXXXXXXXXXX","XC.....X.......X","X.XXXX.X.XXXXX.X","X....X.X.....X.X","XXXX.X.XXXXX.X.X","X....X.....X...X","X.XXXXXXXXX.X.XX","X...X.......X..X","X.X.X.XXXXXXX..X","X.X...X........X","X.XXXXX.XXXXXX.X","X..............X","XXXXXXXXXXXXXXXX"]]
class Game:
 def __init__(self):
  pyxel.init(W,H,title='Lucky Cat Coin Trail',fps=30)
  self.level=0;self.state='title';self.score=0;self.load(0)
  pyxel.sounds[0].mml('T220 O4 C8 E8 G8 >C8');pyxel.sounds[1].mml('T120 O3 G8 E8 C8')
  pyxel.run(self.update,self.draw)
 def load(self,l):
  self.level=l;self.map=MAPS[l];self.x=1;self.y=1;self.step=0
  self.coins=set()
  spots=[(x,y) for y,row in enumerate(self.map) for x,c in enumerate(row) if c=='.' and (x,y)!=(1,1)]
  random.seed(100+l);self.coins=set(random.sample(spots,7+l*2));self.remaining=len(self.coins)
  self.timer=30*(110+l*25);self.bump=0
 def update(self):
  if self.state!='playing':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
    self.score=0;self.load(0);self.state='playing'
   return
  if self.bump:self.bump-=1
  self.timer-=1
  if self.timer<=0:self.state='over';pyxel.play(0,1);return
  dx=int(pyxel.btnp(pyxel.KEY_D,5,4) or pyxel.btnp(pyxel.KEY_RIGHT,5,4) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,5,4))-int(pyxel.btnp(pyxel.KEY_A,5,4) or pyxel.btnp(pyxel.KEY_LEFT,5,4) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,5,4))
  dy=int(pyxel.btnp(pyxel.KEY_S,5,4) or pyxel.btnp(pyxel.KEY_DOWN,5,4) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,5,4))-int(pyxel.btnp(pyxel.KEY_W,5,4) or pyxel.btnp(pyxel.KEY_UP,5,4) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,5,4))
  if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
   mx,my=pyxel.mouse_x,pyxel.mouse_y
   if mx<64:dx=-1
   elif mx>192:dx=1
   elif my<80:dy=-1
   elif my>145:dy=1
  if dx and dy:dy=0
  if dx or dy:
   xx,yy=self.x+dx,self.y+dy
   if 0<=yy<len(self.map) and 0<=xx<len(self.map[yy]) and self.map[yy][xx]!='X':
    self.x,self.y=xx,yy;self.step+=1
    if (xx,yy) in self.coins:
     self.coins.remove((xx,yy));self.score+=100;self.bump=7;pyxel.play(0,0)
     if not self.coins:
      if self.level==2:self.state='won'
      else:self.load(self.level+1)
 def draw(self):
  pyxel.cls(PAPER)
  pyxel.rect(0,0,W,27,INK);pyxel.text(8,7,'LUCKY CAT / COIN TRAIL',PAPER)
  pyxel.text(8,18,'GARDEN %d/3'%(self.level+1),GOLD);pyxel.text(104,18,'%02d COINS'%len(self.coins),PAPER)
  pyxel.text(197,18,'%02ds'%(max(0,self.timer//30)),PAPER)
  for y,row in enumerate(self.map):
   for x,c in enumerate(row):
    px,py=x*14+16,y*11+31
    if c=='X':
     pyxel.rect(px,py,13,10,INK)
     if (x+y)%3==0:pyxel.line(px+2,py+2,px+7,py+2,RED)
    elif (x,y) in self.coins:
     pyxel.circ(px+6,py+5,3,INK);pyxel.circ(px+6,py+5,2,GOLD)
     pyxel.pset(px+6,py+5,INK)
    else:
     pyxel.pset(px+6,py+5,13)
  # The maze player is a one-tile figurine, not the large menu illustration.
  px=self.x*14+16;py=self.y*11+31
  pyxel.rect(px+3,py+4,8,6,INK);pyxel.rect(px+4,py+4,6,5,PAPER)
  pyxel.tri(px+3,py+4,px+4,py+1,px+6,py+4,INK)
  pyxel.tri(px+8,py+4,px+10,py+1,px+11,py+4,INK)
  pyxel.pset(px+5,py+5,INK);pyxel.pset(px+9,py+5,INK)
  pyxel.pset(px+7,py+7,RED);pyxel.pset(px+7,py+9,GOLD)
  pyxel.rect(px+11,py+1-(pyxel.frame_count//12%2),2,5,INK)
  pyxel.rect(0,174,W,18,INK);pyxel.text(8,180,'ARROWS / WASD - COLLECT EVERY KOBAN',PAPER)
  if self.state!='playing':
   pyxel.rect(29,60,198,86,PAPER);pyxel.rectb(29,60,198,86,INK)
   cat(61,82,1,1)
   pyxel.text(97,78,{'title':'COIN TRAIL','won':'THREE GARDENS CLEAR','over':'THE PATH WENT DARK'}[self.state],INK)
   pyxel.text(97,92,'A LITTLE LUCK GOES FAR',RED)
   pyxel.text(97,124,'TAP / SPACE TO PLAY' if self.state=='title' else 'TAP / SPACE TO REPLAY',INK)
Game()
