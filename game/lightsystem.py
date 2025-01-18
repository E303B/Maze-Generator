import game.tilesystem # Использует систему клеток по очевидным причинам

class LightSystem: # Сообственно, вся система управления светом
    def reset(self): # Обнуляет все подсвеченные клетки через два цикла, один из которых вложен в другой
        for x in range(0, len(self.lighted)):
            for y in range(0, len(self.lighted[x])):
                self.lighted[x][y]=False
    
    def __init__(self, tileset: game.tilesystem.Tileset):
        self.lighted=[] # Список для списков для хранения значения подсвеченности
        self.reftileset=tileset # Сохранение tileset-а с которым в последствии нужно работать
        for x in range(0, tileset.width): # Создаёт все подсвеченные клетки через два цикла, один из которых вложен в другой
            self.lighted.append([])
            for y in range(0, tileset.height):
                self.lighted[x].append(False)
                
    def isLegitCoords(self, x:int, y:int)->bool: # Просто проверка на правильность координат
        return x>=0 and y>=0 and x<=self.reftileset.width-1 and y<=self.reftileset.height-1
    
    def runLightWithDelta(self, x:int, y:int, delta): # Под функция для запуска луча с определённой дельтой координат каждый микротик
        cx=x
        cy=y
        while self.isLegitCoords(cx, cy) and not self.reftileset.isSolid(cx,cy):
            self.lighted[cx][cy]=True
            cx+= delta[0]
            cy+=delta[1]
        
        if self.isLegitCoords(cx,cy):self.lighted[cx][cy]=True # Чтобы стены, на которых прекратился луч света, тоже подсвечивались, если это, конечно, стена, а не клетка за картой
    
    def runLightOnPoint(self, x:int, y:int): # Четыре луча во всех направлениях
        self.runLightWithDelta(x, y, (-1, 0))
        self.runLightWithDelta(x, y, (1, 0))
        self.runLightWithDelta(x, y, (0, 1))
        self.runLightWithDelta(x, y, (0, -1))