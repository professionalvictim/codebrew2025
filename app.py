import streamlit as st

st.set_page_config(
    page_title="TEST 1",
    layout="wide",
)

audio_value = st.audio_input("Record Something")

if audio_value:
    st.markdown("Listen to yourself")
    st.audio(audio_value)
