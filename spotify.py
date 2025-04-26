import streamlit as st
from testing import get_token



CLIENT_ID = ""
CLIENT_SECRET = ""

with st.container(border=True):
    CLIENT_ID = st.text_input("Client ID: ")
    CLIENT_SECRET = st.text_input("Client Secret: ")

    st.text_input("Song title: ")
    st.text_input("Author / Artist(s): ")


if st.button("Find lyrics"):
    token = get_token(CLIENT_ID, CLIENT_SECRET)
    st.write(token)

import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    if st.button("Start"):
        st.write("Listening...")
        try:
            # Adjust for ambient noise and record
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            st.write("You said:", text)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")


    if st.button("Stop"):
        st.write("Stops")

