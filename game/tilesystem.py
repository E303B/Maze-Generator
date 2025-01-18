import pygame # Отрисовка
from random import randint # Забыл убрать
from defines import colors # Забыл убрать

class Tile: # Просто класс для хранения клеток: цвета, явлется ли спановм/финишем/твёрдым
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
        self.height=max(height, 10) # Защита от слишком маленьких карт
        self.wallColor=wallColor # Цвет стен
        self.tileColor=tileColor # Цвет пустых клеток
        self.hiddenColor=hiddenColor # Цвет неподсвеченных клеток
        self.tiles=list(list(Tile(tileColor) for _ in range(0, self.height)) 
                       for _ in range(0, self.width)) # Короткая генерация всех нужных клеток
        
        w, h= (480, 360)  # Начальная установка размеров клеток
        self.tileSize=min(round(w/self.width), round(h/self.height))
        self.xOffset=(w-self.tileSize*self.width)/2
        self.yOffset=(h-self.tileSize*self.height)/2
        
                
    def render(self, ctx: pygame.Surface, lighted, lightMode:str="off"):
        w, h=ctx.get_size() # Получение размера окна
        self.tileSize=min(round(w/self.width), round(h/self.height)) # Высчитывает размеры клетки: берёт минимальное из округлений (ширина окна/количество столбцов) и (высота окна/количество рядов)
        self.xOffset=(w-self.tileSize*self.width)/2 # Расчёт смещения по x: если минимальным оказалось округление (ширина окна/количество столбцов), то ничего не будет, иначе будет смещение, зависящая от разности ширины окна и (round(ширина окна/количество столбцов)* количество столбцов)
        self.yOffset=(h-self.tileSize*self.height)/2 # Расчёт смещения по y: если минимальным оказалось округление (высота окна/количество рядов), то ничего не будет, иначе будет смещение, зависящая от разности высоты окна и (round(высота окна/количество рядов)* количество рядов)
        for x in range(0, self.width): # Рендер всех клеток через два цикла
            for y in range(0, self.height):
                self.tiles[x][y].render(self.xOffset+self.tileSize/2+x*self.tileSize, self.yOffset+self.tileSize/2+y*self.tileSize, self.tileSize, ctx, lighted[x][y] or lightMode=="off", self.hiddenColor)
                
    def getSpawns(self): # Получение кортежей всех возможных спавнов, путем итерации по всем клеткам через два цикла
        result=[]
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.tiles[x][y].isSpawn:
                    result.append((x, y))
        return result
    
    def isSolid(self, x: int, y:int)->bool: # Проверка на то, является ли клетка непроходимой(стеной)
        if x>=0 and y>=0 and x<=self.width-1 and y<=self.height-1:
            return self.tiles[x][y].isSolid
        return True
    
    def isEnd(self, x:int, y:int)->bool: # Проверка на то, является ли клетка финишем
        if x>=0 and y>=0 and x<=self.width-1 and y<=self.height-1:
            return self.tiles[x][y].isEnd
        return False