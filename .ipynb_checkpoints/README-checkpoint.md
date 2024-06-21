# VoiceChatbot

This project aims to demostrate the capabilities of ATT (Audio To Text), use of LLM, Prompt Engineering and RAG to analyze the speaker's intention and output a text that meets the speaker's need and converts this text to audio via TTA (Text to Audio)

Initial Chosen Technologies (Subject to change)
- Python client running on Mac and Ubuntu
- Open AI GPT4o and GPT-3.5 Turbo for the LLM
- tts-1 model from OpenAI (TTA)
- Whisper from OpenAI (ATT)
- RAG to be decided

In order to demostrate these capabilities a resturant context will be used. A customer is talking to an AI representive in order to make an order according to the imaginary resturant operating criteria such as menus, prices, availabilitiy, operating time, current time, etc

This project will be completed in different stages

# Stage 1
- Simple Python client that converts user's speach to text, and then that same text to speach demostrating the ATT and TTA capabilities. This will be a simple echo of the user's audio
- Latency testing and improving to determine realtime responsive in a real situation
- Method to determine when speaker has finshed talking and how to handle user's interuptions

# Stage 2
- Develop fake restaurant material with generate AI for use in RAG and LLM
- Choose RAG method
- Create LLM and RAG logic to handle transform user's text to AI representive's output text
- Integrate this to the ATT and TTA pipeline
- Latency and Price reduction to determine if this is a realistic project for in the wild