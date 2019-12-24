from nova import *
#import nova
from random import randrange,choice


collisionTypes={"pointer":1,"block":2}

def blocky(game,position,size):
    block = Entity(game.entitySys)
    #k = 40
    #block.addComponent(PointComponent(320 - l + j,450 - (i*k) ))            
    block.addComponent(PointComponent(position))
    block.addComponent(SpriteComponent(["block.png"],game.SpritesGroup.component["PyscrollGroup"],size = size))
    position = block.component["PointComponent"].position 
    #k=20
    size = block.component["SpriteComponent"].image.get_size()# + vector(0,-k)
    block.addComponent(CollisionComponent(position,game.space,size))#,offset=(0,-k/2)))
    block.component["CollisionComponent"].shape.collision_type=collisionTypes["block"]
    block.component["CollisionComponent"].body.velocity_func = limit_velocity
    block.component["CollisionComponent"].shape.friction = FRICTION 
    block.component["CollisionComponent"].shape.mass = MASS
    block.component["CollisionComponent"].shape.elasticity = ELASTICITY
    return block
    pass

def limit_velocity(body, gravity, damping, dt):
    max_velocity = MAX_VEL
    pymunk.Body.update_velocity(body, gravity, damping, dt)
    #print(body.velocity.length)
    if body.velocity.length > max_velocity:
        body.velocity = body.velocity * VEL_DAMP    
