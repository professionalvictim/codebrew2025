import streamlit as st
import requests
from urllib.parse import urlencode
import speech_recognition as sr



st.markdown("<strong><span style='font-size: 4rem;'>Welcome To </span>"
            "<span style='font-size: 4rem;'>Karaoke</span>"
            "<span style='color: #1DB954; font-size: 4rem;'>Flow</span><strong>", unsafe_allow_html=True)


st.image("logo.png")



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
            print("Sorry, what did you say")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

        if st.button("Stop"):
            st.write("Stops")


CLIENT_ID     = "d71f5a9c01194c12b5b65f43032a0ea5"
CLIENT_SECRET = "17839d41b7f94d85829e78b9e2a66abb"
REDIRECT_URI  = "https://d1ghlj2ob2e0g7.cloudfront.net/" # Put the redirect URI here

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SCOPE = "user-read-email user-read-private"

auth_params = {
    "client_id":     CLIENT_ID,
    "response_type": "code",
    "redirect_uri":  REDIRECT_URI,
    "scope":         SCOPE,
}

login_url = f"{SPOTIFY_AUTH_URL}/?{urlencode(auth_params)}"



params = st.experimental_get_query_params()
if "code" in params:
    code = params["code"][0]

    # Exchange code for access token
    token_resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type":    "authorization_code",
            "code":          code,
            "redirect_uri":  REDIRECT_URI,
            "client_id":     CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )
    token_data = token_resp.json()
    access_token = token_data.get("access_token")

    if access_token:
        st.session_state["spotify_token"] = access_token # This is the access token that you should use for any stuff you want to use
        st.success("Spotify authentication successful!")


if st.session_state.get("spotify_token"):
    headers = {"Authorization": f"Bearer {st.session_state.spotify_token}"}
    user_profile = requests.get("https://api.spotify.com/v1/me", headers=headers).json()
    st.write("Logged in as", user_profile["display_name"])


 #Add the login stuff here
st.button(f"[Log in with Spotify]({login_url})")



