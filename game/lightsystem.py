import game.tilesystem

class LightSystem:
    def reset(self):
        for x in range(0, len(self.lighted)):
            for y in range(0, len(self.lighted[x])):
                self.lighted[x][y]=False
    
    def __init__(self, tileset: game.tilesystem.Tileset):
        self.lighted=[]
        self.reftileset=tileset
        for x in range(0, tileset.width):
            self.lighted.append([])
            for y in range(0, tileset.height):
                self.lighted[x].append(False)
                
    def isLegitCoords(self, x:int, y:int)->bool:
        return x>=0 and y>=0 and x<=self.reftileset.width-1 and y<=self.reftileset.height-1
    
    def runLightWithDelta(self, x:int, y:int, delta):
        cx=x
        cy=y
        while self.isLegitCoords(cx, cy) and not self.reftileset.isSolid(cx,cy):
            self.lighted[cx][cy]=True
            cx+= delta[0]
            cy+=delta[1]
        
        if self.isLegitCoords(cx,cy):self.lighted[cx][cy]=True
    
    def runLightOnPoint(self, x:int, y:int):
        self.runLightWithDelta(x, y, (-1, 0))
        self.runLightWithDelta(x, y, (1, 0))
        self.runLightWithDelta(x, y, (0, 1))
        self.runLightWithDelta(x, y, (0, -1))