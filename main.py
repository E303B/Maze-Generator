import pygame
import screeninfo
import defines.colors as colors
import game
import game.tilesystem
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
        
        temp=colors.getColor(config_dict.get("tileColor", "red"))
        if temp==None:
            tileColor=colors.parseColor(config_dict.get("tileColor"))
        else:
            tileColor=temp
        temp=colors.getColor(config_dict.get("wallColor", "black"))
        if temp==None:
            wallColor=colors.parseColor(config_dict.get("wallColor"))
        else:
            wallColor=temp
        self.tileset=game.tilesystem.Tileset(config_dict.get("width", 10), config_dict.get("height", 10), tileColor, wallColor)
        basegen=random.randint(-2147483648, 2147483647) # Просто из Java Integer.MIN_VALUE и MAX_VALUE
        temp=config_dict.get("randomSeed", basegen) 
        
        if isinstance(temp, str):
            if len(temp)==0:
                temp=0
            else: 
                try:
                    temp=int(temp)
                except ValueError:
                    temp=basegen
        self.random=random.seed(temp)
    
    def main(self):
        while self.working:
            self.deltaTime=self.clock.tick()
            self.tick()
            self.render()
            pygame.time.wait(round(1000/self.tps))
            
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                self.working = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
    
    def render(self):
        self.screen.fill(colors.BLACK)
        self.tileset.render(self.screen)
        pygame.display.flip()

mainRunner=None

config_dict=None

if __name__=="__main__":
    config_dict=config.loadJSON("config.json")
    mainRunner= Runner(50, monitor.width/2, monitor.height/2)
    mainRunner.main()