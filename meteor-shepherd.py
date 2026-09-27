# title: Meteor Shepherd
# desc: Orbit a beacon and intercept falling meteors.
import pyxel,math,random
from pyxel.cube import Node,Camera,Mat4,Vec3,Shading
W,H=240,180
random.seed(33)
class Scene(Node):
 def __init__(self,g):
  super().__init__();self.g=g;self.camera=Camera();self.camera.clear_color=1;self.shading=Shading(pyxel.colors)
  self.camera.transform=Mat4.look_at(Vec3(0,150,220),Vec3(0,0,0))
 def on_draw(self):
  g=self.g;t=pyxel.frame_count
  self.box(Mat4.from_translation(Vec3(0,-6,0)),Vec3(180,8,180),1)
  self.depth_write(False);self.depth_offset(-.5)
  for q in range(-80,81,20):
   self.line(Vec3(q,0,-80),Vec3(q,0,80),5)
   self.line(Vec3(-80,0,q),Vec3(80,0,q),5)
  self.box(Mat4.from_translation(Vec3(0,9,0)),Vec3(21,18,21),10)
  self.sphere(Vec3(0,25+math.sin(t*.15)*2,0),8,14)
  self.circb(Vec3(0,3,0),50,10)
  px,pz=45*math.cos(g.angle),45*math.sin(g.angle)
  self.sphere(Vec3(px,8,pz),8,12);self.sphere(Vec3(px,15,pz),3,7)
  for x,y,z,v in g.meteors:
   self.sphere(Vec3(x,y,z),6,8)
   self.sphere(Vec3(x,y+7,z),3,14)
   self.line(Vec3(x,y+9,z),Vec3(x,y+19,z),8)
  for x,z,age in g.sparks:
   self.sphere(Vec3(x,4+age*.5,z),max(1,6-age*.3),10)
class Game:
 def __init__(self):
  pyxel.init(W,H,title='Meteor Shepherd',fps=30);self.reset();self.scene=Scene(self)
  pyxel.sounds[0].set('c4g4','p','6','n',10);pyxel.run(self.update,self.draw)
 def reset(self):
  self.angle=0.;self.hp=5;self.score=0;self.wave=0;self.frame=0;self.state='title';self.meteors=[];self.sparks=[];self.spawn_index=0
 def next_wave(self):
  self.wave+=1;self.frame=0;self.meteors=[];self.sparks=[];self.spawn_index=0;self.angle=0.
 def update(self):
  if self.state!='playing':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
    if self.state=='clear':self.next_wave()
    else:self.reset()
    self.state='playing'
   self.scene.update();return
  self.frame+=1
  left=pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
  right=pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)
  if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):left=pyxel.mouse_x<120;right=not left
  self.angle+=(int(right)-int(left))*.09
  # Twelve fixed telegraphed impacts per wave; gaps give the player time to cross the ring.
  if self.frame%62==1 and self.spawn_index<12:
   theta=(self.spawn_index*(.38,.67,.91)[self.wave]+(.2,.7,1.1)[self.wave])%math.tau
   self.meteors.append((45*math.cos(theta),95.,45*math.sin(theta),1.55+.12*self.wave));self.spawn_index+=1
  px,pz=45*math.cos(self.angle),45*math.sin(self.angle)
  updated=[]
  for x,y,z,v in self.meteors:
   y-=v
   if y<20 and (x-px)**2+(z-pz)**2<280:
    self.score+=1;self.sparks.append((x,z,0));pyxel.play(0,0)
   elif y<4:self.hp-=1
   else:updated.append((x,y,z,v))
  self.meteors=updated;self.sparks=[(x,z,a+1) for x,z,a in self.sparks if a<18]
  if self.hp<=0:self.state='over'
  elif self.spawn_index==12 and not self.meteors:self.state='won' if self.wave==2 else 'clear'
  self.scene.update()
 def draw(self):
  pyxel.cls(1);self.scene.draw(0,0,W,H)
  pyxel.rect(0,0,W,25,1);pyxel.line(0,24,W,24,(10,12,14)[self.wave])
  pyxel.text(7,7,'METEOR SHEPHERD',7);pyxel.text(99,18,'WAVE %d/3'%(self.wave+1),10)
  pyxel.text(132,7,'SAVE %02d'%self.score,10);pyxel.text(186,7,'H%d'%self.hp,8)
  pyxel.rect(0,159,W,21,1);pyxel.line(0,158,W,158,5);pyxel.text(8,166,'LEFT / RIGHT TO ORBIT THE BEACON',7)
  if self.state!='playing':
   pyxel.rect(22,55,196,75,1);pyxel.rectb(22,55,196,75,10)
   pyxel.text(61,67,{'title':'KEEP THE BEACON ALIVE','clear':'THE BEACON HOLDS','won':'THREE WAVES SURVIVED','over':'THE BEACON WENT DARK'}[self.state],7)
   pyxel.text(49,85,{'title':'THREE METEOR WAVES','clear':'THE NEXT STORM IS COMING','won':'METEORS CAUGHT: %02d'%self.score,'over':'METEORS CAUGHT: %02d'%self.score}[self.state],10)
   pyxel.text(69,110,'TAP / SPACE TO '+('START' if self.state=='title' else 'NEXT' if self.state=='clear' else 'REPLAY'),7)
Game()
