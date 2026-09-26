# title: Orbit Orchard
# desc: Collect glowing fruit in a rotating 3D orchard.
import pyxel, math, random
from pyxel.cube import Camera, Mat4, Node, Shading, Vec3

MODE = 'orchard'
W,H=240,180
random.seed(8)

class World(Node):
    def __init__(self, game):
        super().__init__(); self.game=game
        self.shading=Shading(pyxel.colors); self.camera=Camera()
        self.camera.clear_color=1; self.camera.far=1500
        self.camera.transform=Mat4.look_at(Vec3(145,150,210),Vec3(0,0,0))
    def on_draw(self):
        g=self.game; t=pyxel.frame_count
        # a dark tiled stage with readable edging
        self.box(Mat4.from_translation(Vec3(0,-6,0)),Vec3(170,10,170),1)
        self.depth_write(False); self.depth_offset(-0.5)
        for q in range(-80,81,20):
            self.line(Vec3(q,0,-80),Vec3(q,0,80),5)
            self.line(Vec3(-80,0,q),Vec3(80,0,q),5)
        for p in g.plants:
            x,z=p
            self.box(Mat4.from_translation(Vec3(x,8,z)),Vec3(3,16,3),4)
            self.box(Mat4.from_translation(Vec3(x,19,z)),Vec3(15,11,15),11)
        for i,(x,z,phase) in enumerate(g.fruit):
            if i in g.taken: continue
            y=10+3*math.sin(t*.09+phase)
            self.sphere(Vec3(x,y,z),5,10 if i%3 else 14)
            self.sphere(Vec3(x-1,y+3,z),1.4,7)
        # avatar with two ears and a luminous center
        x,z=g.x,g.z
        self.box(Mat4.from_translation(Vec3(x,7,z)),Vec3(11,13,10),12)
        self.box(Mat4.from_translation(Vec3(x-4,16,z)),Vec3(3,8,3),12)
        self.box(Mat4.from_translation(Vec3(x+4,16,z)),Vec3(3,8,3),12)
        self.sphere(Vec3(x,10,z+5),2.6,7)

class Game:
    def __init__(self):
        pyxel.init(W,H,title='Orbit Orchard',fps=30)
        self.reset(); self.scene=World(self)
        pyxel.sounds[0].set('c4e4g4c4','p','6','n',12)
        pyxel.sounds[1].set('c3a2','p','5','n',14)
        pyxel.run(self.update,self.draw)
    def reset(self):
        self.x=0.;self.z=0.;self.score=0;self.taken=set();self.time=30*75;self.state='title'
        self.plants=[(-64,-60),(58,-60),(-63,52),(57,57),(0,-50)]
        self.fruit=[(-42,-37,0),(26,-50,1),(49,-12,2),(38,38,3),(-12,52,4),(-49,16,5),(5,4,6),(-18,-18,7),(-8,-59,8),(62,55,9)]
    def update(self):
        if self.state!='playing':
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset();self.state='playing'
            self.scene.update();return
        dx=(pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT))-(pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT))
        dz=(pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN))-(pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP))
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            mx,my=pyxel.mouse_x,pyxel.mouse_y
            if my<155:
                dx+= (1 if mx>W*.55 else -1 if mx<W*.45 else 0)
                dz+= (1 if my>H*.57 else -1 if my<H*.43 else 0)
        mag=max(1,math.hypot(dx,dz));self.x=max(-76,min(76,self.x+dx*2.3/mag));self.z=max(-76,min(76,self.z+dz*2.3/mag))
        for i,(x,z,_) in enumerate(self.fruit):
            if i not in self.taken and (x-self.x)**2+(z-self.z)**2<115:
                self.taken.add(i);self.score+=1;pyxel.play(0,0)
        self.time-=1
        if self.score==len(self.fruit): self.state='won';pyxel.play(0,0)
        elif self.time<=0: self.state='over';pyxel.play(0,1)
        self.scene.update()
    def draw(self):
        pyxel.cls(1);self.scene.draw(0,0,W,H)
        pyxel.rect(0,0,W,25,1);pyxel.line(0,24,W,24,5)
        pyxel.text(8,7,'ORBIT ORCHARD',7);pyxel.text(113,7,'FRUIT %02d/10'%self.score,10)
        pyxel.text(201,7,'%02d'%max(0,self.time//30),14)
        pyxel.rect(0,159,W,21,1);pyxel.line(0,158,W,158,5)
        pyxel.text(8,166,'ARROWS / WASD TO MOVE  -  GET ALL TEN',7)
        if self.state!='playing':
            pyxel.rect(22,59,196,62,1);pyxel.rectb(22,59,196,62,10)
            pyxel.text(54,70,'THE ORCHARD IS WAITING',7)
            line='PICK UP ALL 10 FRUIT' if self.state=='title' else ('ALL FRUIT COLLECTED!' if self.state=='won' else 'THE ORCHARD WENT DARK')
            pyxel.text(63,84,line,10)
            pyxel.text(68,105,'TAP / SPACE TO START' if self.state=='title' else 'TAP / SPACE TO REPLAY',7)
Game()
