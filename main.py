import speech_recognition as sr
import openai
import pyttsx3
import pygame
import threading

openai.api_key = 'YOUR_API_KEY'
recognizer = sr.Recognizer()
engine = pyttsx3.init()
pygame.mixer.init()


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""



def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()



def speak(text):
    engine.say(text)
    engine.runAndWait()



def display_output(user_input, orion_response):
    print(f"User: {user_input}")
    print(f"ORION: {orion_response}")
    
    
    
def play_humming():
    pygame.mixer.music.load("humming.mp3")
    pygame.mixer.music.play(-1)
    
    

def stop_humming():
    pygame.mixer.music.stop()
    
    

def process_with_humming(prompt):
    humming_thread = threading.Thread(target=play_humming)
    humming_thread.start()
    response = generate_response(prompt)
    stop_humming()
    return response


def main():
    while True:
        user_input = listen()
        if user_input:
            orion_response = process_with_humming(user_input)
            display_output(user_input, orion_response)
            speak(orion_response)

if __name__ == "__main__":
    main()
