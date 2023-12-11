from pathlib import Path
from openai import OpenAI
import os 

from dotenv import load_dotenv
load_dotenv()

def text_to_speech(text, max_len=400):
    text = text[:max_len]
    title = "_".join(text.split(" ")[:5])
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    speech_file_path = Path(__file__).parent / f"audio/{title}.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    response.stream_to_file(speech_file_path)
