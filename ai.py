import json
import os

import numpy as np
import openai
from openai import OpenAI

name = "Mattia"
greetings = [f"whats up master {name}",
             "ah? umhh, yeah?",
             "Well, hello there, Master of Puns and Jokes - how's it going today?",
             f"Ahoy there, Captain {name}! How's the ship sailing?",
             f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?" ]


class Client:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Load API key from conf.json
        try:
            # Load the API key from the conf.json file
            with open("conf.json", "r") as f:
                config = json.load(f)
                openai_api_key = config.get("OPENAI_API_KEY")
                
            if not openai_api_key:
                raise ValueError("API key not found in conf.json")
            
            # Set the environment variable for OpenAI API key
            os.environ["OPENAI_API_KEY"] = openai_api_key
            self._client = OpenAI(api_key=openai_api_key)
        except FileNotFoundError:
            raise FileNotFoundError("conf.json file not found.")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OpenAI client: {e}")
    
    def get_client(self):
        if not self._client:
            raise ValueError("Openai client not started!")
        return self._client


def get_greeding():
    return np.random.choice(greetings)
    

client = Client().get_client()