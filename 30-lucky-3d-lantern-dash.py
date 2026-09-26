# title: Lucky Cat Courtyard
# desc: A three-dimensional koban hunt through a small shrine garden.
import pyxel,math
from pyxel.cube import Camera,Mat4,Node,Shading,Vec3
W,H=320,240
PAPER=7;INK=1;RED=8;GOLD=10

def block(node,x,y,z,w,h,d,c):node.box(Mat4.from_translation(Vec3(x,y,z)),Vec3(w,h,d),c)
def cat3(node,x,z,turn=0,lift=0):
 # Traditional porcelain figurine: ears, raised right paw, red collar, central koban.
 block(node,x,10+lift,z,15,19,12,PAPER)
 block(node,x,22+lift,z,16,13,13,PAPER)
 block(node,x-6,30+lift,z,4,8,5,PAPER);block(node,x+6,30+lift,z,4,8,5,PAPER)
 block(node,x-6,31+lift,z+3,2,3,1,RED);block(node,x+6,31+lift,z+3,2,3,1,RED)
 block(node,x-4,23+lift,z+7,2,2,1,INK);block(node,x+4,23+lift,z+7,2,2,1,INK)
 block(node,x,20+lift,z+7,2,2,1,RED)
 block(node,x,15+lift,z+7,14,3,1,RED)
 # paw above shoulder, beside face
 block(node,x+10,23+turn+lift,z+2,5,17,5,PAPER)
 block(node,x+10,33+turn+lift,z+2,7,6,5,PAPER)
 block(node,x,9+lift,z+7,10,10,2,INK)
 block(node,x,9+lift,z+8,8,8,1,GOLD)
 block(node,x,8+lift,z+9,4,1,1,INK)

class Runway(Node):
 def __init__(self,g):
  super().__init__();self.g=g;self.camera=Camera();self.camera.clear_color=PAPER;self.camera.far=700;self.shading=Shading(pyxel.colors)
  self.camera.transform=Mat4.look_at(Vec3(45,68,170),Vec3(0,10,-40))
 def on_draw(self):
  g=self.g;t=pyxel.frame_count
  block(self,0,-4,-22,115,8,260,13)
  self.depth_write(False);self.depth_offset(-.4)
  for x in (-50,-17,17,50):self.line(Vec3(x,.3,100),Vec3(x,.3,-145),5)
  for q in range(-140,110,20):
   z=q+g.progress%20
   self.line(Vec3(-50,.3,z),Vec3(50,.3,z),5)
  for lane in (-1,0,1):
   x=lane*32
   block(self,x,3,-125,23,6,8,8)
   block(self,x,13,-125,4,16,4,8)
  for i,(lane,z,kind) in enumerate(g.objects):
   if z>110 or z< -145:continue
   x=lane*32
   if kind=='coin':
    self.sphere(Vec3(x,9+2*math.sin(t*.13+i),z),5,10)
    self.sphere(Vec3(x-1,11,z+3),1,1)
   else:
    block(self,x,8,z,25,16,13,1)
    block(self,x,17,z,26,4,14,8)
    block(self,x,4,z+8,8,7,1,8)
  cat3(self,g.lane*32,65,3 if g.jump else (t//12)%2,int(13*math.sin(math.pi*g.jump/24)) if g.jump else 0)

class Game:
 def __init__(self):
  pyxel.init(W,H,title='Lucky Cat Lantern Dash',fps=30)
  self.scene=Runway(self);self.reset()
  pyxel.run(self.update,self.draw)
 def reset(self):
  self.lane=0;self.progress=0;self.objects=[];self.score=0;self.hearts=3;self.jump=0;self.cool=0
  self.time=30*60;self.state='title';self.spawn=0
 def update(self):
  if self.state!='playing':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
    self.reset();self.state='playing'
   self.scene.update();return
  if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):self.lane=max(-1,self.lane-1)
  if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):self.lane=min(1,self.lane+1)
  if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)) and not self.jump:self.jump=24
  if self.jump:self.jump-=1
  self.progress+=2.3
  self.spawn+=1
  if self.spawn>=32:
   self.spawn=0
   lane=(-1,0,1)[(pyxel.frame_count//32*7)%3]
   kind='coin' if (pyxel.frame_count//32)%4!=2 else 'gate'
   self.objects.append((lane,-138,kind))
  later=[]
  for lane,z,kind in self.objects:
   z+=2.3
   if z>=57 and z<61 and lane==self.lane:
    if kind=='coin':self.score+=1
    elif not self.jump and not self.cool:self.hearts-=1;self.cool=20
   elif z<100:later.append((lane,z,kind))
  self.objects=later
  if self.cool:self.cool-=1
  self.time-=1
  if self.score>=15:self.state='won'
  elif self.hearts<=0 or self.time<=0:self.state='over'
  self.scene.update()
 def draw(self):
  pyxel.cls(PAPER);self.scene.draw(0,0,W,H)
  pyxel.rect(0,0,W,31,1);pyxel.line(0,30,W,30,8)
  pyxel.text(8,7,'LUCKY CAT / LANTERN DASH',7)
  pyxel.text(8,19,'KOBAN %02d/15'%self.score,10)
  pyxel.text(135,19,'HEARTS %d'%self.hearts,8)
  pyxel.text(251,19,'TIME %02d'%max(0,self.time//30),7)
  pyxel.rect(0,H-23,W,23,1);pyxel.line(0,H-24,W,H-24,8)
  pyxel.text(8,H-15,'LEFT / RIGHT: LANE   -   TAP / SPACE: JUMP',7)
  if self.state!='playing':
   pyxel.rect(38,82,244,77,1);pyxel.rectb(38,82,244,77,8)
   pyxel.text(102,94,'LANTERN DASH',7)
   pyxel.text(62,115,{'title':'COLLECT 15. DODGE THE GATES.','won':'FIFTEEN KOBAN COLLECTED!','over':'THE RUN IS OVER.'}[self.state],10)
   pyxel.text(83,142,'TAP / SPACE TO '+('START' if self.state=='title' else 'REPLAY'),7)
Game()
