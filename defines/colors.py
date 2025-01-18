# Много разных цветов. Чтобы не вводить постоянно все эти кортежи

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 224, 255)
DARK_GRAY = (42, 42, 42)

# боже...
def getColor(string: str): # Конвертирует строку с цветом, по возможности, в кортеж с цветом
    l=string.lower() # Приводим текст к нижнему реестру, а потом прогоняем через кучу if elif else
    if l=="red":
        return RED
    elif l=="black":
        return BLACK
    elif l=="white":
        return WHITE
    elif l=="green":
        return GREEN
    elif l=="blue":
        return BLUE
    elif l=="yellow":
        return YELLOW
    elif l=="cyan":
        return CYAN
    elif l=="dark_gray":
        return DARK_GRAY
    else:
        return None
    
def parseColor(string: str): # r, g, b  Парсит rgb строки формата "r,g,b"
    s=string.replace(" ", "") # Убрать все пробелы из текста
    splitted=s.split(",") # Разделить текст по запятым на список строк
    if len(splitted)!=3: # Если длина меньше или больше трёх, значит что-то не так
        return None
    return (int(splitted[0]), int(splitted[1]), int(splitted[2])) 