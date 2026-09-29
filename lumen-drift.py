"""Lumen Drift: an original Pyxel arcade delivery game. MIT licensed."""
import math
import random
import pyxel

W,H=256,192
random.seed(39)
class Game:
 def __init__(self):
  pyxel.init(W,H,title='LUMEN DRIFT',fps=30,display_scale=3)
  self.best=0; self.mode='title'; self.t=0; self.clouds=[(random.randrange(W),random.randrange(16,100),random.randrange(5,25)) for _ in range(13)]
  self.stars=[(random.randrange(W),random.randrange(8,90),random.randrange(10,31)) for _ in range(35)]
  self.islands=[]
  for i in range(22):
   x=i*48+random.randrange(-12,13); y=132+random.randrange(-12,11)
   self.islands.append((x,y,random.randrange(17,32)))
  self.reset(); pyxel.run(self.update,self.draw)
 def reset(self):
  self.x=45.; self.y=108.; self.vx=0.;self.vy=0.;self.cam=0.;self.life=3;self.fuel=100.;self.score=0;self.cargo=0;self.combo=0;self.distance=0.;self.inv=0;self.motes=[];self.beacons=[(180,95),(380,73),(580,110),(790,84),(990,67)];self.shards=[(x,70+random.randrange(-28,35)) for x in range(110,1040,32)];self.hazards=[(x,98+random.randrange(-28,28)) for x in range(240,1020,90)];self.particles=[];self.delivered=0;self.time=0
 def update(self):
  self.t+=1
  if self.mode in ('title','win','lose'):
   if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A): self.reset();self.mode='play'
   return
  self.time+=1
  thrust=pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)
  left=pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A)
  right=pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D)
  self.vx+=(0.38 if right else -0.32 if left else 0);self.vx*=.97;self.vx=max(-2.8,min(3.4,self.vx));self.x=max(8,min(1040,self.x+self.vx));self.vy+=.17
  if thrust and self.fuel>0:
   self.vy-=.42;self.fuel-=.24
   if self.t%2==0:self.spark(self.x-3,self.y+6,10,2)
  self.vy=max(-3.8,min(3.8,self.vy));self.y+=self.vy;self.cam+=(max(0,self.x-68)-self.cam)*.10;self.inv=max(0,self.inv-1)
  if self.y<21:self.y=21;self.vy=.5
  if self.y>141:
   self.y=141;self.vy=-1.2
  for x,y in self.shards[:]:
   if abs(x-self.x)<9 and abs(y-self.y)<9:self.shards.remove((x,y));self.score+=10+self.combo*2;self.combo=min(9,self.combo+1);self.fuel=min(100,self.fuel+7);self.spark(x,y,10,8)
  for x,y in self.hazards:
   yy=y+math.sin(self.t*.07+x)*7
   if abs(x-self.x)<11 and abs(yy-self.y)<9:self.hit()
  for bx,by in self.beacons:
   if abs(bx-self.x)<13 and abs(by-self.y)<16 and bx>self.distance:
    self.delivered+=1;self.distance=bx;self.score+=100+self.combo*10;self.fuel=min(100,self.fuel+35);self.spark(bx,by,11,24)
    if self.delivered==5:self.mode='win';self.best=max(self.best,self.score)
  self.particles=[(x+vx,y+vy,vx*.97,vy+.04,col,life-1) for x,y,vx,vy,col,life in self.particles if life>0]
 def hit(self):
  if self.inv:return
  self.life-=1;self.combo=0;self.inv=50;self.spark(self.x,self.y,8,14)
  if self.life==0:self.mode='lose';self.best=max(self.best,self.score)
 def spark(self,x,y,col,n):
  for _ in range(n):self.particles.append((x,y,random.uniform(-2,2),random.uniform(-2,1),col,random.randrange(9,19)))
 def draw(self):
  pyxel.cls(1);c=self.cam
  for x,y,r in self.stars:
   sx=(x-c*.12)%W
   pyxel.pset(sx,y,7 if (self.t+x)%37<30 else 10)
  pyxel.circ(207-c*.04%260,34,19,5);pyxel.circ(203-c*.04%260,30,16,13)
  for x,y,r in self.clouds:
   sx=(x-c*.22)%290-15
   pyxel.elli(sx,y,r*2,8,2);pyxel.line(sx+6,y+3,sx+r*2-4,y+3,5)
  for i in range(22):
   sx=i*35-c*.36%35
   pyxel.tri(sx,128,sx+40,59+(i%4)*9,sx+79,128,2)
  pyxel.rect(0,146,W,46,0)
  for x,y,r in self.islands:
   sx=int(x-c)
   if -60<sx<300:
    pyxel.elli(sx-r,y+8,r*2,12,0);pyxel.elli(sx-r,y,r*2,13,4);pyxel.line(sx-r+4,y+3,sx+r-4,y+3,9)
    pyxel.tri(sx-r+4,y+11,sx,y+25,sx+r-4,y+11,2)
    for j in range(3):pyxel.pset(sx-r+7+j*8,y+2,11)
  for x,y in self.shards:
   sx=x-c
   if -10<sx<266:
    yy=y+math.sin(self.t*.12+x)*2
    pyxel.tri(sx,yy-5,sx+4,yy,sx,yy+5,10);pyxel.tri(sx,yy-5,sx-4,yy,sx,yy+5,7)
  for x,y in self.hazards:
   sx=x-c;yy=y+math.sin(self.t*.07+x)*7
   if -16<sx<272:
    pyxel.circ(sx,yy,7,8);pyxel.circb(sx,yy,8,7);pyxel.line(sx-4,yy-4,sx+4,yy+4,0);pyxel.line(sx+4,yy-4,sx-4,yy+4,0)
  for i,(x,y) in enumerate(self.beacons):
   sx=x-c
   if -30<sx<280:
    active=i>=self.delivered
    pyxel.rect(sx-2,y-25,4,35,5 if active else 2);pyxel.circ(sx,y-26,12,10 if active else 13);pyxel.circb(sx,y-26,13,7)
    pyxel.text(sx-4,y-28,str(i+1),0 if active else 7)
    pyxel.line(sx-12,y+9,sx+12,y+9,7)
  for x,y,vx,vy,col,life in self.particles:pyxel.pset(x-c,y,col)
  if self.inv%6<3:
   sx=self.x-c
   pyxel.tri(sx-8,self.y+5,sx+7,self.y+5,sx+3,self.y-5,7)
   pyxel.tri(sx-3,self.y+3,sx+5,self.y+2,sx+2,self.y-3,10)
   pyxel.rect(sx-3,self.y-1,4,3,0)
   pyxel.line(sx-6,self.y+7,sx+5,self.y+7,8)
  # Fixed-size HUD, deliberate 16-color palette.
  pyxel.rect(0,0,W,16,0);pyxel.line(0,16,W,16,9)
  pyxel.text(7,5,'LUMEN DRIFT',10);pyxel.text(96,5,'SCORE '+str(self.score).zfill(5),7);pyxel.text(185,5,'HULL '+str(self.life),8)
  pyxel.rect(7,181,76,5,5);pyxel.rect(7,181,self.fuel*.76,5,10 if self.fuel>20 else 8)
  pyxel.text(89,180,'FUEL',7);pyxel.text(154,180,'BEACONS '+str(self.delivered)+'/5',7)
  if self.mode!='play':
   pyxel.rect(23,45,210,100,0);pyxel.rectb(23,45,210,100,10)
   pyxel.text(76,59,'LUMEN DRIFT',10)
   if self.mode=='title':
    pyxel.text(44,76,'DELIVER LIGHT TO 5 BEACONS',7);pyxel.text(45,88,'DODGE MINES, GATHER FUEL',7)
   else:
    pyxel.text(91,78,'ROUTE COMPLETE' if self.mode=='win' else 'SHIP LOST',11 if self.mode=='win' else 8)
    pyxel.text(77,91,'FINAL SCORE '+str(self.score),7)
   pyxel.text(56,113,'ARROWS MOVE  SPACE THRUST',6)
   pyxel.text(69,129,'ENTER / SPACE START',10)
Game()
