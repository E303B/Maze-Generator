BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 224, 255)
DARK_GRAY = (42, 42, 42)

# боже...
def getColor(string: str):
    l=string.lower()
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
    
def parseColor(string: str): # r, g, b
    s=string.replace(" ", "")
    splitted=s.split(",")
    if len(splitted)!=3:
        return None
    return (int(splitted[0]), int(splitted[1]), int(splitted[2]))