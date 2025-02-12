from random import randint # Нужно только использовать случайное число
from game import tilesystem # Соотственно для применения генерации на карту
# ПРИМЕЧАНИЕ: я не люблю зубрить алгоритмы, поэтому алгоритм генерации случайного лабиринта я взял с сайта geekforgeeks и адаптировал, сделав разбор. Также, я внёс парочку изменений, чтобы сделать более интересный лабиринт
class Node: # Одна нода в стэке
    def __init__(self, value = None, 
               next_element = None):
        self.val = value
        self.next = next_element
 

class stack: # Не буду объяснять принцип работы стека, в документации оставил ссылку на разбор
   
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
    ROWS, COLS = r, c # Сообственно ряды и стобцы
     
     
    
    maze = list(list(0 for _ in range(COLS)) 
                       for _ in range(ROWS)) # Генерация пустой карты
     
    
    seen = list(list(False for _ in range(COLS)) 
                           for _ in range(ROWS)) # Генерация пустой карты клеток, которые уже были посещены
    previous = list(list((-1, -1) 
     for _ in range(COLS)) for _ in range(ROWS))
    S = stack()
    S.insert(P0) 
    while S.not_empty():
        x, y = S.chooseRandomAndPop() # Выбираем случайную клетку
        seen[x][y] = True
        if (x + 1 < ROWS) and maze[x + 1][y] == 1 \
        and previous[x][y] != (x + 1,  y): # Защита от: координат вне карты, уже отработанных клеток и стен
            continue
        if (0 < x) and maze[x-1][y] == 1 \
        and previous[x][y] != (x-1,  y): # Защита от: координат вне карты, уже отработанных клеток и стен
            continue
        if (y + 1 < COLS) and maze[x][y + 1] == 1 \
        and previous[x][y] != (x, y + 1): # Защита от: координат вне карты, уже отработанных клеток и стен
            continue
        if (y > 0) and maze[x][y-1] == 1 \
        and previous[x][y] != (x, y-1): # Защита от: координат вне карты, уже отработанных клеток и стен
            continue
        maze[x][y] = 1 # Установка стены
        to_stack = [] # Создание списка, с последующим добавлением в него через if возможных клеток для обработки
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
         
        
        pf_flag = False # Был ли найден кандидат, являющийся финишем?
        while len(to_stack): # Итерация по всем врзможным соседям клетки, с их случайным добавлением в стек
            neighbour = to_stack.pop(randint(0, len(to_stack)-1))
            if neighbour == Pf:
                pf_flag = True
             
            
            else:
                S.insert(neighbour)
         
        if pf_flag: # Если был найден кандидат, являющийся финишем, то нужно добавить его в стек
            S.insert(Pf)
                 
    
    x0, y0 = P0 # Парсинг координат из кортежей
    xf, yf = Pf # Парсинг координат из кортежей
    maze[x0][y0] = 2 # Установка спавна
    maze[xf][yf] = 3 # Установка финиша
     
    
    return maze

def generate(tileset: tilesystem.Tileset, startColor=(0, 255, 0), endColor=(0, 255, 255)):
    startX, startY=randint(0, tileset.width-1), randint(0, tileset.height-1) # Выбор случайных координат для начала
    endX, endY=randint(0, tileset.width-1), randint(0, tileset.height-1) # Выбор случайных координат для финиша
    
    maze=random_maze_generator(tileset.width, tileset.height, (startX, startY), (endX, endY)) # Генерация простого лабиринта скриптом выше
    
    for x in range(0, tileset.width): # Перенос лабиринта на tileset
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
