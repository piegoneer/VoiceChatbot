import queue
import sys
import sounddevice as sd
from google.cloud import speech_v1 as speech
from google.oauth2 import service_account

import io
from google.cloud import texttospeech
from pydub import AudioSegment
import pyaudio

import utils

# Audio recording parameters
RATE = 16000
# CHUNK = int(RATE / 10)  # 100ms
CHUNK = int(RATE)  # 100ms

# Initialize the queue to hold audio data
q = queue.Queue()
speechToTextClient = None
speechToTextConfig = None
speechToTextStreamingConfig = None
textToSpeechClient = None
voice = None
audio_config = None

def initGoogleCloudServices():
    global speechToTextClient
    global speechToTextConfig
    global speechToTextStreamingConfig
    global textToSpeechClient
    global voice
    global audio_config

    utils.setupOpenAIAPI()
    
    credentials = service_account.Credentials.from_service_account_file('google_credential.json')
    speechToTextClient = speech.SpeechClient(credentials=credentials)

    speechToTextConfig = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
        enable_automatic_punctuation=True
    )

    speechToTextStreamingConfig = speech.StreamingRecognitionConfig(config=speechToTextConfig, interim_results=False)

    # Text To Speech
    textToSpeechClient = texttospeech.TextToSpeechClient(credentials=credentials)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

# Define the callback function to process audio data
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def speechToText():
    def generator():
        while True:
            data = q.get()
            if data is None:
                break
            yield speech.StreamingRecognizeRequest(audio_content=data)

    with sd.RawInputStream(samplerate=RATE, blocksize=CHUNK, dtype='int16',
                           channels=1, callback=callback):
        print("Listening (press Ctrl+C to stop)...")
        requests = generator()
        responses = speechToTextClient.streaming_recognize(config=speechToTextStreamingConfig, requests=requests)

        try:
            for response in responses:
                for result in response.results:
                    if result.is_final:
                        print(f"Transcript: {result.alternatives[0].transcript}")
                        salesBotReply = utils.salesBot(result.alternatives[0].transcript)
                        print(f"Sales Bot:{salesBotReply}")
                        text_to_speech(salesBotReply)
                        if result.alternatives[0].transcript.strip()[:13].lower() == "see you later":
                            print("\nExiting...")
                            q.put(None)
                    else:
                        print(f"Intermediate transcript: {result.alternatives[0].transcript}", end='\r')
        except KeyboardInterrupt:
            print("\nExiting...")
            q.put(None)



def play_audio(audio_segment):
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a .Stream with the appropriate settings
    stream = p.open(format=p.get_format_from_width(audio_segment.sample_width),
                    channels=audio_segment.channels,
                    rate=audio_segment.frame_rate,
                    output=True)

    # Write the raw audio data to the stream
    stream.write(audio_segment.raw_data)

    # Close the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

def text_to_speech(text):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Perform the text-to-speech request
    response = textToSpeechClient.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Use pydub to load the audio content
    audio = AudioSegment.from_file(io.BytesIO(response.audio_content), format="mp3")

    # Play the audio
    play_audio(audio)