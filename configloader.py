import json

def loadJSON(filePath: str)-> dict:
    with open(filePath) as file:
        data = file.read()
    
    parsed_data=json.loads(data)
    return parsed_data
    
