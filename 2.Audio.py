import streamlit as st


st.audio(open("audio.mp3", "rb").read(), format="audio/ogg",
         start_time=10,end_time=20,loop=False)
