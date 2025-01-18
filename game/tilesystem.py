import pygame
from random import randint
from defines import colors

class Tile:
    def __init__(self, color, isSpawn: bool=False, isEnd:bool=False, isSolid:bool=False):
        self.color=color
        self.isSpawn=isSpawn
        self.isEnd=isEnd
        self.isSolid=isSolid
    
    def render(self, x:int, y:int, size: int, ctx: pygame.Surface, lighted: bool= True, hiddenColor=(0, 0, 0)):
        color=(0, 0 ,0)
        if lighted:
            color=self.color
        else:
            color=hiddenColor
        pygame.draw.rect(ctx, color, (x-size/2, y-size/2, size, size))

class Tileset:
    def __init__(self, width:int=10, height:int=10, tileColor=(255, 0, 0), wallColor=(42, 42, 42), hiddenColor=(0, 0, 0)):
        self.width=max(width, 10) # Защита от слишком маленьких карт
        self.height=max(height, 10)
        self.wallColor=wallColor
        self.tileColor=tileColor
        self.hiddenColor=hiddenColor
        self.tiles=list(list(Tile(tileColor) for _ in range(0, self.height)) 
                       for _ in range(0, self.width))
        
        w, h= (480, 360)  
        self.tileSize=min(round(w/self.width), round(h/self.height))
        self.xOffset=(w-self.tileSize*self.width)/2
        self.yOffset=(h-self.tileSize*self.height)/2
        
                
    def render(self, ctx: pygame.Surface, lighted, lightMode:str="off"):
        w, h=ctx.get_size()
        self.tileSize=min(round(w/self.width), round(h/self.height))
        self.xOffset=(w-self.tileSize*self.width)/2
        self.yOffset=(h-self.tileSize*self.height)/2
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.tiles[x][y].render(self.xOffset+self.tileSize/2+x*self.tileSize, self.yOffset+self.tileSize/2+y*self.tileSize, self.tileSize, ctx, lighted[x][y] or lightMode=="off", self.hiddenColor)
                
    def getSpawns(self):
        result=[]
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.tiles[x][y].isSpawn:
                    result.append((x, y))
        return result
    
    def isSolid(self, x: int, y:int)->bool:
        if x>=0 and y>=0 and x<=self.width-1 and y<=self.height-1:
            return self.tiles[x][y].isSolid
        return True
    
    def isEnd(self, x:int, y:int)->bool:
        if x>=0 and y>=0 and x<=self.width-1 and y<=self.height-1:
            return self.tiles[x][y].isEnd
        return False