import pygame
import screeninfo
import defines.colors as colors
import game.tilesystem
import game.generator
import game.entitysystem
import game.lightsystem
import configloader as config
import random

monitor=screeninfo.get_monitors()[0]

class Runner:
    def __init__(self, tps:int,  width: int=480, height:int=360):
        self.width=width
        self.height=height
        self.tps=tps
        pygame.init()
        self.screen=pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Maze")
        
        self.clock = pygame.time.Clock()
        self.clock.tick(tps)
        self.working=True
        self.deltaTime=0.0
        self.keysPressed=[]
                
        temp=colors.getColor(config_dict.get("tileColor", "red"))
        if temp==None:
            tileColor=colors.parseColor(config_dict.get("tileColor"))
        else:
            tileColor=temp
        temp=colors.getColor(config_dict.get("wallColor", "dark_gray"))
        if temp==None:
            wallColor=colors.parseColor(config_dict.get("wallColor"))
        else:
            wallColor=temp
        temp=colors.getColor(config_dict.get("hiddenColor", "black"))
        if temp==None:
            hiddenColor=colors.parseColor(config_dict.get("hiddenColor"))
        else:
            hiddenColor=temp
        self.tileset=game.tilesystem.Tileset(config_dict.get("width", 10), config_dict.get("height", 10), tileColor, wallColor, hiddenColor)
        
        basegen=random.randint(-2147483648, 2147483647) # Просто из Java Integer.MIN_VALUE и MAX_VALUE (-(2^32) и (2^32)-1 соответственно)
        generator=config_dict.get("generator", None)
        if isinstance(generator, dict):
            temp=generator.get("randomSeed", basegen) 
            
            if isinstance(temp, str):
                if len(temp)==0:
                    temp=basegen
                else: 
                    try:
                        temp=int(temp)
                    except ValueError:
                        temp=basegen
            random.seed(temp)
        
        else:
            random.seed(basegen)
            
        
        temp=colors.getColor(config_dict.get("startColor", "green"))
        if temp==None:
            startColor=colors.parseColor(config_dict.get("startColor"))
        else:
            startColor=temp
        temp=colors.getColor(config_dict.get("endColor", "yellow"))
        if temp==None:
            endColor=colors.parseColor(config_dict.get("endColor"))
        else:
            endColor=temp
        game.generator.generate(self.tileset, startColor, endColor)
        
        temp=colors.getColor(config_dict.get("playerColor", "cyan"))
        if temp==None:
            playerColor=colors.parseColor(config_dict.get("playerColor"))
        else:
            playerColor=temp
        self.entitysystem=game.entitysystem.EntitySystem()
        temp=config_dict.get("playerSpeed", 1)
        for c in self.tileset.getSpawns():
            x, y= c
            self.entitysystem.createPlayer(x, y, playerColor, (1.0/temp))
            
        self.lightMode=config_dict.get("lightMode", "off")
        self.lightsystem=game.lightsystem.LightSystem(self.tileset)
        
    
    def main(self):
        while self.working:
            self.deltaTime=self.clock.tick()
            self.tick()
            self.render()
            pygame.time.wait(round(1000/self.tps))
            
    def tick(self):
        self.keysPressed=[]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                self.working = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            
            elif event.type == pygame.KEYDOWN:
                self.keysPressed.append(event.key)
        if self.lightMode=="partial":
            self.lightsystem.reset()
        self.entitysystem.tick(self)
    
    def render(self):
        self.screen.fill(colors.BLACK)
        self.tileset.render(self.screen, self.lightsystem.lighted, self.lightMode)
        self.entitysystem.render(self)
        pygame.display.flip()

mainRunner=None

config_dict=None

if __name__=="__main__":
    config_dict=config.loadJSON("config.json")
    mainRunner= Runner(50, monitor.width/2, monitor.height/2)
    mainRunner.main()