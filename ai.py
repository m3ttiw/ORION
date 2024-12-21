import json
import os

from openai import OpenAI

client = OpenAI()

# Load the API key from the conf.json file
with open("conf.json", "r") as f:
    config = json.load(f)
    os.environ["OPENAI_API_KEY"] = config.get("OPENAI_API_KEY")
    client.api_key = os.getenv("OPENAI_API_KEY")