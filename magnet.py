# title: Magnet Maze
# desc: Turn polarity to pull your way through three gates.
import pyxel,math
from pyxel.cube import Node, Camera, Mat4, Vec3, Shading
W,H=240,180
class Scene(Node):
 def __init__(self,g):
  super().__init__();self.g=g;self.camera=Camera();self.camera.clear_color=1;self.shading=Shading(pyxel.colors)
  self.camera.transform=Mat4.look_at(Vec3(0,175,130),Vec3(0,0,0))
 def on_draw(self):
  g=self.g;t=pyxel.frame_count
  self.box(Mat4.from_translation(Vec3(0,-6,0)),Vec3(185,8,185),1)
  self.depth_write(False);self.depth_offset(-.5)
  for q in range(-80,81,20):
   self.line(Vec3(q,0,-80),Vec3(q,0,80),5);self.line(Vec3(-80,0,q),Vec3(80,0,q),5)
  # three color-coded magnetic pillars and their fields
  for i,(x,z,p) in enumerate(g.poles):
   col=12 if p>0 else 8
   self.box(Mat4.from_translation(Vec3(x,11,z)),Vec3(15,23,15),col)
   self.sphere(Vec3(x,25+math.sin(t*.09+i)*2,z),5,col)
   if t%6<3:self.circb(Vec3(x,3,z),13,col)
  self.sphere(Vec3(69,11,67),9,10);self.sphere(Vec3(69,11,67),3,7)
  x,z=g.x,g.z
  self.sphere(Vec3(x,8,z),7,12 if g.charge>0 else 8)
  self.sphere(Vec3(x,14,z),2,7)
  self.boxb(Mat4.from_translation(Vec3(x,8,z)),Vec3(17,17,17),7)
class Game:
 def __init__(self):
  pyxel.init(W,H,title='Magnet Maze',fps=30);self.reset();self.scene=Scene(self);pyxel.run(self.update,self.draw)
 def reset(self):
  self.x,self.z=-68.,-66.;self.vx,self.vz=0.,0.;self.charge=1;self.frame=0;self.state='title'
  self.poles=[(-35,-35,1),(28,-27,-1),(24,42,1)]
 def update(self):
  if self.state!='playing':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):self.reset();self.state='playing'
   self.scene.update();return
  self.frame+=1
  if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):self.charge*=-1
  dx=int(pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT))-int(pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT))
  dz=int(pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN))-int(pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP))
  ax,az=dx*.22,dz*.22
  for x,z,p in self.poles:
   vx,vz=x-self.x,z-self.z;d=max(12,math.hypot(vx,vz));a=-self.charge*p*min(.4,210/(d*d))
   ax+=vx/d*a;az+=vz/d*a
  self.vx=max(-2.5,min(2.5,(self.vx+ax)*.94));self.vz=max(-2.5,min(2.5,(self.vz+az)*.94))
  self.x=max(-78,min(78,self.x+self.vx));self.z=max(-78,min(78,self.z+self.vz))
  if (self.x-69)**2+(self.z-67)**2<180:self.state='won'
  if self.frame>30*70:self.state='over'
  self.scene.update()
 def draw(self):
  pyxel.cls(1);self.scene.draw(0,0,W,H)
  pyxel.rect(0,0,W,25,1);pyxel.line(0,24,W,24,5)
  pyxel.text(8,7,'MAGNET MAZE',7);pyxel.text(113,7,'POLARITY %s'%('+' if self.charge>0 else '-'),12 if self.charge>0 else 8)
  pyxel.text(204,7,'%02d'%max(0,70-self.frame//30),14)
  pyxel.rect(0,159,W,21,1);pyxel.line(0,158,W,158,5)
  pyxel.text(8,166,'ARROWS MOVE  /  SPACE OR TAP FLIPS',7)
  if self.state!='playing':
   pyxel.rect(21,59,198,63,1);pyxel.rectb(21,59,198,63,10)
   pyxel.text(70,69,'A FIELD OF FORCES',7)
   pyxel.text(60,84,{'title':'REACH THE GOLDEN GATE','won':'YOU FOUND THE WAY OUT','over':'THE FIELD RESET'}[self.state],10)
   pyxel.text(72,105,'TAP / SPACE TO START' if self.state=='title' else 'TAP / SPACE TO REPLAY',7)
Game()
