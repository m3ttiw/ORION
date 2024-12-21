import json

import numpy as np
import openai
import speech_recognition as sr

from ai import Client, get_greeding
from audio import say

model = 'gpt-4'
recognizer = sr.Recognizer()


def listen_for_wake_word(source):
    print("Listening for 'Orion'...")

    while True:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("User: ", text)
            if "orion" in text.lower():
                print("-----")
                response = get_greeding()
                print('ORION: ', response)
                say(response)
                
                # listen_and_respond(source)
                
                break
            else:
                print('Waiting')
        except sr.UnknownValueError:
            pass


def main():

    client = Client().get_client()
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        listen_for_wake_word(source)
        
        
        
        
if __name__ == "__main__":
    main()
        
        
