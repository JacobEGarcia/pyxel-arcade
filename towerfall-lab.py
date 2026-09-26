# title: Towerfall Lab
# desc: Three-stage 3D physics demolition with combo scoring.
import pyxel, math
from pyxel.cube import Camera, Collider, Mat4, Node, Shading, Vec3
W,H=320,240
COLORS=(8,14,11,9,10,12)

class Body(Node):
 def __init__(self,parent,pos,size,color,mass=0,radius=0,target=False):
  super().__init__();self.transform=Mat4.from_translation(pos)
  self.size=size;self.color=color;self.target=target;self.cleared=False
  self.collider=Collider(size=size,radius=radius,mass=mass,rolls=False,
                         restitution=.05 if mass else .0,friction=.75)
  parent.add_child(self)
 def on_collide(self,other,contact):
  if self.collider.mass:
   self.transform=Mat4.from_translation(contact.normal*contact.depth)*self.transform
   self.collider.velocity+=contact.delta_velocity
   self.collider.angular_velocity+=contact.delta_angular_velocity
 def on_draw(self):
  if self.collider.radius and self.size==Vec3.ZERO:
   self.sphere(Vec3.ZERO,self.collider.radius,self.color)
   self.sphere(Vec3(-3,4,5),2,7)
  else:
   self.box(Mat4.IDENTITY,self.size,self.color)
   self.boxb(Mat4.IDENTITY,self.size,7 if self.target else 5)

