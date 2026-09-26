# title: Lucky Cat Courtyard
# desc: A three-dimensional koban hunt through a small shrine garden.
import pyxel,math
from pyxel.cube import Camera,Mat4,Node,Shading,Vec3
W,H=320,240
PAPER=7;INK=1;RED=8;GOLD=10

def block(node,x,y,z,w,h,d,c):node.box(Mat4.from_translation(Vec3(x,y,z)),Vec3(w,h,d),c)
def cat3(node,x,z,turn=0):
 # Traditional porcelain figurine: ears, raised right paw, red collar, central koban.
 block(node,x,10,z,15,19,12,PAPER)
 block(node,x,22,z,16,13,13,PAPER)
 block(node,x-6,30,z,4,8,5,PAPER);block(node,x+6,30,z,4,8,5,PAPER)
 block(node,x-6,31,z+3,2,3,1,RED);block(node,x+6,31,z+3,2,3,1,RED)
 block(node,x-4,23,z+7,2,2,1,INK);block(node,x+4,23,z+7,2,2,1,INK)
 block(node,x,20,z+7,2,2,1,RED)
 block(node,x,15,z+7,14,3,1,RED)
 # paw above shoulder, beside face
 block(node,x+10,23+turn,z+2,5,17,5,PAPER)
 block(node,x+10,33+turn,z+2,7,6,5,PAPER)
 block(node,x,9,z+7,10,10,2,INK)
 block(node,x,9,z+8,8,8,1,GOLD)
 block(node,x,8,z+9,4,1,1,INK)

class Range(Node):
 def __init__(self,g):
  super().__init__();self.g=g;self.camera=Camera();self.camera.clear_color=PAPER;self.camera.far=900;self.shading=Shading(pyxel.colors)
  self.camera.transform=Mat4.look_at(Vec3(120,135,175),Vec3(0,10,-25))
 def on_draw(self):
  g=self.g; t=pyxel.frame_count
  block(self,0,-5,0,230,10,210,13)
  self.depth_write(False);self.depth_offset(-.4)
  for q in range(-100,101,20):
   self.line(Vec3(q,.3,-96),Vec3(q,.3,96),5)
   self.line(Vec3(-105,.3,q),Vec3(105,.3,q),5)
  cat3(self,0,72,2 if g.throw>0 else (t//15)%2)
  # Three red lacquer bowls on porcelain plinths, with moving red targets.
  for i,(x,z) in enumerate(g.targets):
   hit=i in g.hit
   block(self,x,5,z,26,10,26,7)
   block(self,x,11,z,21,3,21,1)
   block(self,x,15,z,19,4,19,8 if not hit else 5)
   block(self,x,19,z,14,3,14,1)
   if not hit:
    self.sphere(Vec3(x,25+2*math.sin(t*.07+i),z),3,8)
  # The coin in flight is a solid gold disc, animated in real 3D.
  if g.throw:
   u=1-g.throw/26
   tx,tz=g.throw_target
   x=tx*u;z=72+(tz-72)*u;y=34+35*math.sin(math.pi*u)
   block(self,x,y,z,9,9,2,10)
   block(self,x,y,z+2,3,1,1,1)
  # Aim line is a shallow charcoal guide; the actual target flashes when aligned.
  theta=math.radians(g.aim)
  endpoint=Vec3(math.sin(theta)*125,1,72-math.cos(theta)*125)
  self.line(Vec3(0,1,65),endpoint,1)
  self.sphere(endpoint,3,8)

class Game:
 def __init__(self):
  pyxel.init(W,H,title='Lucky Cat Koban Toss',fps=30)
  self.scene=Range(self);self.reset()
  pyxel.run(self.update,self.draw)
 def reset(self):
  self.targets=[(-56,-44),(0,-70),(57,-38)]
  self.hit=set();self.aim=0.;self.throw=0;self.throw_target=(0.,0.);self.throw_hit=-1
  self.shots=9;self.time=30*65;self.state='title';self.score=0
 def update(self):
  if self.state!='playing':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
    self.reset();self.state='playing'
   self.scene.update();return
  direction=int(bool(pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)))-int(bool(pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)))
  self.aim=max(-45,min(45,self.aim+direction*1.35))
  if self.throw:
   self.throw-=1
   if not self.throw and self.throw_hit>=0:
    self.hit.add(self.throw_hit);self.score+=100;self.throw_hit=-1
  elif self.shots and (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)):
   self.shots-=1;self.throw=26
   best=100;idx=-1
   for i,(x,z) in enumerate(self.targets):
    if i in self.hit:continue
    angle=math.degrees(math.atan2(x,72-z))
    miss=abs(angle-self.aim)
    if miss<best:best=miss;idx=i
   self.throw_hit=idx if best<6.5 else -1
   self.throw_target=self.targets[idx] if self.throw_hit>=0 else (math.sin(math.radians(self.aim))*145,72-math.cos(math.radians(self.aim))*145)
  self.time-=1
  if len(self.hit)==3:self.state='won'
  elif self.time<=0 or (self.shots==0 and not self.throw):self.state='over'
  self.scene.update()
 def draw(self):
  pyxel.cls(PAPER);self.scene.draw(0,0,W,H)
  pyxel.rect(0,0,W,31,1);pyxel.line(0,30,W,30,8)
  pyxel.text(8,7,'LUCKY CAT / KOBAN TOSS',7)
  pyxel.text(8,19,'BOWLS %d/3'%len(self.hit),10)
  pyxel.text(124,19,'COINS %d'%self.shots,7)
  pyxel.text(252,19,'TIME %02d'%max(0,self.time//30),7)
  pyxel.rect(0,H-23,W,23,1);pyxel.line(0,H-24,W,H-24,8)
  pyxel.text(8,H-15,'LEFT / RIGHT: AIM  -  TAP / SPACE: TOSS',7)
  if self.state!='playing':
   pyxel.rect(34,81,252,77,1);pyxel.rectb(34,81,252,77,8)
   pyxel.text(101,93,'KOBAN TOSS',7)
   pyxel.text(65,115,{'title':'THREE BOWLS. NINE COINS.','won':'THREE PERFECT LANDINGS!','over':'TRY ANOTHER ROUND.'}[self.state],10)
   pyxel.text(84,142,'TAP / SPACE TO '+('START' if self.state=='title' else 'REPLAY'),7)
Game()
