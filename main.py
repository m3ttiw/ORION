import json

import numpy as np
import openai
import speech_recognition as sr

from audio import create_openai_response_audio, play_audio, say

# Load the API key from the conf.json file
with open("conf.json", "r") as f:
    config = json.load(f)
    openai.api_key = config.get("OPENAI_API_KEY")

model = 'gpt-4'
recognizer = sr.Recognizer()

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
            print(text)
            if "hey" in text.lower():
                print("Wake word detected.")
                say(create_openai_response_audio(np.random.choice(greetings)))
                # engine.say(np.random.choice(greetings))
                # engine.runAndWait()
                # listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass


def main():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        listen_for_wake_word(source)
        
        
        
        
if __name__ == "__main__":
    main()
        
        
