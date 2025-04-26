import streamlit as st
from urllib.parse import urlencode
import requests

st.set_page_config(
    page_title="TEST 1",
    layout="wide",
)

# 1) Load credentials
CLIENT_ID     = "d71f5a9c01194c12b5b65f43032a0ea5" 
CLIENT_SECRET = "17839d41b7f94d85829e78b9e2a66abb"
REDIRECT_URI  = "https://d1ghlj2ob2e0g7.cloudfront.net/" # Put the redirect URI here

# 2) Build Spotify authorization URL
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SCOPE = "user-read-email user-read-private"

# Auth object
auth_params = {
    "client_id":     CLIENT_ID,
    "response_type": "code",
    "redirect_uri":  REDIRECT_URI,
    "scope":         SCOPE,
}

# Login url
login_url = f"{SPOTIFY_AUTH_URL}/?{urlencode(auth_params)}"

 #Add the login stuff here
st.markdown(f"[Log in with Spotify]({login_url})")

# 3) Handle the callback
params = st.query_params()
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

# 4) Use the token for any API calls
if st.session_state.get("spotify_token"):
    headers = {"Authorization": f"Bearer {st.session_state.spotify_token}"}
    user_profile = requests.get("https://api.spotify.com/v1/me", headers=headers).json()
