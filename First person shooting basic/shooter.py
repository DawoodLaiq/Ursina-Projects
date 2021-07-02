from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
app = Ursina()

# 1. Creating floor, walls and a barrier
ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
barrier = Entity(model = 'cube', scale=(20,2,0.5), color=color.orange, collider = 'box', x =0,z=2)
wall1 = Entity(model = 'cube', scale=(20,12,1), color=color.white50, collider = 'box', x =0,z=-2)
wall2 = Entity(model = 'cube', scale=(20,12,1), color=color.white50, collider = 'box', x =0,z=22)
wall3 = Entity(model = 'cube', scale=(24,12,1), color=color.white50, collider = 'box', x =-10,z=10, rotation_y = 90)
wall4 = Entity(model = 'cube', scale=(24,12,1), color=color.white50, collider = 'box', x =10,z=10, rotation_y = 90)

#2. Creating bullet and moving target list 
bullets = []
moving_targets = []

#3. Creating six random locations for six moving targets
for i in range(6):
    x = random.randrange(-9,9,2)
    y = random.randrange(1,6,1)
    z = random.randrange(3,21,2)
    moving_target = Entity(model='cube', color=color.white,texture='target.jpg',scale=(1,1,0.1),dx=0.05, position=(x,y,z), collider='box')
    moving_targets.append(moving_target)

#4. Creating a gun entity that is attached to the player (parent=camera)
gun = Entity(parent=camera, model='cube', color=color.gray, origin_y=-0.5, scale= (0.5,0.5,2), position=(2,-1,2.5), collider='box')

#5. Creating an entity which works like a first person shooter
player = FirstPersonController(model='cube', y=0, origin_y=-.5)
player.gun = gun

#6. Creating an input function where bullets are made after left mouse click
def input(key):
    global bullets
    if key == 'left mouse down' and player.gun:
        bullet = Entity(parent=gun, model='cube', scale=.1, position=(0,0.5,0),speed = 3, color=color.black,collider='box')
        bullets.append(bullet)
        gun.blink(color.white)
        bullet.world_parent = scene
        
#7. Creating an update function where moving targets are moving left and right continously and the bullet goes forward from the gun.
#   if the bullet hits the moving target it gets destroyed. Hit all of them to win.
def update():

    for m in moving_targets:
        m.x += m.dx
        if m.x > 9:
            m.x = 9
            m.dx *=-1
        if m.x < -9:
            m.x = -9
            m.dx *=-1

    global bullets
    if len(bullets) > 0:
        for b in bullets:
            b.position += b.forward * 8
            hit_info = b.intersects()
            if hit_info.hit:
                if hit_info.entity in moving_targets:
                    moving_targets.remove(hit_info.entity)
                    destroy(hit_info.entity)
                    if len(moving_targets) == 0:
                        message = Text(text = 'YOU WON', scale=2, origin=(0,0), background=True, color=color.blue)
                        application.pause()


      
app.run()