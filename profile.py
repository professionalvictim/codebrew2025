import streamlit as st
import json

data = ""

st.title("Most recently played tracks")

with open('response.json', 'r') as f:
    data = json.load(f)


track_count = data["limit"]
song_titles = [item['track']['name'] for item in data['items']]
artist_names = [artist['track']['artists'][0]['name'] for artist in data['items']]

print(artist_names)


for i in range(track_count):
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(data['items'][i]['track']['album']['images'][1]["url"])
        with col2:
            st.markdown(f"<h3 style='font-size: 2.5rem;'>{artist_names[i]}</h3>"
                        f"<h4 style='font-size: 1rem;'>{song_titles[i]}</h4>", unsafe_allow_html=True)




