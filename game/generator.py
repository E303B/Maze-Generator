from random import randint
from game import tilesystem

class Node:
    def __init__(self, value = None, 
               next_element = None):
        self.val = value
        self.next = next_element
 

class stack:
   
    # Constructor
    def __init__(self):
        self.head = None
        self.length = 0
 
    
    def insert(self, data):
        self.head = Node(data, self.head)
        self.length += 1
        
    def choose(self, number:int):
        if number>self.length-1:
            return None
        current=self.head
        for i in range(number):
            current=current.next
        return current
    
    def chooseRandom(self):
        if self.length==0:
            return None
        i=randint(0, self.length-1)
        return self.choose(i).val
    
    def chooseRandomAndPop(self):
        if self.length==0:
            return None
        i=randint(0, self.length-1)
        choosen=self.choose(i)
        if i>0 and i<self.length-1:
            self.choose(i-1).next=self.choose(i+1)
        self.length-=1
        return choosen.val
    
    def pop(self):
        if self.length == 0:
            return None
        else:
            returned = self.head.val
            self.head = self.head.next
            self.length -= 1
            return returned
 
     
    
    def not_empty(self):
        return bool(self.length)
 
    
    def top(self):
        return self.head.val
 

def random_maze_generator(r, c, P0, Pf):
    ROWS, COLS = r, c
     
     
    
    maze = list(list(0 for _ in range(COLS)) 
                       for _ in range(ROWS))
     
    
    seen = list(list(False for _ in range(COLS)) 
                           for _ in range(ROWS))
    previous = list(list((-1, -1) 
     for _ in range(COLS)) for _ in range(ROWS))
    S = stack()
    S.insert(P0) 
    while S.not_empty():
        x, y = S.chooseRandomAndPop()
        seen[x][y] = True
        if (x + 1 < ROWS) and maze[x + 1][y] == 1 \
        and previous[x][y] != (x + 1,  y):
            continue
        if (0 < x) and maze[x-1][y] == 1 \
        and previous[x][y] != (x-1,  y):
            continue
        if (y + 1 < COLS) and maze[x][y + 1] == 1 \
        and previous[x][y] != (x, y + 1):
            continue
        if (y > 0) and maze[x][y-1] == 1 \
        and previous[x][y] != (x, y-1):
            continue
        maze[x][y] = 1
        to_stack = []
        if (x + 1 < ROWS) and seen[x + 1][y] == False:
            seen[x + 1][y] = True
            to_stack.append((x + 1,  y))
            previous[x + 1][y] = (x, y)
        if (0 < x) and seen[x-1][y] == False:
            seen[x-1][y] = True
            to_stack.append((x-1,  y))
            previous[x-1][y] = (x, y)
        if (y + 1 < COLS) and seen[x][y + 1] == False:
            seen[x][y + 1] = True
            to_stack.append((x, y + 1))
            previous[x][y + 1] = (x, y)
         
        if (y > 0) and seen[x][y-1] == False:
            seen[x][y-1] = True
            to_stack.append((x, y-1))
            previous[x][y-1] = (x, y)
         
        
        pf_flag = False
        while len(to_stack):
            neighbour = to_stack.pop(randint(0, len(to_stack)-1))
            if neighbour == Pf:
                pf_flag = True
             
            
            else:
                S.insert(neighbour)
         
        if pf_flag:
            S.insert(Pf)
                 
    
    x0, y0 = P0
    xf, yf = Pf
    maze[x0][y0] = 2
    maze[xf][yf] = 3
     
    
    return maze

def generate(tileset: tilesystem.Tileset, startColor=(0, 255, 0), endColor=(0, 255, 255)):
    startX, startY=randint(0, tileset.width-1), randint(0, tileset.height-1)
    endX, endY=randint(0, tileset.width-1), randint(0, tileset.height-1)
    
    maze=random_maze_generator(tileset.width, tileset.height, (startX, startY), (endX, endY))
    
    for x in range(0, tileset.width):
        for y in range(0, tileset.height):
            tile=maze[x][y]
            if tile==0:
                tileset.tiles[x][y]=tilesystem.Tile(tileset.wallColor, isSolid=True)
            if tile==1:
                tileset.tiles[x][y]=tilesystem.Tile(tileset.tileColor)
            elif tile==2:
                tileset.tiles[x][y]=tilesystem.Tile(startColor, isSpawn=True)
            elif tile==3:
                tileset.tiles[x][y]=tilesystem.Tile(endColor, isEnd=True)