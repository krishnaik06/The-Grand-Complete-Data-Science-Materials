import os
import re

import pandas as pd
import streamlit as st
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from secret_key import openapi_key

os.environ['OPENAI_API_KEY'] = openapi_key


def data_fetch(emotion, number=10):
    llm = OpenAI(temperature=0.6)

    prompt_template = PromptTemplate(
        input_variables=['emotion', 'number'],
        template="I need {number} songs along with the singer base on the song emotion {emotion}."
                 " Return me as a comma-separated list."
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain({'number': number, 'emotion': emotion})

    return response['text'].strip()


def data_preprocessing(response):
    items = response.split(",")

    songs = []
    artists = []
    for item in items:
        result = item.split("by")

        if len(result) == 2:
            song = result[0].strip().replace('"', '')
            artist = result[1].strip()
            songs.append(song)
            artists.append(artist)
        else:
            # Handle cases where the item doesn't contain "by" or the split result is not as expected
            print(f"Skipping invalid item: {item}")

    return songs, artists


def emotion_clean(emotion):
    input_string = emotion

    # Using regular expression class to matching the input
    match = re.search(r'^([^/]+)', input_string)

    if match:
        result = match.group(1)
        return result

    return emotion


# Cache the data preventing on retrieve from API
@st.cache_data
def song_listing(songs, artists):
    return pd.DataFrame({
        'songs': songs,
        'header': artists,
    })
