# title: Lantern Run
# desc: Skim a ring of lanterns; dodge the red sentries.
import pyxel,math,random
from pyxel.cube import Node, Camera, Mat4, Vec3, Shading
W,H=240,180
random.seed(15)
class Scene(Node):
 def __init__(self,g):
  super().__init__();self.g=g;self.camera=Camera();self.camera.clear_color=1;self.shading=Shading(pyxel.colors)
  self.camera.transform=Mat4.look_at(Vec3(0,170,160),Vec3(0,0,0))
 def on_draw(self):
  g=self.g;t=pyxel.frame_count
  self.box(Mat4.from_translation(Vec3(0,-6,0)),Vec3(180,9,180),1)
  self.depth_write(False);self.depth_offset(-.5)
  for q in range(-80,81,20):
   self.line(Vec3(q,0,-80),Vec3(q,0,80),5)
   self.line(Vec3(-80,0,q),Vec3(80,0,q),5)
  for i in range(9):
   a=i*math.tau/9; x,z=67*math.cos(a),67*math.sin(a)
   self.box(Mat4.from_translation(Vec3(x,5,z)),Vec3(4,11,4),5)
   self.box(Mat4.from_translation(Vec3(x,13+math.sin(t*.09+i)*2,z)),Vec3(9,10,9),14)
  for i,(x,z) in enumerate(g.pickups):
   self.sphere(Vec3(x,8+math.sin(t*.13+i)*2,z),5,10)
   self.boxb(Mat4.from_translation(Vec3(x,8,z)),Vec3(13,13,13),7)
  for i,(x,z) in enumerate(g.enemies):
   self.box(Mat4.from_translation(Vec3(x,8,z)) * Mat4.from_euler(Vec3(0,t*2+i*70,0)),Vec3(12,14,12),8)
   self.sphere(Vec3(x,13,z+7),2,7)
  x,z=g.x,g.z
  self.box(Mat4.from_translation(Vec3(x,7,z)),Vec3(11,14,10),12)
  self.box(Mat4.from_translation(Vec3(x-4,15,z)),Vec3(3,7,3),12)
  self.box(Mat4.from_translation(Vec3(x+4,15,z)),Vec3(3,7,3),12)
  self.sphere(Vec3(x,12,z+5),2,7)
class Game:
 def __init__(self):
  pyxel.init(W,H,title='Lantern Run',fps=30);self.reset();self.scene=Scene(self);pyxel.run(self.update,self.draw)
 def reset(self):
  self.x,self.z=0.,0.;self.score=0;self.hp=3;self.frame=0;self.state='title';self.invuln=0
  self.pickups=[(-38,-38),(40,-42),(-60,15),(55,41),(0,60)]
  self.enemies=[(-50,40),(52,-18),(0,-65)]
 def update(self):
  if self.state!='playing':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):self.reset();self.state='playing'
   self.scene.update();return
  self.frame+=1
  dx=int(pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT))-int(pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT))
  dz=int(pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN))-int(pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP))
  if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_y<155:
   dx+= 1 if pyxel.mouse_x>135 else -1 if pyxel.mouse_x<105 else 0
   dz+= 1 if pyxel.mouse_y>100 else -1 if pyxel.mouse_y<70 else 0
  norm=max(1,math.hypot(dx,dz));self.x=max(-77,min(77,self.x+dx*2.8/norm));self.z=max(-77,min(77,self.z+dz*2.8/norm))
  for i,(x,z) in enumerate(self.enemies):
   ax,az=self.x-x,self.z-z;dist=max(1,math.hypot(ax,az));speed=.63+self.score*.07
   self.enemies[i]=(x+ax/dist*speed,z+az/dist*speed)
   if dist<11 and self.invuln==0:
    self.hp-=1;self.invuln=40
    if self.hp==0:self.state='over'
  if self.invuln:self.invuln-=1
  for x,z in list(self.pickups):
   if (self.x-x)**2+(self.z-z)**2<130:
    self.pickups.remove((x,z));self.score+=1;self.invuln=15
    # shift pursuers back to give the player breathing room
    self.enemies=[(ex*1.15,ez*1.15) for ex,ez in self.enemies]
  if not self.pickups:self.state='won'
  self.scene.update()
 def draw(self):
  pyxel.cls(1);self.scene.draw(0,0,W,H)
  pyxel.rect(0,0,W,25,1);pyxel.line(0,24,W,24,5)
  pyxel.text(8,7,'LANTERN RUN',7);pyxel.text(113,7,'LIGHT %d/5'%self.score,10);pyxel.text(194,7,'HP %d'%self.hp,8)
  pyxel.rect(0,159,W,21,1);pyxel.line(0,158,W,158,5);pyxel.text(8,166,'GET THE LIGHTS  /  AVOID THE RED',7)
  if self.state!='playing':
   pyxel.rect(23,60,194,61,1);pyxel.rectb(23,60,194,61,10)
   pyxel.text(64,71,'THE LIGHTS ARE LOST',7)
   pyxel.text(62,85,{'title':'FIND FIVE / KEEP THREE HEARTS','won':'YOU BROUGHT BACK THE LIGHT','over':'THE SENTRIES CAUGHT YOU'}[self.state],10)
   pyxel.text(68,106,'TAP / SPACE TO PLAY' if self.state=='title' else 'TAP / SPACE TO REPLAY',7)
Game()
