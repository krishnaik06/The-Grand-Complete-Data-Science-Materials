import streamlit as st
import requests
import sounddevice as sd
import wavio
from langchain import OpenAI
import os
os.environ["OPENAI_API_KEY"]="API_KEY" 
from openai import OpenAI
client = OpenAI()


# Record audio
def record_audio(filename, duration, fs):
    print("Recording audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    print("Audio recorded and saved as", filename)


st.write("Speak here")
if st.button(label="Click here to speak"):
    audio_filename = "input.wav"
    duration = 5  # Duration of the recording in seconds
    fs = 44100  # Sample rate
    record_audio(audio_filename, duration, fs) ## user input recorded and stores

    ##converting to text using whisper
    audio_file= open("virat.wav", "rb")
    transcript = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file)
    a=transcript.text
    st.write(a)

    ##generating the images for the text using the dalle model
    response = client.images.generate(
    model="dall-e-2",
    prompt=a,
    size="1024x1024",
    quality="standard",
    n=1)
    image_url = response.data[0].url
    image_response = requests.get(image_url)

    ##getting the image from the url produced by the model
    image_path = "generated_image.jpg"
    with open(image_path, "wb") as f:
        f.write(image_response.content)
    print("Image generated and saved as", image_path)

    ##display the output
    st.image("generated_image.jpg")
