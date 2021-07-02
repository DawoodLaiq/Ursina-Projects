from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()
player = FirstPersonController(collider = 'box')

ground = Entity(model='plane', scale=(50,1,50), color=color.white.tint(-0.2), texture='grass.jpg', collider='box')

lava = Entity(model='plane', scale=(50,1,50),texture='noise', color=color.red.tint(-0.2),position=(0,-16,0), collider='box' )
c = Cylinder(6, height=2, start=1)

goals = []
for i in range(3):
    finish = Entity(model = 'cube', scale=(2,2,2), color=color.green, collider = 'box', x =random.randint(-15,15), y =random.randint(3,15) ,z=random.randint(-15,15))
    goals.append(finish)
blocks= []

def input(key):
    global blocks
    if ground.hovered:
        if key == 'left mouse down':
            block = Entity(model='cube',color=color.red.tint(0.4),texture='brick', scale=(2,2,2),world_position=mouse.world_point, collider = 'box' )
            blocks.append(block)
            
    for block in blocks:
            if block.hovered == True: 
                if key == 'left mouse down': 
                    block = Entity(model='cube',color=color.red.tint(.4), texture='brick',scale=(2,2,2),position=mouse.world_point,collider = 'box' )
                    blocks.append(block)
                if key == 'right mouse down':
                    blocks.remove(block)
                    destroy(block)
    
def update(): 
    hit_info = player.intersects()
    if hit_info.hit:
        if hit_info.entity in goals:
            goals.remove(hit_info.entity)
            if len(goals) == 0:  
                message = Text(text = 'You WON', scale=2, origin=(0,0), background=True, color=color.blue)
                application.pause()
                mouse.locked = False
        if hit_info.entity == lava:
            message = Text(text = 'You LOST', scale=2, origin=(0,0), background=True, color=color.blue)
            application.pause()
            mouse.locked = False

def lavarise():
    lava.y += 1
    seq = invoke(lavarise, delay=5)

lavarise()
sky = Sky(color=color.orange.tint(0.8))
app.run()
