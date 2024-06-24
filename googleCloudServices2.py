import queue
import sys
import sounddevice as sd
from google.cloud import speech_v1 as speech
from google.oauth2 import service_account

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE)  # 100ms

# Initialize the queue to hold audio data
q = queue.Queue()
speechToTextClient = None
speechToTextConfig = None
speechToTextStreamingConfig = None
responses = None

def initGoogleCloudServices():
    global speechToTextClient
    global speechToTextConfig
    global speechToTextStreamingConfig
    global responses
    
    # Initialize Google Cloud Speech-to-Text client
    credentials = service_account.Credentials.from_service_account_file('google_credential.json')
    speechToTextClient = speech.SpeechClient(credentials=credentials)

    speechToTextConfig = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
        enable_automatic_punctuation=True
    )

    speechToTextStreamingConfig = speech.StreamingRecognitionConfig(config=speechToTextConfig, interim_results=False)

    def generator():
        while True:
            data = q.get()
            if data is None:
                break
            yield speech.StreamingRecognizeRequest(audio_content=data)

    # Start audio input stream
    with sd.RawInputStream(samplerate=RATE, blocksize=CHUNK, dtype='int16', channels=1, callback=callback):
        print("Listening (press Ctrl+C to stop)...")
        requests = generator()
        responses = speechToTextClient.streaming_recognize(config=speechToTextStreamingConfig, requests=requests)

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def getTranscript():
    global responses
    try:
        for response in responses:
            for result in response.results:
                if result.is_final:
                    return result.alternatives[0].transcript
    except KeyboardInterrupt:
        print("\nExiting...")
        q.put(None)
        raise