import time

import numpy as np
import openai
import speech_recognition as sr

from ai import client, get_greeding
from audio import say

recognizer = sr.Recognizer()

def get_chat_response(user_input):
    
    return client.chat.completions.create(
        model="gpt-4", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        stream=True
        )


def listen_and_respond(source):
    print("Listening ...")
    
    while True:
        audio = recognizer.listen(source, timeout=2000)
        try:
            text = recognizer.recognize_google(audio)
            print(f"User: {text}")
            if not text:
                continue
            if "stop" in text.lower():
                stop_response = "Ok, I'll go to sleep. Wake me up if you need something!"
                print('ORION: ', stop_response)
                say(stop_response)
                break
            # Send input to OpenAI API
            completion = get_chat_response(text)
            generated_words = [chunk.choices[0].delta.content for chunk in completion if chunk.choices[0].delta.content != None]
            response_text = ''.join(generated_words)
            print('ORION: ', response_text)
            say(response_text)
            
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            say("HUM, I don't know how to respond, I think I'm having an error")
            listen_for_wake_word(source)
            break

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
                
                listen_and_respond(source)
                
                break
            else:
                print('Waiting')
        except sr.UnknownValueError:
            pass


def main():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        listen_for_wake_word(source)
        

        
if __name__ == "__main__":
    main()
        
        
