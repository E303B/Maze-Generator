import pygame # Сообственно, для отрисовки
import game.tilesystem # Получение клеток
from main import Runner # И главный раннер

# Прототип, абстрактный класс (в Питоне их нет), всех существ
class Entity:
    def __init__(self, x:int=0, y:int=0, color=(255, 255, 255)): # Сообственно координаты x и y, а также цвет кружка
        self.x=x
        self.y=y
        self.color=color
    
    def render(self, ctx: pygame.Surface, tileset: game.tilesystem.Tileset): # Отрисовка кружка
        pygame.draw.circle(ctx, self.color, (round((self.x+0.5)*tileset.tileSize+tileset.xOffset), round((self.y+0.5)*tileset.tileSize+tileset.yOffset)), round(tileset.tileSize*0.4))
    
    def tick(self, runner: Runner): # Один тик существа
        pass

class EntitySystem:
    def __init__(self):
        self.entities=[] # Хранение все существа
    
    def tick(self, runner: Runner):
        for entity in self.entities:
            entity.tick(runner) # Запуск тика у всех существ
            
    def createPlayer(self, x: int, y: int, color=(255, 255, 255), walkSpeed=0.1):
        self.entities.append(Player(x, y, color, walkSpeed)) # Базовый скрипт
            
    def render(self, runner: Runner):
        for entity in self.entities: # Рендер всех существа
            entity.render(runner.screen, runner.tileset)
            
class Player(Entity):
    def __init__(self, x = 0, y = 0, color=(255, 255, 255), walkSpeed=0.1):
        super().__init__(x, y, color) # Запускаем родительский конструктор
        self.walkTimeOut=0 # Двигаемся мы всё таки по клеточкам, поэтому, для того чтобы не улетать на всю карту от одного нажатия кнопки, делаем скорость и таймаут движения
        self.walkSpeed=walkSpeed
    
    def tryMove(self, deltaCord, tileset: game.tilesystem.Tileset): # Небольшая функция для удобности перемещения
        x, y = self.x+deltaCord[0], self.y+deltaCord[1]
        if not tileset.isSolid(x, y):
            self.x=x
            self.y=y
        
    
    def tick(self, runner: Runner):
        if self.walkTimeOut<=0: # Если ещё 'перезарядка' движения, то двигаться нельзя, нужно сокращаться перезарядку в соотвествии с tps раннера. Иначе, двигаться можно
            try:
                # Сообственно проверка всех нужны нам клавиш, при нажатии которых мы перемещаемся. ПРИМЕЧАНИЕ: В отличии от математики, где чем больше y, тем он выше, в программировании, чаще всего, отсчёт координаты y начинается СВЕРХУ ВНИЗ, то есть чем больше y - тем ниже координата
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
            except ValueError: # Забыл убрать xD Здесь try-catch (в питоне try-except) не нужен, однако до этого я использовал другой способ обнаружения нажатия клавиш, который основывался на этом
                pass
        else:
            self.walkTimeOut-=1.0/runner.tps # 1 секунда/количество tps
        runner.lightsystem.runLightOnPoint(self.x, self.y) # Запуск света на клетке под собой
        if runner.tileset.isEnd(self.x, self.y): # Проверка, финиш ли, если да, то отключить цикл и напечатать "You win!" в консоль
            runner.working=False
            print("You win!")