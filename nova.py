import pygame
import pytmx
import pyscroll
import pymunk
#import pymunk.util as u
#import classes
#from classes import *
from settings import *
from os import path
import sys
from math import cos,sin,sqrt

config_name = 'myapp.cfg'
if getattr(sys, 'frozen', False):
    application_path = path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
else:
    try:
        app_full_path = path.realpath(__file__)
        application_path = path.dirname(app_full_path)
        #running_mode = "Non-interactive (e.g. 'python myapp.py')"
    except NameError:
        application_path = getcwd()
        running_mode = 'Interactive'

#print("running mode: "+running_mode)
FOLDER = application_path
F_img = path.join(FOLDER, "imgs")
F_map = path.join(FOLDER, "maps")
F_font = path.join(FOLDER, "fonts")
vector = pygame.math.Vector2

class Map():
    def __init__(self,folder,file):
        self.tmx = pytmx.load_pygame(path.join(folder,file))
        self.data = pyscroll.data.TiledMapData(self.tmx)
        self.layer = pyscroll.BufferedRenderer  (self.data,
                                                (WIDTH, HEIGHT),
                                                clamp_camera=True)

class Game0bj() :
    def __init__(self, game):
        self.game = game

class Text():
    def __init__(self,size=16,color=COLOR_DEBUG, bkgcolor=COLORS["BLACK"]):
        self.name='Text'
        self.size=size
        #self.font = pygame.font.SysFont("arial", self.size)
        self.font=pygame.font.Font(path.join(F_font,'Inconsolata-Regular.ttf'),self.size)
        self.color = color
        self.bkgcolor = bkgcolor
        self.image = self.font.render(str(''), 1, self.color)
    def draw_text(self,src_txt,target,x=0,y=0):
        for i in range(0,len(src_txt)):
            self.image = self.font.render(src_txt[i], True, self.color,self.bkgcolor)
            target.blit(self.image,(x,y+i*self.size))

class BaseScene():
    def _init_(self):
        self.name='BaseScene'
        pass
    def load_data(self):
        pass
    def new(self):
        pass
    def update(self):
        pass
    def draw_scene(self):
        pass
    def events(self): 
        self.key_hit=pygame.key.get_pressed()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (self.key_hit[pygame.K_ESCAPE]):
                self.running = False
                print("Procesado evento de salir")
                #pygame.quit()
                #exit()
        pass
        pass
    def run(self):
        #try:
            while self.running:
                self.events()

                self.draw_scene()

                self.update()
        #except KeyboardInterrupt:
            #if self.running==False:
             #   self.running = False
              #  print("Saliedo...")
               # pygame.quit()
        #pass

######ECS


class PointComponent():
    def __init__(self,x=0,y=0,r=0):
        self.position= vector(x,y)
        self.rotation= r
        
class CollisionComponent():
    def __init__(self,position,space,rect=(TILE,TILE),offset=(0,0),angle=0,mass=1):
        self.referece=self
        self.collisionRect = pygame.Rect(0,0,rect[0],rect[1])
        moment = pymunk.moment_for_box(mass, rect)
        self.body = pymunk.Body(mass, moment)
        self.shape = pymunk.Poly.create_box(self.body, rect)
        self.shape.friction = 1
        self.body.position = flipy(position)
        self.body.angle = (angle /(180/3.14))
        self.offset = offset
        self.space = space
        self.space.add(self.body, self.shape)
        #self.body.sleep()
        """
    def drawRect(self,screen,group):
        rect=(self.collisionRect.left-group.view.left, self.collisionRect.top-group.view.top, self.collisionRect.width, self.collisionRect.height)
        pygame.draw.rect(screen,COLORS["GREEN"],rect,1)
        #self.gameObj.hud.draw_text([str(type(entity))],self.gameObj.screen,component.collisionRect.x,component.collisionRect.y)
    def draw_poly(self, screen):      
        #body = self.body
        ps = [p.rotated(self.body.angle) + self.body.position for p in self.shape.get_vertices()]
        ps.append(ps[0])
        ps = list(map(self.flipyv, ps))
        if u.is_clockwise(ps):
            #color = THECOLORS["green"]
            color = COLOR_DEBUG
        else:
            color = COLORS["RED"]
        pygame.draw.lines(screen, color, False, ps)
        """
    def drawBox(self,screen,group):
        self.collisionRect.center = flipy(self.body.position)
        rectInsideGroup=(self.collisionRect.left-group.view.left, self.collisionRect.top-group.view.top, self.collisionRect.width, self.collisionRect.height)
        rect=pygame.Rect(rectInsideGroup)
        points=(rect.topleft,rect.topright,rect.bottomright,rect.bottomleft)
        points2=[]
        for p in points:
            points2.append(rotate(rect.center,p,-self.body.angle))

        pygame.draw.lines(screen, COLOR_DEBUG, True, points2)
    def flipyv(self, v):
        return int(v.x), int(-v.y+HEIGHT)

