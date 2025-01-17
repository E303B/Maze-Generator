from defines import colors
import pygame

class Tile:
    def __init__(self, color, isSpawn: bool=False, isEnd:bool=False):
        self.color=color
        self.isSpawn=isSpawn
        self.isEnd=isEnd
    
    def render(self, x:int, y:int, size: int, ctx: pygame.Surface):
        pygame.draw.rect(ctx, self.color, (x-size/2, y-size/2, size, size))

class Tileset:
    def __init__(self, width:int=10, height:int=10, tileColor=(255, 0, 0), wallColor=(0, 0, 0)):
        self.width=width
        self.height=height
        self.tiles=[]
        self.wallColor=wallColor
        for x in range(0, width):
            self.tiles.append([])
            for y in range(0, height):
                self.tiles[x].append(Tile(tileColor))

        self.horizontalWalls=[]
        for x in range(0, width):
            self.horizontalWalls.append([])
            for y in range(0, height+1):
                self.horizontalWalls[x].append(True)
        self.verticalWalls=[]
        for x in range(0, width+1):
            self.verticalWalls.append([])
            for y in range(0, height):
                self.verticalWalls[x].append(True)
                
    def render(self, ctx: pygame.Surface):
        w, h=ctx.get_size()
        tileSize=min(round(w/self.width), round(h/self.height))
        xOffset=(w-tileSize*self.width)/2
        yOffset=(h-tileSize*self.height)/2
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.tiles[x][y].render(xOffset+tileSize/2+x*tileSize, yOffset+tileSize/2+y*tileSize, tileSize, ctx)
        
        for x in range(0, self.width):
            for y in range(0, self.height+1):
                if self.horizontalWalls[x][y]:
                    pygame.draw.line(ctx, self.wallColor, (xOffset+x*tileSize, yOffset+y*tileSize), (xOffset+x*tileSize+tileSize, yOffset+y*tileSize), round(tileSize/10))
                    
        for x in range(0, self.width+1):
            for y in range(0, self.height):
                if self.verticalWalls[x][y]:
                    pygame.draw.line(ctx, self.wallColor, (xOffset+x*tileSize, yOffset+y*tileSize), (xOffset+x*tileSize, yOffset+y*tileSize+tileSize), round(tileSize/10))