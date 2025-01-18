import pygame
import game.tilesystem
from main import Runner


class Entity:
    def __init__(self, x:int=0, y:int=0, color=(255, 255, 255)):
        self.x=x
        self.y=y
        self.color=color
    
    def render(self, ctx: pygame.Surface, tileset: game.tilesystem.Tileset):
        pygame.draw.circle(ctx, self.color, (round((self.x+0.5)*tileset.tileSize+tileset.xOffset), round((self.y+0.5)*tileset.tileSize+tileset.yOffset)), round(tileset.tileSize*0.4))
    
    def tick(self, runner: Runner):
        pass

class EntitySystem:
    def __init__(self):
        self.entities=[]
    
    def tick(self, runner: Runner):
        for entity in self.entities:
            entity.tick(runner)
            
    def createPlayer(self, x: int, y: int, color=(255, 255, 255), walkSpeed=0.1):
        self.entities.append(Player(x, y, color, walkSpeed))
            
    def render(self, runner: Runner):
        for entity in self.entities:
            entity.render(runner.screen, runner.tileset)
            
class Player(Entity):
    def __init__(self, x = 0, y = 0, color=(255, 255, 255), walkSpeed=0.1):
        super().__init__(x, y, color)
        self.walkTimeOut=0
        self.walkSpeed=walkSpeed
    
    def tryMove(self, deltaCord, tileset: game.tilesystem.Tileset):
        x, y = self.x+deltaCord[0], self.y+deltaCord[1]
        if not tileset.isSolid(x, y):
            self.x=x
            self.y=y
        
    
    def tick(self, runner: Runner):
        if self.walkTimeOut<=0:
            try:
                if pygame.K_w in runner.keysPressed:
                    self.tryMove((0, -1), runner.tileset)
                    self.walkTimeOut=self.walkSpeed
                elif pygame.K_s in runner.keysPressed:
                    self.tryMove((0, 1), runner.tileset)
                    self.walkTimeOut=self.walkSpeed
                elif pygame.K_d in runner.keysPressed:
                    self.tryMove((1, 0), runner.tileset)
                    self.walkTimeOut=self.walkSpeed
                elif pygame.K_a in runner.keysPressed:
                    self.tryMove((-1, 0), runner.tileset)
                    self.walkTimeOut=self.walkSpeed
            except ValueError:
                pass
        else:
            self.walkTimeOut-=1.0/runner.tps
        runner.lightsystem.runLightOnPoint(self.x, self.y)
        if runner.tileset.isEnd(self.x, self.y):
            runner.working=False
            print("You win!")