class BehaviourComponent():
    def __init__(self,entity):
        #self.componentName = "behaviour"
        self.componentsToBehave=entity.component
    def updateBehaviour(self):
        pass
        
class SpriteComponent(pygame.sprite.Sprite):
    def __init__(self,image,group,layer=1,
                centerX=None,centerY=None,rotation=None,spritePos=None,size=(0,0),
                step=1,animation_type=1,frame_duration=1):
        self._layer = layer
        pygame.sprite.Sprite.__init__(self)
        group.add(self)
        self.group = group
        #self.imagesKeyframes=[]
        self.imagesKeyframesOriginal=[]
        self.keyframe_len = len(image)
        self.frame = 0
        self.frame_position = 0
        self.frame_step = step #1)beg_to_end|-1)end_to_beg
        self.frame_duration = frame_duration # duracion en frames por key
        self.animation_type = animation_type #1-cycle|2-bounce|3-once
        for i in range(self.keyframe_len):         
            self.imagesKeyframesOriginal.append(pygame.image.load(path.join(F_img,image[i])))
        self.modify(i,centerX,centerY,rotation,size)
        self.image = self.imagesKeyframesOriginal[0]     
        self.rect = self.image.get_rect()
        if spritePos != None:
            self.rect.center = spritePos
        self.size = size
        self.rotSprite = 0
        self.finished = False
    def modify(self,i,x,y,rotation,size):
        for i in range(self.keyframe_len):
            if x == None or y == None:
                #x e y positionicionan el centro de la imagen para la rotacion
                #surface = pygame.Surface((self.image.get_width(),self.image.get_height()))
                surface = self.imagesKeyframesOriginal[i]
            else:
                _w = surface.get_width()
                _h = surface.get_height()
                surface = pygame.Surface((_w*2,_h*2))
                surface.blit(surface,(_w-x,_h-y))
            if rotation != None:
                surface = pygame.transform.rotate(surface,rotation)
            if size != (0,0):
                #size=(size[0]/100,size[1]/100)
                #surface = pygame.transform.scale(surface,(int(surface.get_width()*size[1]),int(surface.get_height()**size[0])))
                #size=(size[0]/100,size[1]/100)
                surface = pygame.transform.scale(surface,size)
            self.imagesKeyframesOriginal[i] = surface
    def change_key(self):
        if self.frame in range(self.keyframe_len-1):
            self.frame += self.frame_step
        else:
            if self.animation_type == 1:
                self.frame = 0
            if self.animation_type == 2:
                self.frame_step = -self.frame_step
                self.frame += self.frame_step
            if self.animation_type == 3:
                self.finished = True
                pass
    def updateFrame(self):
        self.frame_position += 1
        if self.frame_position == self.frame_duration :
            self.change_key()
            self.frame_position = 0
    def updateSpriteAnimation(self):
        self.image = pygame.transform.rotate(self.imagesKeyframesOriginal[self.frame],self.rotSprite)
        self.rect= self.image.get_rect()
        self.updateFrame()
        pass
    def change_layer(self,layer):
        self.group.change_layer(self,layer)    

