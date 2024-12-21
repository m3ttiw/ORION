import json

import openai
import pyaudio

from ai import client


# Function to play audio data
def play_audio(data):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=24000,
                    output=True)
    stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    

# Stream audio to speakers
def say(response):
    for chunk in response:
        play_audio(chunk)
        

def create_openai_response_audio(text):
    # Generate speech from text
    return client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input=text,
)
        
    