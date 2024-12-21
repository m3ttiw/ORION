import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS

import openai
import pyaudio

# Load the API key from the conf.json file
with open("conf.json", "r") as f:
    config = json.load(f)
    openai.api_key = config.get("OPENAI_API_KEY")

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

# Generate speech from text
response = openai.Audio.create(
    model="text-to-speech",
    input="Today is a wonderful day to build something people love!",
    voice="onyx",
    response_format="wav",
    stream=True
)

# Stream audio to speakers
for chunk in response:
    play_audio(chunk)


# Load api key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
model = 'gpt-4'
recognizer = sr.Recognizer()

engine = pyttsx3.init("dummy")
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
name = "Mattia"
greetings = [f"whats up master {name}",
             "yeah?",
             "Well, hello there, Master of Puns and Jokes - how's it going today?",
             f"Ahoy there, Captain {name}! How's the ship sailing?",
             f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?" ]

def listen_for_wake_word(source):
    print("Listening for 'Hey'...")

    while True:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            if "hey" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                #listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass


def main():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        listen_for_wake_word(source)
        
        
        
        
if __name__ == "__main__":
    main()
        
        
