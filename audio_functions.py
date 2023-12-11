import requests
import subprocess
import io
import os
import re

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

XI_API_KEY = os.getenv("XI_API_KEY")
ariana_voice_id = os.getenv("ARIANA_VOICE_ID")

def get_filename(text): 
    # Name the file by the first 5 words in the text
    file_name = text.split(" ")
    if len(file_name) > 5:
        file_name = "_".join(file_name[:5])
    else:
        file_name = "_".join(file_name)

    file_name = re.sub('[^A-Za-z0-9]+', '_', file_name).strip('_')
    file_name += '.mp3'

    return file_name 

def get_audio(text):
    # Limit text length
    max_len = 400
    text = text[:max_len]

    options = {
        'headers': {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'xi-api-key': XI_API_KEY,
        },
        'json': {
            'text': text,
            'voice_settings': {
                'stability': 0.75,
                'similarity_boost': 0.75,
            }
        },
    }

    try:
        response = requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{ariana_voice_id}', **options)
        audio_dir = 'audio'
        file_name = get_filename(text)
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        arr = []
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                arr.append(chunk)

        buffered_data = b''.join(arr)
        with io.BytesIO(buffered_data) as f:
            with open(f"{audio_dir}/{file_name}", "wb") as audio_file:
                audio_file.write(f.read())
        
        os.system(f"afplay {audio_dir}/{file_name}")
        
        # print("Audio written to file as", file_name)

    except Exception as e:
        print(e)
        return None

    # return buffered_data



def combine_audios(input_dir="audio", output_file="combined.mp3"):
    filenames = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".mp3")]

    # Create a temporary file to store the list of filenames
    with open("file_list.txt", "w") as f:
        for filename in filenames:
            f.write(f"file '{filename}'\n")

    # Create the command line for ffmpeg using subprocess
    command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "file_list.txt", "-c", "copy", output_file]

    try:
        # Run the ffmpeg command
        subprocess.run(command, check=True)
        print(f"Combined audio files into {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while combining audio files: {e}")
    finally:
        # Delete the temporary file
        if os.path.exists("file_list.txt"):
            os.remove("file_list.txt")

# get_audio('good morning, what would you like to do today?')
# combine_audios()