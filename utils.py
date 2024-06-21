import os

configPathLocation = "config.txt"

def readConfig(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split('=')
            config[name] = value
    return config

def getOPENAI_API_KEY():
    config = readConfig(configPathLocation)
    OPENAI_API_KEY = config.get('OPENAI_API_KEY')
    return OPENAI_API_KEY
    
