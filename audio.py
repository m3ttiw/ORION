import io
import json
from pathlib import Path

import openai
import pyaudio

from ai import client


# Stream audio to speakers
def say_old(text):
    print('[DEBUG] I\'m trying to speech...', text)
    
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=24_000,
                    output=True)
    
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="onyx",
        input="     " + text + "      ",
        response_format="pcm"
    ) as response:
        for chunk in response.iter_bytes(1024):
            stream.write(chunk)

def generate_silence(duration_ms, sample_rate=24000, sample_width=2, channels=1):
    num_samples = int(sample_rate * duration_ms / 1000)
    return b'\x00' * num_samples * sample_width * channels

    
def say(text):
    #print('[DEBUG] Preparing to speak:', text)

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=24000,
                    output=True)

    # Generate 500 milliseconds of silence before and after the speech
    silence_duration_ms = 500
    silence = generate_silence(silence_duration_ms)

    try:
        # Play silence before speech
        stream.write(silence)

        # Stream the TTS response
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="onyx",
            input=text,
            response_format="pcm"
        ) as response:
            for chunk in response.iter_bytes(1024):
                stream.write(chunk)

        # Play silence after speech
        stream.write(silence)
    finally:
        # Close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()