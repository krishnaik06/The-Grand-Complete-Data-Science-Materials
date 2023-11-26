import langchain
import os
import streamlit as st
import requests
import sounddevice as sd
import wavio
os.environ["OPENAI_API_KEY"]="ADD KEY" 
import openai
from openai import OpenAI
client=OpenAI()
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "You are a presonal assistant for {your name] and your name is luna "
                "if the user call you by any other name than luna you need to correct him by your orginal name."
                "And for every output you can also use the username  in the answer which will be nice gesture"
                "you can act more,like an human speaking more than an ai replying to the message"
                "Consider the user as your friend"
                "Speak like a friend"
                "Be more creative and funny way"
            )
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

llm = ChatOpenAI()


# Record audio
def record_audio(filename, duration, fs):
    print("Recording audio...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    print("Audio recorded and saved as", filename)


## Streamlit UI
st.set_page_config(page_title="Personal voice assistant ")

website_heading = "I am Your Personal Voice assistant"

# Display as a heading
st.markdown(f"<h1 style='text-align: center; color: #a274a3;'>{website_heading}</h1>", unsafe_allow_html=True)


st.write("Speak here")
if st.button(label="Click here to speak"):
    audio_filename = "input.wav"
    duration = 5  # Duration of the recording in seconds
    fs = 44100  # Sample rate
    record_audio(audio_filename, duration, fs) ## user input recorded and stores

    ##converting to text using whisper
  
    audio_file= open("input.wav", "rb")
    transcript = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file)
    a=transcript.text
    # st.write(a)
    print(a)
    ##model
    a=llm(chat_template.format_messages(text=a))
    a=a.content

    ##audio output

    speech_file_path ="speech.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=a)
    response.stream_to_file(speech_file_path)

    st.audio("speech.mp3")

