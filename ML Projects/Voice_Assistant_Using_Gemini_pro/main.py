import streamlit as st
from datetime import date
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr

# Load environment variables
load_dotenv()
# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

today = str(date.today())

engine = pyttsx3.init()
engine.setProperty('rate', 190)  # speaking rate
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female

model = genai.GenerativeModel('gemini-pro')

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

talk = []

def append2log(text):
    global today
    fname = 'chatlog-' + today + '.txt'
    with open(fname, 'a') as f:
        f.write(text + '\n')

def process_request(request):
    global talk, today, model
    append2log(f"You: {request}\n")
    talk.append({'role': 'user', 'parts': [request]})

    response = model.generate_content(talk, stream=True)
    response_text = ""
    for chunk in response:
        response_text += chunk.text + ' '
        speak_text(chunk.text.replace("*", ""))
    response_text = response_text.strip()

    talk.append({'role': 'model', 'parts': [response_text]})
    append2log(f'AI: {response_text}\n')

    return response_text

st.title('Voice Assistant with Google Generative AI')
st.write('Use your voice to interact with the AI.')

if st.button('Start Listening'):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    
    try:
        request = recognizer.recognize_google(audio)
        st.write(f"You said: {request}")
        if 'jack' in request.lower():
            request = request.lower().split("jack")[1].strip()
            response = process_request(request)
            st.write(f"AI: {response}")
        else:
            st.write("Please address the request to 'Jack'.")
    except sr.UnknownValueError:
        st.write("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
