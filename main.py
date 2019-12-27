
#from nova import *
from classes import *
import pymunk.pygame_util


class Game(BaseScene):
    def __init__(self):
        pygame.init()
        self.window = WindowSDL()
        self.screen = self.window.display
        pygame.display.set_caption("DEMO")
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_data() #precacheo de recursos
        self.new() #inicialisacion de recursos

        pass

    def load_data(self):
        #CARGAR RECURSOS
        #self.map = Map(F_map, "LevelDemo2.tmx")
        self.map = Map(F_map, "jenga2.tmx")
        pass

    def new(self):
        self.space = pymunk.Space()
        self.space.gravity = vector(0, GRAVITY)
        self.map.data.convert_surfaces(self.screen,True)
        #self.map.layer.zoom=0.5
        self.entitySys = EntitySystem(self)
        self.SpritesGroup = Entity(self.entitySys,"2")
        self.SpritesGroup.addComponent(pyscroll.PyscrollGroup(map_layer=self.map.layer))



        self.hud=Text()
        self.mousePos= (0,0)

        self.block = []
        self.collisionTypes={"pointer":1,"block":2}


        dimensions = DIMENSIONS
        
        self.textMap = []
        with open(path.join(F_map, 'map.txt'), 'rt') as f:
            #x = f.read().splitlines() 
            #x = f.readlines()
            self.textMap = [line.split() for line in f]
            #for line in f:
             #   self.textMap.append(line)
        print(self.textMap)
        #print(self.textMap[0])
        #print(self.textMap[0][0])
        #print(x[0])
        
        #self.textMap = MAP
        #print(len(self.textMap))
        for i in range(len(self.textMap)):
            x = 290
            print(self.textMap[i])
            print(self.textMap[i][0])
            print(len(self.textMap[i][0]))
            for j in range(len(self.textMap[i][0])):
                """
                if self.textMap[i][j] == 1:
                    size = dimensions[0]
                                  
                if self.textMap[i][j] == 2:              
                    size = dimensions[1]
                    
                if self.textMap[i][j] == 3:    
                    size = dimensions[2]

                if self.textMap[i][j] == 4:    
                    size = dimensions[3]
                """
                #print((self.textMap[i][j]))
                #print(int(self.textMap[i][j][0]))
                size = dimensions[int(self.textMap[i][0][j])-1]
                x += int(size[0]/2)
                y = (432-size[1]/2) - (size[1]*i) 
                block = blocky(self,(x,y),size)
                x += int(size[0]/2)
                self.block.append(block)

        
        self.pointer = Entity(self.entitySys)
        self.pointer.addComponent(PointComponent())
        self.pointer.addComponent(CollisionComponent(self.pointer.component["PointComponent"].position,self.space,(1,1)))
        self.pointer.component["CollisionComponent"].body.body_type = pymunk.Body.KINEMATIC

        self.first = False
        self.pos = vector(0,0)

        def collisionPointer(arbiter, space, data):
            for c in arbiter.contact_point_set.points:
                p = (tuple(map(int, flipy(c.point_a))))
            if pygame.mouse.get_pressed()[0] == True:
                if self.first==False:
                    self.pos = self.mousePos - flipy(arbiter.shapes[1].body.position)
                    self.first = True
                newPos = flipy(self.mousePos - self.pos) 
                arbiter.shapes[1].body.position =  newPos
                arbiter.shapes[1].body.velocity = vector(0,0)
            else:
                self.first = False
            return False
        h=self.space.add_collision_handler(self.collisionTypes["pointer"],self.collisionTypes["block"])
        h.pre_solve = collisionPointer

        self.pointer.component["CollisionComponent"].shape.collision_type=self.collisionTypes["pointer"]


        for tile_object in self.map.tmx.objects:
            obj_center = vector(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'mesa':
                mesa = Entity(self.entitySys,"3")
                mesa.addComponent(PointComponent(obj_center))
                mesa.addComponent(CollisionComponent(mesa.component["PointComponent"].position,self.space,(tile_object.width,tile_object.height)))
                mesa.component["CollisionComponent"].body.body_type=pymunk.Body.STATIC
                #mesa.component["CollisionComponent"].body.elasticity = 0.95
                #mesa.component["CollisionComponent"].shape.elasticity = 0




        #self.events()
        #self.entitySys.update(self.SpritesGroup.component["PyscrollGroup"].view.center,self.map.data.map_size[0]*TILE)

    def draw_scene(self):
        self.hud.draw_text(['fps: '+str(self.clock.get_fps())[0:4],
                           ],self.screen)
        pygame.display.update(self.screen.get_rect())

    def update(self):

        if self.key_hit[pygame.K_r]:
            self.new()
        
        for i in range(len(self.block)):
            self.block[i].component["SpriteComponent"].change_layer(int(flipy(self.block[i].component["PointComponent"].position)[1]))
        self.space.step(1) 
        self.delta_time = self.clock.tick(FPS) / 1000 
        #self.SpritesGroup.component["PyscrollGroup"].center(self.player.component["PointComponent"].position)
        self.entitySys.update(self.SpritesGroup.component["PyscrollGroup"].view.center,1000)
        self.mousePos = [(pygame.mouse.get_pos()[0] + self.SpritesGroup.component["PyscrollGroup"].view.left), (pygame.mouse.get_pos()[1] + self.SpritesGroup.component["PyscrollGroup"].view.top)] 
        self.pointer.component["CollisionComponent"].body.position = flipy(self.mousePos)
        pass

    def events(self):
        BaseScene.events(self)
        pass


game = Game()

if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption('N O V A.')
    #intro.run()
    if game.running==True:
        game.run()
        pygame.quit()
