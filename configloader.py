import json # Встроенная библиотека для чтения json

def loadJSON(filePath: str)-> dict:
    with open(filePath) as file: # Открываем файл из пути и читаем его
        data = file.read()
    
    parsed_data=json.loads(data) # Парсим файл 
    return parsed_data # И возвращаем запарсенные данные
    
