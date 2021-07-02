from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController
app = Ursina()


# 1. Making the grid and water texture
grid = Entity(model=Grid(20,20), scale=50, color=color.white, rotation_x=90, y = -1, collider = 'box')
water = Entity(model= Plane(subdivisions=(2,8)), scale=50, color=color.white,texture='water.png', rotation_x=0, y = -0.5)

# 2. Making boundries
wall1 = Entity(model = 'cube', scale=(20,12,1), color=color.black, collider = 'box', x =0,z=-2)
wall2 = Entity(model = 'cube', scale=(20,12,1), color=color.black, collider = 'box', x =0,z=22)
wall3 = Entity(model = 'cube', scale=(24,12,1), color=color.black, collider = 'box', x =-10,z=10, rotation_y = 90)
wall4 = Entity(model = 'cube', scale=(24,12,1), color=color.black, collider = 'box', x =10,z=10, rotation_y = 90)

# 3. Making spawn entity and finish entity
start = Entity(model = 'cube', scale=(2,1,2), color=color.red, collider = 'box', x =0,z=0)
finish = Entity(model = 'cube', scale=(2,1,2), color=color.green, collider = 'box', x =0,z=20)

# 4. Making random blocks on the floor
cords = []
blocks = []
z = 0
x = 0
for i in range(6):
    z += 3
    for u in range(3):
        x = random.randrange(-8,8,3) 
        cords.append((x,z))
        print(cords)
        bb = Entity(model = 'cube', scale=(2,1,2), color=color.orange,texture='stone.jpg', collider = 'box', x =x,z=z)
        blocks.append(bb)

# 5. Making the player in first person mode
fpc = FirstPersonController(model='cube',collider = 'box', position=(0.5,1,0.5))

# 6. Making an update function where if you hit the blocks you have 2 seconds to jump to another or else you will lose.
#    If you jump your way to the green block you win.
def update():   
    count = 0   
    hit_info = fpc.intersects()
    if hit_info.hit:
        if hit_info.entity in blocks:
            hit_info.entity.fade_out(duration=2)
            destroy(hit_info.entity,delay=2)
        elif hit_info.entity == grid:
            end_game('YOU LOSE')    
        elif hit_info.entity == finish:    
            end_game('YOU WON ')
            
            
# 7. Making a message function for end game when the player loses or wins.          
def end_game(user_message):
    message = Text(text = user_message, scale=2, origin=(0,0), background=True, color=color.blue)
    application.pause()
    mouse.locked = False

app.run()