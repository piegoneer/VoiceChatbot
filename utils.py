import os
from pathlib import Path
import openai

configPathLocation = "config.txt"
client = None

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

def setupOpenAIAPI():
    global client
    OPENAI_API_KEY = getOPENAI_API_KEY()
    client = openai.OpenAI(api_key=OPENAI_API_KEY)


def textToAudioFile(text, audioFileOuput):
    speech_file_path = audioFileOuput
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    response.stream_to_file(speech_file_path)
    



    