class Stage(Node):
 def __init__(self,app):
  super().__init__();self.app=app
  self.camera=Camera();self.camera.clear_color=1;self.camera.far=1800
  self.shading=Shading(pyxel.colors)
  self.boxes=[];self.shots=[];self.level=0;self.camera_angle=30;self.camera_pitch=19
  self.load(0)
 def look(self):
  rad=math.radians(self.camera_angle)
  eye=Vec3(math.sin(rad)*285,135+self.camera_pitch*1.8,math.cos(rad)*285)
  self.camera.transform=Mat4.look_at(eye,Vec3(0,35,0))
 def load(self,level):
  for node in list(self.children):node.destroy()
  self.boxes=[];self.shots=[];self.level=level;self.fired=False;self.origin={};self.look()
  Body(self,Vec3(0,-9,0),Vec3(280,18,240),1)
  # Three different physics structures: two staggered towers, a bridge,
  # and a stepped core whose capstones anchor the final target.
  if level==0:
   for x in (-45,45):
    for row in range(4):
     for z in (-14,14):
      self.boxes.append(Body(self,Vec3(x+(row%2)*5,10+row*19,z),Vec3(19,18,19),COLORS[(row+(1 if x>0 else 0))%6],2,target=True))
   for x in (-45,45):
    self.boxes.append(Body(self,Vec3(x,87,0),Vec3(38,9,40),10,4,target=True))
  elif level==1:
   for i,x in enumerate((-64,-33,33,64)):
    for r in range(3):
     self.boxes.append(Body(self,Vec3(x,9+r*18,0),Vec3(17,17,23),COLORS[(r+i)%6],2,target=True))
   for r in range(3):
    self.boxes.append(Body(self,Vec3(0,60+r*12,0),Vec3(153-20*r,11,36),COLORS[(r+3)%6],5,target=True))
   for x in (-40,0,40):self.boxes.append(Body(self,Vec3(x,106,0),Vec3.ZERO,14,4,radius=12,target=True))
  else:
   for row in range(5):
    width=5-row
    for col in range(width):
     x=(col-(width-1)/2)*25
     for z in (-16,16):
      self.boxes.append(Body(self,Vec3(x,10+row*19,z),Vec3(22,18,22),COLORS[(row+col)%6],3,target=True))
   for x in (-27,0,27):self.boxes.append(Body(self,Vec3(x,110,0),Vec3.ZERO,14,5,radius=10,target=True))
  self.origin={id(box):box.world_transform.pos for box in self.boxes}
  for box in self.boxes:
   box.collider.gravity=0
   box.collider.velocity=Vec3.ZERO
   box.collider.angular_velocity=Vec3.ZERO
   box.collider.mass=0
 def on_draw(self):
  # Place grid just above the collidable floor.
  self.depth_write(False);self.depth_offset(-.5)
  for q in range(-120,121,20):
   self.line(Vec3(q,.2,-110),Vec3(q,.2,110),5)
   self.line(Vec3(-130,.2,q),Vec3(130,.2,q),5)
 def fire(self):
  a=self.app
  if a.ammo<=0:return
  a.ammo-=1
  if not self.fired:
   self.fired=True
   self.fired_at=pyxel.frame_count
   for box in self.boxes:
    box.collider.gravity=9.8
    box.collider.mass=2
  angle=math.radians(self.camera_angle)
  direction=Vec3(-math.sin(angle),-.055,-math.cos(angle))
  start=Vec3(math.sin(angle)*125,49,math.cos(angle)*125)
  shot=Body(self,start,Vec3.ZERO,14,8,radius=10)
  shot.collider.velocity=direction*12
  shot.collider.angular_velocity=Vec3(2,3,4)
  self.shots.append(shot)
  pyxel.play(0,0)
 def assess(self):
  a=self.app
  for b in self.boxes:
   if b.cleared or not self.fired or pyxel.frame_count-self.fired_at<15:continue
   p=b.world_transform.pos
   start=self.origin.get(id(b),p)
   if abs(p.x-start.x)>26 or abs(p.z-start.z)>26 or p.y<start.y-19 or abs(p.x)>110 or abs(p.z)>100:
    b.cleared=True;a.score+=100*(1+a.combo//3);a.combo+=1;a.flash=12;pyxel.play(1,1)
  for b in list(self.shots):
   p=b.world_transform.pos
   if p.y< -20 or abs(p.x)>400 or abs(p.z)>400:
    self.shots.remove(b);b.destroy()

class Game:
 def __init__(self):
  pyxel.init(W,H,title='Towerfall Lab',fps=30)
  self.score=0;self.ammo=5;self.combo=0;self.flash=0;self.timer=0;self.state='title';self.level=0
  self.stage=Stage(self)
  pyxel.sounds[0].set('c3g2c2','n','6','f',7)
  pyxel.sounds[1].set('c4e4g4','p','6','n',9)
  pyxel.run(self.update,self.draw)
 def new(self):
  self.score=0;self.level=0;self.state='playing';self.load(0)
 def load(self,level):
  self.level=level;self.ammo=5+level;self.combo=0;self.timer=0;self.stage.load(level)
 def update(self):
  if self.state=='title':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):self.new()
   return
  if self.state in ('won','over'):
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):self.new()
   return
  if self.state=='stage':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
    if self.level==2:self.state='won'
    else:self.load(self.level+1);self.state='playing'
   return
  s=self.stage
  s.camera_angle+=int(pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT))*2
  s.camera_angle-=int(pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT))*2
  s.camera_pitch=max(-15,min(55,s.camera_pitch+int(pyxel.btn(pyxel.KEY_UP))-int(pyxel.btn(pyxel.KEY_DOWN))))
  if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):s.fire()
  s.look();s.update();s.assess()
  if self.flash:self.flash-=1
  self.timer+=1
  # Stage clear requires removing a third of the stack; spent ammunition
  # still gets a short settling window before result is measured.
  cleared=sum(b.cleared for b in s.boxes)
  if s.fired and cleared>=max(6,len(s.boxes)//3):self.state='stage';self.score+=self.ammo*150
  elif self.ammo==0 and self.timer>420:
   if cleared>=4:
    self.state='stage';self.score+=self.ammo*150
   else:self.state='over'
  
 def draw(self):
  pyxel.cls(1);self.stage.draw(0,0,W,H)
  if self.flash and self.flash%2:pyxel.rect(0,0,W,3,10)
  pyxel.rect(0,0,W,29,1);pyxel.line(0,28,W,28,5)
  pyxel.text(8,7,'TOWERFALL LAB',7)
  pyxel.text(8,18,'STAGE %d/3'% (self.level+1),10)
  pyxel.text(132,7,'SCORE %05d'%self.score,14)
  pyxel.text(252,7,'SHOTS %d'%self.ammo,7)
  pyxel.text(132,18,'COMBO x%d'%max(1,self.combo//3+1),10)
  pyxel.rect(0,H-27,W,27,1);pyxel.line(0,H-27,W,H-27,5)
  pyxel.text(8,H-19,'LEFT / RIGHT : ORBIT CAMERA    TAP / SPACE : FIRE',7)
  pyxel.text(8,H-10,'TOPPLE THE TOWERS. KEEP YOUR SHOTS.',7)
  if self.state!='playing':
   pyxel.rect(40,82,240,78,1);pyxel.rectb(40,82,240,78,10)
   pyxel.text(77,94,{'title':'THREE STRUCTURES. LIMITED SHOTS.','stage':'STRUCTURE DOWN. NEXT STAGE.','won':'LAB COMPLETE. PERFECT CHAOS.','over':'THE TOWER STILL STANDS.'}[self.state],7)
   pyxel.text(83,116,{'title':'MAKE THEM FALL FOR REAL','stage':'YOUR SCORE CARRIES OVER','won':'RUN IT BACK FOR A NEW SCORE','over':'ORBIT, AIM, AND TRY AGAIN'}[self.state],10)
   pyxel.text(88,141,'TAP / SPACE TO CONTINUE',7)
Game()