class Entity():
    def __init__(self,entitySystem,name = "1"):
        self.component = {}
        self.active = True
        self.name = name
        entitySystem.addEntity(self)
    def addComponent(self,source):
        self.component[source.__class__.__name__] = source
    def removeComponent(self,source):
        self.component.pop(source)
        
class EntitySystem():
    def __init__(self,gameObj):
        self.gameObj = gameObj
        self.list= []
    def addEntity(self,source):
        self.list.append(source)
        #self.list[type(source)] = source
    def removeEntity(self,source):
        self.list.remove(source)
    def update(self,center,ratio):
        pass
        for entity in self.list:
         
            if "PointComponent" in entity.component:
                if dist(entity.component["PointComponent"].position,center) < ratio*1.2:
                                  
                    if "PointComponent" in entity.component:
                        position = entity.component["PointComponent"].position
                        rotation = entity.component["PointComponent"].rotation
                    
                    if "CollisionComponent" in entity.component:
                        #if (entity.component["CollisionComponent"].body.is_sleeping):
                         #   entity.component["CollisionComponent"].body.activate()
                          #  pass
                        
                        position = flipy(entity.component["CollisionComponent"].body.position) + vector(entity.component["CollisionComponent"].offset)
                        rotation = (entity.component["CollisionComponent"].body.angle) * 180/3.14
                        entity.component["PointComponent"].position = position 
                        entity.component["PointComponent"].rotation = rotation
                        #entity.component["CollisionComponent"].drawBox(self.gameObj.screen,self.gameObj.SpritesGroup.component["PyscrollGroup"])

                        if entity.component["CollisionComponent"].body.space == None:
                            entity.active = False

                    if "SpriteComponent" in entity.component:
                        entity.component["SpriteComponent"].rotSprite = rotation
                        entity.component["SpriteComponent"].updateSpriteAnimation()                 
                        entity.component["SpriteComponent"].rect.center = position 
                        if entity.component["SpriteComponent"].finished==True:
                            entity.active=False
                    
                    if "Behaviour" in entity.component:
                        entity.component["Behaviour"].updateBehaviour()

                if dist(entity.component["PointComponent"].position,center) > ratio*2:
                    if "CollisionComponent" in entity.component:
                        if entity.component["CollisionComponent"].body.is_sleeping == False:
                            #entity.component["CollisionComponent"].body.sleep()
                            pass
            
            if entity.active==False:
                entity.removeComponent('PointComponent')
                entity.component['SpriteComponent'].group.remove(entity.component['SpriteComponent'])
                entity.removeComponent('SpriteComponent')
                if "CollisionComponent" in entity.component:
                    entity.removeComponent('CollisionComponent')
                if "Behaviour" in entity.component:
                    entity.removeComponent('Behaviour')
                self.list.remove(entity)  
            
            if "PyscrollGroup" in entity.component:
                entity.component["PyscrollGroup"].draw(self.gameObj.screen)

    def returnList(self):
        for i in range(len(self.list)):
            return str(self.list[i].name)
class WindowSDL():
    def __init__(self,width=WIDTH,height=HEIGHT):
        
        _flags = 0
        #_flags = pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.RESIZABLE
        self.display = pygame.display.set_mode((width, height), _flags )
        self.display.set_alpha(None)

def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return vector(p[0], -p[1]+HEIGHT)

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return qx, qy

def dist(d1,d2):
    #dist = sqrt((d1.x-d2.x)**2 + (d1.y-d2.y)**2)
    dist = sqrt((d1[0]-d2[0])**2 + (d1[1]-d2[1])**2)
    return dist
