# title: Lucky Cat: Bell Garden
# desc: A rhythm garden: follow the falling bells and collect a melody.
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
random.seed(12)
NOTES=[(48,0),(112,1),(176,2),(112,1),(48,0),(176,2),(48,0),(112,1),(176,2),(48,0),(112,1),(176,2)]
class Game:
 def __init__(self):
  pyxel.init(W,H,title='Lucky Cat Bell Garden',fps=30)
  self.state='title';self.reset()
  for i,m in enumerate(['T160 O4 C8','T160 O4 E8','T160 O4 G8']):pyxel.sounds[i].mml(m)
  pyxel.sounds[3].mml('T80 O3 C8 R8 C8');pyxel.run(self.update,self.draw)
 def reset(self):
  self.state='title';self.frame=0;self.score=0;self.streak=0;self.hearts=5;self.next=0;self.notes=[];self.flash=0
 def play(self):
  self.reset();self.state='playing'
 def update(self):
  if self.state!='playing':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):self.play()
   return
  self.frame+=1
  if self.flash:self.flash-=1
  if self.next<len(NOTES) and self.frame>=45+self.next*39:
   lane=NOTES[self.next][1];self.notes.append([lane,-10,self.next]);self.next+=1
  hit=-1
  for i,k in enumerate([pyxel.KEY_A,pyxel.KEY_S,pyxel.KEY_D]):
   if pyxel.btnp(k) or pyxel.btnp([pyxel.KEY_LEFT,pyxel.KEY_DOWN,pyxel.KEY_RIGHT][i]) or pyxel.btnp([pyxel.GAMEPAD1_BUTTON_X,pyxel.GAMEPAD1_BUTTON_A,pyxel.GAMEPAD1_BUTTON_B][i]):hit=i
  if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_y<155:hit=max(0,min(2,pyxel.mouse_x//(W//3)))
  if hit>=0:
   candidates=[n for n in self.notes if n[0]==hit and abs(n[1]-119)<21]
   if candidates:
    n=min(candidates,key=lambda v:abs(v[1]-119));self.notes.remove(n)
    self.streak+=1;self.score+=100+min(500,self.streak*25);self.flash=10;pyxel.play(0,hit)
   else:self.streak=0
  for n in list(self.notes):
   n[1]+=2.5
   if n[1]>141:
    self.notes.remove(n);self.hearts-=1;self.streak=0;pyxel.play(0,3)
    if self.hearts<=0:self.state='over'
  if self.next==len(NOTES) and not self.notes and self.state=='playing':self.state='won'
 def draw(self):
  pyxel.cls(PAPER);pyxel.rect(0,0,W,25,INK)
  pyxel.text(8,7,'LUCKY CAT / BELL GARDEN',PAPER)
  pyxel.text(8,17,'SCORE %05d'%self.score,GOLD);pyxel.text(112,17,'CHAIN %02d'%self.streak,PAPER)
  pyxel.text(216,17,'H%d'%self.hearts,RED)
  for lane in range(3):
   x=29+lane*76
   pyxel.rect(x,34,62,109,13 if lane%2 else PAPER)
   pyxel.rectb(x,34,62,109,INK)
   pyxel.text(x+28,146,'ASD'[lane],INK)
   pyxel.circ(x+31,120,13,INK);pyxel.circ(x+31,120,11,PAPER)
   pyxel.circ(x+31,120,3,RED)
  for lane,y,index in self.notes:
   x=60+lane*76
   pyxel.tri(x-10,y-4,x+10,y-4,x,y+8,INK)
   pyxel.tri(x-7,y-3,x+7,y-3,x,y+5,GOLD)
   pyxel.circ(x,y+9,2,RED)
  if self.flash:pyxel.line(17,158,239,158,GOLD)
  cat(45,168,1,self.streak and self.frame//7%2)
  pyxel.text(80,164,'A / S / D TO RING',INK)
  pyxel.text(80,177,'TAP A LANE AT THE RED DOT',RED)
  if self.state!='playing':
   pyxel.rect(19,49,218,80,PAPER);pyxel.rectb(19,49,218,80,INK)
   cat(56,69,1,1)
   pyxel.text(95,65,{'title':'BELL GARDEN','won':'THE GARDEN SINGS','over':'THE BELLS FELL SILENT'}[self.state],INK)
   pyxel.text(95,82,'12 NOTES. 3 BELLS.',RED)
   pyxel.text(95,108,'TAP / SPACE TO PLAY' if self.state=='title' else 'TAP / SPACE TO REPLAY',INK)
Game()
