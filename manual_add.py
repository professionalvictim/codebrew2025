import streamlit as st
import re
import requests
from pathlib import Path
from lyricsgenius import Genius
import yt_dlp

# API Keys and track directory
RAPID_API_KEY = "b37af82edemsh866749ea931657ep18b9bdjsn2189d3775723"
TRACKS_DIR = Path("tracks")
TRACKS_DIR.mkdir(exist_ok=True)
genius_token = "QLFOTZuTTGQKc0pKN0aY35rqwS0ywt0qmnun4QHVHoKd7u8bq7IcXgrxIB6vPJxP"
genius = Genius(genius_token)

raw_lyrics = ""
cleaned_lyrics = ""

def extract_yt_id(url):
    # Extract the pattern from full length or shortened youtube urls
    pattern = re.compile(
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    )
    match = pattern.search(url)
    if (match):
        return match.group(1)
    else:
        return None


def fetch_mp3_info(video_id):
    url = f"https://youtube-mp36.p.rapidapi.com/dl?id={video_id}"
    headers = {
        "x-rapidapi-host": "youtube-mp36.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def download_mp3(link, title):
    response = requests.get(link, stream=True)
    filename = f"{title}.mp3".replace(" ", "_").replace("/", "_")
    filepath = TRACKS_DIR / filename  # Initialising filepath using Path library, no fstring needed

    if filepath.exists():
        st.warning(f"File {filename} already exists, not overwriting it.")
    with open(filepath, 'wb') as f:
        # Write the audio file in 1KB at a time as the download comes in streams (Memory efficiency)
        # Note that this API gives download links that support streamed downloads
        for chunk in response.iter_content(1024):
            f.write(chunk)
    return filepath


def get_youtube_link(song_name):
    ydl_opts = {
        "quiet": True,
        "default_search": "ytsearch1",  # Search for the first result
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(song_name, download=False)
        if "entries" in info:
            return info["entries"][0]["webpage_url"]
        return None


st.title("Lyrics Downloader")
song_name = st.text_input("Enter song name:")
artist = st.text_input("Enter artist name:")

# Genius API usage to get lyrics
if st.button("Get Lyrics"):
    if song_name and artist:
        song = genius.search_song(title=song_name, artist=artist)
        if song:
            if (song.artist == artist):
                lyrics = song.lyrics
                start = lyrics.find("[Verse 1]")

                st.text(cleaned_lyrics)
            else:
                st.error("No lyrics found")
        else:
            st.error("Song unavailable")
    else:
        st.error("Please enter a song name and artist together (Genius API).")

# Nicey's code goes here

st.button("Start Karaoke-ing")
st.button("Stop")