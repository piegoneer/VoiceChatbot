import os
from pathlib import Path
import openai






configPathLocation = "config.txt"
client = None

# Create a list to store all the messages for context
messages = [
    {"role": "system", "content": "You are a helpful assistant taking orders for Burgers Direct. Annonce yourself as as a bot at the start. We only sell 5 products, Danger Burger for $10, Happy Burger for $5, Banana Burger for $2, Fruit Burger $1, Sad Burger is $14. extra protein costs $2 more per burger. This text will be converted to speech so no emoticons or unusal symbols. At the end confirm the order with the customer and tell the customer the total cost. Reply 'TALK_ENDED' once order is confimed and generate a list for the cheif. If the customer wants to speak to a human, reply with text 'HUMAN_OP_REQUEST'"},
]

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
    if client is None:
        raise ValueError("The OpenAI API client has not been initialized. Call setupOpenAIAPI(api_key) first.")
    speech_file_path = audioFileOuput
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    response.stream_to_file(speech_file_path)



def audioToText(audioFile):
    if client is None:
        raise ValueError("The OpenAI API client has not been initialized. Call setupOpenAIAPI(api_key) first.")
    
    with open(audioFile, "rb") as audio:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio
        )
    return transcription.text


def salesBot(message):
    global messages
    # Add each new message to the list
    messages.append({"role": "user", "content": message})
    
    # Request gpt-4o for chat completion
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=messages
    )

    # Print the response and add it to the messages list
    chat_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_message})

    return chat_message


# completion = utils.client.chat.completions.create(
#   model="gpt-4o",
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Hello!"}
#   ]
# )

# print(completion.choices[0].message)






