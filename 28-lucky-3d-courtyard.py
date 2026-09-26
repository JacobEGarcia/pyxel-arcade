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

class Garden(Node):
 def __init__(self,g):
  super().__init__();self.g=g;self.camera=Camera();self.camera.clear_color=7;self.camera.far=900;self.shading=Shading(pyxel.colors)
 def on_draw(self):
  g=self.g;t=pyxel.frame_count
  block(self,0,-4,0,220,8,220,13)
  self.depth_write(False);self.depth_offset(-.4)
  for q in range(-100,101,20):
   self.line(Vec3(q,.3,-100),Vec3(q,.3,100),5)
   self.line(Vec3(-100,.3,q),Vec3(100,.3,q),5)
  for x,z in ((-78,-75),(79,-75),(-78,78),(79,78)):
   block(self,x,2,z,16,4,16,1);block(self,x,13,z,10,20,10,7)
   block(self,x,23,z,24,4,24,8)
  for x,z in ((0,-90),(0,90)):
   block(self,x,24,z,4,48,4,8)
   block(self,x-17,45,z,4,8,4,8);block(self,x+17,45,z,4,8,4,8)
   block(self,x,39,z,40,4,5,8)
  for i,(x,z) in enumerate(g.coins):
   if i in g.taken:continue
   y=10+2*math.sin(t*.11+i)
   self.sphere(Vec3(x,y,z),5,10)
   self.sphere(Vec3(x-1,y+2,z+3),1.5,1)
  cat3(self,g.x,g.z,(t//14)%2 if g.state=='playing' else 0)

class Game:
 def __init__(self):
  pyxel.init(W,H,title='Lucky Cat Courtyard',fps=30)
  self.scene=Garden(self);self.reset()
  pyxel.run(self.update,self.draw)
 def reset(self):
  self.x=0.;self.z=45.;self.taken=set();self.coins=[(-55,-57),(-21,-50),(30,-63),(63,-28),(-62,12),(-20,9),(35,12),(68,67),(-48,68),(8,71)]
  self.time=30*80;self.state='title';self.scene.camera.transform=Mat4.look_at(Vec3(120,135,170),Vec3(0,0,0))
 def update(self):
  if self.state!='playing':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
    self.reset();self.state='playing'
   self.scene.update();return
  dx=int(bool(pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)))-int(bool(pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)))
  dz=int(bool(pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)))-int(bool(pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)))
  m=max(1,math.hypot(dx,dz));self.x=max(-94,min(94,self.x+dx*2.2/m));self.z=max(-94,min(94,self.z+dz*2.2/m))
  for i,(x,z) in enumerate(self.coins):
   if i not in self.taken and (x-self.x)**2+(z-self.z)**2<120:self.taken.add(i)
  self.time-=1
  if len(self.taken)==len(self.coins):self.state='won'
  elif self.time==0:self.state='over'
  eye=Vec3(105+self.x*.48,120,145+self.z*.48)
  self.scene.camera.transform=Mat4.look_at(eye,Vec3(self.x*.55,0,self.z*.55))
  self.scene.update()
 def draw(self):
  pyxel.cls(PAPER);self.scene.draw(0,0,W,H)
  pyxel.rect(0,0,W,31,1);pyxel.line(0,30,W,30,8)
  pyxel.text(9,7,'LUCKY CAT / COURTYARD',7)
  pyxel.text(9,19,'KOBAN %02d/10'%len(self.taken),10)
  pyxel.text(251,19,'TIME %02d'%max(0,self.time//30),7)
  pyxel.rect(0,H-22,W,22,1);pyxel.line(0,H-23,W,H-23,8)
  pyxel.text(8,H-14,'ARROWS / WASD  -  WALK THROUGH THE 3D GARDEN',7)
  if self.state!='playing':
   pyxel.rect(45,76,230,87,1);pyxel.rectb(45,76,230,87,8)
   pyxel.text(96,91,'THE COURTYARD',7)
   line={'title':'FIND ALL TEN KOBAN','won':'ALL TEN FOUND!','over':'THE GARDEN CLOSES'}[self.state]
   pyxel.text(100,111,line,10)
   pyxel.text(91,141,'TAP / SPACE TO '+('START' if self.state=='title' else 'REPLAY'),7)
Game()
