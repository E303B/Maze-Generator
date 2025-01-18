import pygame # Основная библиотека, на которой строится вся игра(окно)
import screeninfo # Получиьт размеры экрана
import defines.colors as colors # Цвета
import game.tilesystem # Клетки
import game.generator # Генератор лабиринта
import game.entitysystem # Система для игрока. В будущем может быть использована для создания врагов, монеток и т.п
import game.lightsystem # Система света
import configloader as config # Чтение конфига
import random # Рандомайзер

monitor=screeninfo.get_monitors()[0] # Получаем главный монитор

class Runner: # Основной рабочий класс
    def __init__(self, tps:int,  width: int=480, height:int=360):
        # Базовое присвоение значений переменной
        self.width=width
        self.height=height
        self.tps=tps
        pygame.init() # Запуск pygame
        self.screen=pygame.display.set_mode((width, height), pygame.RESIZABLE) # Установка размеров окна pygame
        pygame.display.set_caption("Maze")
        
        self.clock = pygame.time.Clock() # Ограничитель fps/tps
        self.clock.tick(tps)
        self.working=True # Контроль отключения окна
        self.deltaTime=0.0
        self.keysPressed=[]
        # Много всяких парсеров
        temp=colors.getColor(config_dict.get("tileColor", "red"))
        if temp==None:
            tileColor=colors.parseColor(config_dict.get("tileColor"))
        else:
            tileColor=temp
        temp=colors.getColor(config_dict.get("wallColor", "dark_gray"))
        if temp==None:
            wallColor=colors.parseColor(config_dict.get("wallColor"))
        else:
            wallColor=temp
        temp=colors.getColor(config_dict.get("hiddenColor", "black"))
        if temp==None:
            hiddenColor=colors.parseColor(config_dict.get("hiddenColor"))
        else:
            hiddenColor=temp
        self.tileset=game.tilesystem.Tileset(config_dict.get("width", 10), config_dict.get("height", 10), tileColor, wallColor, hiddenColor) # Наконец-то создаём систему управления клетками
        
        basegen=random.randint(-2147483648, 2147483647) # Просто из Java Integer.MIN_VALUE и MAX_VALUE (-(2^32) и (2^32)-1 соответственно)
        generator=config_dict.get("generator", None)
        if isinstance(generator, dict):
            temp=generator.get("randomSeed", basegen) 
            
            if isinstance(temp, str): # Если наш сид является строкой, то мы проверяем является ли он пустой строкой, тогда мы задаем ему случайное значение, иначе пытаемся парсить, при провале тоже придавая ему случайное значение
                if len(temp)==0:
                    temp=basegen
                else: 
                    try:
                        temp=int(temp)
                    except ValueError:
                        temp=basegen
            random.seed(temp)
        
        else:
            random.seed(basegen)
            
        # Парсинг цветов для генератора
        temp=colors.getColor(config_dict.get("startColor", "green"))
        if temp==None:
            startColor=colors.parseColor(config_dict.get("startColor"))
        else:
            startColor=temp
        temp=colors.getColor(config_dict.get("endColor", "yellow"))
        if temp==None:
            endColor=colors.parseColor(config_dict.get("endColor"))
        else:
            endColor=temp
        game.generator.generate(self.tileset, startColor, endColor) # Сообственно сам генератор
        # Парсинг цвета игрока
        temp=colors.getColor(config_dict.get("playerColor", "cyan"))
        if temp==None:
            playerColor=colors.parseColor(config_dict.get("playerColor"))
        else:
            playerColor=temp
        self.entitysystem=game.entitysystem.EntitySystem() # Инициализация системы сущностей и игрока соответственно 
        temp=config_dict.get("playerSpeed", 1) 
        for c in self.tileset.getSpawns():
            x, y= c
            self.entitysystem.createPlayer(x, y, playerColor, (1.0/temp))
            
        self.lightMode=config_dict.get("lightMode", "off") # Парсинг режима света
        self.lightsystem=game.lightsystem.LightSystem(self.tileset) # Инициализация режима света
        
    # Основной цикл, который запускает главный код и рендерит всё окно
    def main(self):
        while self.working:
            self.deltaTime=self.clock.tick()
            self.tick()
            self.render()
            pygame.time.wait(round(1000/self.tps))
    
    # Один тик в цикле работы
    def tick(self):
        self.keysPressed=[]
        for event in pygame.event.get(): # Обрабатываем все события, такие как выключение, изменение размера окна, нажатие клавиш
            if event.type == pygame.QUIT:  
                self.working = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            
            elif event.type == pygame.KEYDOWN:
                self.keysPressed.append(event.key)
        if self.lightMode=="partial": # Если lightMode частичный(partial), то на каждом тике обновляются отображаемые клетки
            self.lightsystem.reset()
        self.entitysystem.tick(self) # Работа всех сущностей
    
    def render(self): # Весь рендер
        self.screen.fill(colors.BLACK) # Чёрный задний фон
        self.tileset.render(self.screen, self.lightsystem.lighted, self.lightMode) # Отрисовка клеток
        self.entitysystem.render(self) # Отрисовка сущностей ПРИМЕЧАНИЕ: Чтобы игрок был виден, нужно отрисовывать сущности строго ПОСЛЕ клеток
        pygame.display.flip() # Нанесение отрисованного на окно

mainRunner=None # Хранение основного раннера игры

config_dict=None # Словарь для конфига

if __name__=="__main__": # Данный код будет запущен, строго при запуске самого файла. Если будет запускаться любой другой файл, который будет импортировать данный, код под if запускаться не будет
    config_dict=config.loadJSON("config.json") # Чтение конфига
    mainRunner= Runner(50, monitor.width/2, monitor.height/2) # Создание самого окна и раннера
    mainRunner.main() # Запуск раннера