# title: Neon Coast
# desc: An original top-down 3D coastal city courier chase.
import pyxel, math, random
from pyxel.cube import Node, Camera, Mat4, Vec3, Shading
W,H=320,240
random.seed(22)
BLOCKS=[]
for gx in range(-2,3):
 for gz in range(-2,3):
  if (gx,gz) in ((0,0),(-1,0),(1,1)):continue
  x,z=gx*55,gz*55
  h=18+(abs(gx*9+gz*13)*7)%36
  BLOCKS.append((x,z,h, [5,6,12,9,13][(gx+2*gz)%5]))
CHECKPOINTS=[(-82,-55,'DOCKS'),(82,-110,'NORTH PIER'),(82,110,'PALMS'),(-82,110,'LIGHTHOUSE')]
class Scene(Node):
 def __init__(self,g):
  super().__init__();self.g=g;self.camera=Camera();self.camera.clear_color=1;self.camera.far=1000;self.shading=Shading(pyxel.colors)
 def on_draw(self):
  g=self.g;t=pyxel.frame_count
  self.box(Mat4.from_translation(Vec3(0,-8,0)),Vec3(330,14,330),5)
  # Crosscut roads frame nine walkable districts.
  for p in [-82,-27,27,82]:
   self.box(Mat4.from_translation(Vec3(p,-.5,0)),Vec3(16,1,320),1)
   self.box(Mat4.from_translation(Vec3(0,-.4,p)),Vec3(320,1,16),1)
  self.depth_write(False);self.depth_offset(-.8)
  for p in [-82,-27,27,82]:
   for mark in range(-148,149,24):
    self.line(Vec3(p,.2,mark),Vec3(p,.2,mark+10),10)
    self.line(Vec3(mark,.2,p),Vec3(mark+10,.2,p),10)
  # Coastal seawall and seawater: the game's west edge.
  self.box(Mat4.from_translation(Vec3(-162,0,0)),Vec3(7,6,318),7)
  for z in range(-150,151,19):self.line(Vec3(-170,2,z),Vec3(-170,2,z+11),12)
  for i,(x,z,h,col) in enumerate(BLOCKS):
   self.box(Mat4.from_translation(Vec3(x,h/2,z)),Vec3(31,h,32),col)
   self.box(Mat4.from_translation(Vec3(x,h+.6,z)),Vec3(32,2,33),7)
   self.box(Mat4.from_translation(Vec3(x,h+3,z)),Vec3(7,4,7),14)
   # warm window bands on the road-facing facade
   for y in range(8,h-4,11):
    for dx in (-9,1,10):
     self.rect(Mat4.from_translation(Vec3(x+dx,y,z+16.2)),4,4,10 if i%3 else 14)
  # Palm row frames the waterfront.
  for z in (-130,-70,0,74,138):
   self.box(Mat4.from_translation(Vec3(-132,9,z)),Vec3(3,18,3),4)
   for dx,dz in [(-9,0),(9,0),(0,-9),(0,9)]:
    self.box(Mat4.from_translation(Vec3(-132+dx/2,20,z+dz/2)),Vec3(13,2,5),3)
  for i,(x,z) in enumerate(g.traffic):
   self.box(Mat4.from_translation(Vec3(x,4,z)),Vec3(12,7,18),8 if i%2 else 14)
   self.box(Mat4.from_translation(Vec3(x,8,z)),Vec3(10,2,8),7)
  for x,z in g.patrol:
   self.box(Mat4.from_translation(Vec3(x,4,z)),Vec3(12,7,18),12)
   self.box(Mat4.from_translation(Vec3(x,8,z)),Vec3(9,2,8),7)
   if (t//8)%2:self.sphere(Vec3(x,10,z-4),2,8)
  if g.mission<4:
   x,z,name=CHECKPOINTS[g.mission]
   self.boxb(Mat4.from_translation(Vec3(x,3,z)),Vec3(16,6,16),14)
   self.sphere(Vec3(x,15+math.sin(t*.08)*3,z),7,14)
  if g.car:
   self.box(Mat4.from_translation(Vec3(g.x,5,g.z))*Mat4.from_euler(Vec3(0,g.heading,0)),Vec3(14,8,24),11)
   self.box(Mat4.from_translation(Vec3(g.x,10,g.z))*Mat4.from_euler(Vec3(0,g.heading,0)),Vec3(11,3,11),7)
  else:
   self.box(Mat4.from_translation(Vec3(g.x,5,g.z)),Vec3(5,10,5),12)
   self.sphere(Vec3(g.x,12,g.z),4,14)

class Game:
 def __init__(self):
  pyxel.init(W,H,title='Neon Coast',fps=30)
  self.reset();self.scene=Scene(self)
  pyxel.sounds[0].mml('T240 O4 C8 E8 G8 >C8')
  pyxel.sounds[1].mml('T150 O3 C8 R8 C8')
  pyxel.run(self.update,self.draw)
 def reset(self):
  self.x,self.z=0.,0.;self.heading=0.;self.speed=0.;self.car=True
  self.traffic=[(-82,-90),(82,75),(27,-54),(-27,115)]
  self.patrol=[(-82,112),(82,-124)]
  self.heat=0.;self.mission=0;self.cash=0;self.time=0;self.state='title';self.msg='PICK UP THE DOCKS PARCEL';self.msg_until=190
 def position_camera(self):
  # A following camera that tracks the city, not a fixed gameboard view.
  x,z=self.x,self.z
  self.scene.camera.transform=Mat4.look_at(Vec3(x+107,135,z+135),Vec3(x,0,z))
 def road_collision(self,x,z):
  if not (-150<x<150 and -150<z<150):return True
  for bx,bz,h,c in BLOCKS:
   if abs(x-bx)<19 and abs(z-bz)<19:return True
  return False
 def update(self):
  if self.state!='playing':
   if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
    self.reset();self.state='playing'
   self.position_camera();self.scene.update();return
  self.time+=1
  if pyxel.btnp(pyxel.KEY_E) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_y>205 and pyxel.mouse_x>250):
   self.car=not self.car;self.speed=0;self.msg='ON FOOT' if not self.car else 'BACK BEHIND THE WHEEL';self.msg_until=self.time+50
  left=pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and 75<pyxel.mouse_y<205 and pyxel.mouse_x<90)
  right=pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and 75<pyxel.mouse_y<205 and pyxel.mouse_x>230)
  up=pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_y<75)
  down=pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and 75<pyxel.mouse_y<205 and 90<pyxel.mouse_x<230)
  if self.car:
   self.heading+=(int(right)-int(left))* (2.7 if abs(self.speed)>.3 else 1.3)
   self.speed=max(-2.1,min(4.2,self.speed+(0.17 if up else -0.12 if down else 0)))
   self.speed*=.98 if not (up or down) else .994
   a=math.radians(self.heading)
   nx,nz=self.x+math.sin(a)*self.speed,self.z-math.cos(a)*self.speed
  else:
   dx,dz=int(right)-int(left),int(down)-int(up)
   n=max(1,math.hypot(dx,dz));nx,nz=self.x+dx*1.8/n,self.z+dz*1.8/n
  if self.road_collision(nx,nz):
   if abs(self.speed)>2.5:self.heat=min(100,self.heat+9);pyxel.play(1,1)
   self.speed*=-.27
  else:self.x,self.z=nx,nz
  # Traffic circulates on city roads; contact raises a wanted meter.
  for i,(x,z) in enumerate(self.traffic):
   if i%2==0:z+=.8 if i==0 else -.9
   else:x+=.7 if i==1 else -.6
   if z>145:z=-145
   if z< -145:z=145
   if x>145:x=-145
   if x< -145:x=145
   self.traffic[i]=(x,z)
   if (x-self.x)**2+(z-self.z)**2<145 and self.car and self.time%20==0:
    self.heat=min(100,self.heat+15);self.msg='TRAFFIC HIT + WANTED';self.msg_until=self.time+50;pyxel.play(1,1)
  if self.heat>0:self.heat=max(0,self.heat-.025)
  for i,(x,z) in enumerate(self.patrol):
   if self.heat>15:
    dx,dz=self.x-x,self.z-z;norm=max(1,math.hypot(dx,dz));nx, nz=x+dx/norm*.75,z+dz/norm*.75
    if not self.road_collision(nx,nz):x,z=nx,nz
    else:z+=.32 if i==0 else -.32
    if norm<12 and self.time%30==0:self.heat=max(0,self.heat-30);self.cash=max(0,self.cash-50);self.msg='FINES PAID. KEEP MOVING';self.msg_until=self.time+65
   else:z+=.35 if i==0 else -.35
   if z>145:z=-145
   if z< -145:z=145
   self.patrol[i]=(x,z)
  if self.mission<4:
   tx,tz,name=CHECKPOINTS[self.mission]
   if (self.x-tx)**2+(self.z-tz)**2<220:
    self.mission+=1;self.cash+=150+self.mission*50
    self.msg='DROP DELIVERED +$%d'%(150+self.mission*50)
    self.msg_until=self.time+90;pyxel.play(0,0)
    if self.mission==4:self.state='won'
  self.position_camera();self.scene.update()
 def draw(self):
  pyxel.cls(1);self.scene.draw(0,0,W,H)
  pyxel.rect(0,0,W,31,1);pyxel.line(0,30,W,30,5)
  pyxel.text(8,7,'NEON COAST',7);pyxel.text(119,7,'CASH $%04d'%self.cash,10)
  pyxel.text(235,7,'HEAT %02d'%self.heat,8 if self.heat>30 else 7)
  pyxel.text(8,20,'DROP %d/4'%self.mission,14)
  pyxel.text(88,20,'NEXT: '+(CHECKPOINTS[self.mission][2] if self.mission<4 else 'ALL DONE'),7)
  if self.time<self.msg_until:pyxel.text(177,20,self.msg[:23],10)
  pyxel.rect(0,H-33,W,33,1);pyxel.line(0,H-33,W,H-33,5)
  pyxel.text(8,H-26,'W/S DRIVE  A/D STEER  E WALK / DRIVE',7)
  pyxel.text(8,H-15,'FOLLOW THE GOLD MARKER. AVOID TRAFFIC.',7)
  # Navigable mini map in the bottom right.
  pyxel.rect(258,152,54,54,0);pyxel.rectb(258,152,54,54,7)
  for q in (-82,-27,27,82):
   k=285+q*.15;pyxel.line(k,154,k,204,5);pyxel.line(260,179+q*.15,310,179+q*.15,5)
  px,pz=285+self.x*.15,179+self.z*.15
  pyxel.circ(px,pz,2,12)
  if self.mission<4:
   tx,tz,_=CHECKPOINTS[self.mission];pyxel.circ(285+tx*.15,179+tz*.15,2,14)
  if self.state!='playing':
   pyxel.rect(27,68,266,96,1);pyxel.rectb(27,68,266,96,10)
   pyxel.text(111,80,'NEON COAST',7)
   pyxel.text(56,99,'FOUR DELIVERIES. ONE COASTAL CITY.',10)
   pyxel.text(51,115,{'title':'TRAFFIC, PATROL, AND A WANTED METER','won':'ALL DELIVERIES DONE. NIGHT IS YOURS.'}[self.state],7)
   pyxel.text(97,144,'TAP / SPACE TO '+('START' if self.state=='title' else 'REPLAY'),7)
Game()
