import firebase_admin
import streamlit as st
from firebase_admin import credentials
from firebase_admin import db


@st.cache_data
def initialize_firebase_app():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "#place your database URL here"
    })


# Json Structure that we are going to send to the FireBase Real Time Database

# data = {
#     'Sadness/Heartbreak':
#         [
#             {
#                 'song_name': "Some one like  you",
#                 'singer': "adele",
#             },
#             {
#                 'song_name': "stay",
#                 'singer': "Rihanna"
#             }
#         ],
#     'Love/Romance':
#         [
#             {
#                 'song_name': "Thinking out loud",
#                 'artist': "Ed sheeran"
#             },
#             {
#                 'song_name': "Love story",
#                 'artist': "taylor swift"
#             }
#         ]
#
# }


def add_data(emotion, songs, artists):
    new_entry_ref = db.reference('Emotions').child(emotion).child('songs')
    song_list = []
    for song, artist in zip(songs, artists):
        data = {
            'song_name': song,
            'artist': artist
        }

        song_list.append(data)

    new_entry_ref.set(song_list)
