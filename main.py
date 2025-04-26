import streamlit as st
from PIL import Image



# Page details
im = Image.open("favicon.png")

st.set_page_config(
    page_title="InTeliPrompt",
    layout="wide",
    page_icon=im
)


# navigation sidebar
pages = {
    "KaraokeFlow":[
        st.Page("spotify.py", title="Link your Spotify account"),
        st.Page("profile.py", title="Profile details"),
        st.Page("manual_add.py", title="Manual song input"),
    ]
}

pg = st.navigation(pages)

pg.run()

