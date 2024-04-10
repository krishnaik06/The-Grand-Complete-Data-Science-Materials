import base64

import streamlit as st

import database
import preprocess

st.set_page_config(
    page_title="Song finder base on emotion",
    # layout="wide",
    # initial_sidebar_state="collapsed",
)


@st.cache_data
def get_image_as_base64(file):
    with open(file, "rb") as t:
        data = t.read()
    return base64.b64encode(data).decode()


img = get_image_as_base64("Resources/song.jpg")  # path to your desired background image
side_bar_image = get_image_as_base64("Resources/wall.jpg")  # path to your desired sidebar image

# Some CSS styling for adding background image and sidebar

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"]{{
background-image: url("data:image/jpg;base64,{img}");
background-size: cover;
background-attachment: local;
}}
div.e1fqkh3o3{{
background-image: url("data:image/jpg;base64,{side_bar_image}");
background-size: cover;
background-attachment: local;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("Song finder base on emotion")

# Use any emotions that you want ex: I use 8 emotions

emotion = st.sidebar.selectbox("Pick an Emotion", ("Love/Romance", "Happiness/Joy", "Sadness/Heartbreak",
                                                   "Anger/Defiance", "Hope/Inspiration", "Empowerment/Confident",
                                                   "Peace/Calm", "Excitement/Adventurous"))

if emotion:
    emotion = preprocess.emotion_clean(emotion)
    response = preprocess.data_fetch(emotion, 10) # pass arguments base on how many data do you want to retrieve

    songs, artists = preprocess.data_preprocessing(response)

    # st.checkbox("Use container width", value=False, key="use_container_width")

    # Using some preprocessing on data
    df = preprocess.song_listing(songs, artists)

    st.write(f'Song list base on emotion : {emotion}')

    st.dataframe(df, width=600)

    database.initialize_firebase_app()

    database.add_data(emotion, songs, artists)
