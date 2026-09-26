# title: Skyline Stack
# desc: Catch moving cubes above a nighttime city.
import pyxel,math
from pyxel.cube import Node,Camera,Mat4,Vec3,Shading
W,H=240,180
class Scene(Node):
 def __init__(self,g):
  super().__init__();self.g=g;self.camera=Camera();self.camera.clear_color=1;self.shading=Shading(pyxel.colors)
  self.camera.transform=Mat4.look_at(Vec3(155,105,205),Vec3(0,48,0))
 def on_draw(self):
  g=self.g;t=pyxel.frame_count
  self.box(Mat4.from_translation(Vec3(0,-5,0)),Vec3(170,10,120),1)
  self.depth_write(False);self.depth_offset(-.5)
  for x in range(-80,81,20):self.line(Vec3(x,0,-55),Vec3(x,0,55),5)
  for z in range(-40,41,20):self.line(Vec3(-80,0,z),Vec3(80,0,z),5)
  # downtown silhouette around the perimeter
  for i in range(11):
   x=-75+i*15;h=11+(i*i*7)%20
   self.box(Mat4.from_translation(Vec3(x,h/2,-48)),Vec3(10,h,9),5)
  for i,(x,w) in enumerate(g.layers):
   self.box(Mat4.from_translation(Vec3(x,5+i*10,0)),Vec3(w,10,29),[12,11,10,14,9][i%5])
   self.boxb(Mat4.from_translation(Vec3(x,5+i*10,0)),Vec3(w,10,29),7)
  if g.state=='playing':
   h=5+len(g.layers)*10
   self.box(Mat4.from_translation(Vec3(g.x,h,0)),Vec3(g.width,10,29),14)
   self.boxb(Mat4.from_translation(Vec3(g.x,h,0)),Vec3(g.width,10,29),7)
   if t%15<7:self.line(Vec3(g.layers[-1][0],h+9,-17),Vec3(g.layers[-1][0],h+9,17),10)
class Game:
 def __init__(self):
  pyxel.init(W,H,title='Skyline Stack',fps=30);self.reset();self.scene=Scene(self);pyxel.sounds[0].set('g3c4e4','p','6','n',8);pyxel.run(self.update,self.draw)
 def reset(self):
  self.layers=[(0.,55.)];self.x=0.;self.width=55.;self.speed=1.55;self.direction=1;self.misses=0;self.state='title';self.score=0
 def update(self):
  if self.state!='playing':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):self.reset();self.state='playing'
   self.scene.update();return
  self.x+=self.speed*self.direction
  if self.x>69 or self.x< -69:self.direction*=-1
  if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
   prev,pw=self.layers[-1];overlap=max(0,min(self.x+self.width/2,prev+pw/2)-max(self.x-self.width/2,prev-pw/2))
   if overlap<4:self.state='over'
   else:
    left=max(self.x-self.width/2,prev-pw/2);center=left+overlap/2
    self.layers.append((center,overlap));self.score+=1;pyxel.play(0,0)
    self.width=overlap;self.x=-69 if self.score%2==0 else 69;self.direction=1 if self.x<0 else -1
    self.speed=min(3.7,self.speed+.22)
    if self.score>=9:self.state='won'
  self.scene.update()
 def draw(self):
  pyxel.cls(1);self.scene.draw(0,0,W,H)
  pyxel.rect(0,0,W,25,1);pyxel.line(0,24,W,24,5)
  pyxel.text(8,7,'SKYLINE STACK',7);pyxel.text(137,7,'FLOOR %02d/09'%self.score,10)
  pyxel.rect(0,159,W,21,1);pyxel.line(0,158,W,158,5);pyxel.text(8,166,'TAP / SPACE TO DROP THE NEXT FLOOR',7)
  if self.state!='playing':
   pyxel.rect(25,60,190,62,1);pyxel.rectb(25,60,190,62,10)
   pyxel.text(69,70,'BUILD ABOVE THE CITY',7)
   pyxel.text(60,85,{'title':'CATCH EACH MOVING FLOOR','won':'NINE FLOORS / SKYLINE MADE','over':'ONE FLOOR MISSED'}[self.state],10)
   pyxel.text(71,106,'TAP / SPACE TO START' if self.state=='title' else 'TAP / SPACE TO REPLAY',7)
Game()
