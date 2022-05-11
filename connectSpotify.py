from dotenv import load_dotenv
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util
import requests

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "https://prabhav-khera.netlify.com"

def connect(username):
    # client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    # sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    # url = "	https://api.spotify.com/v1/me"
    # response = requests.get(url, headers={"Authorization": "Bearer " + os.getenv("SPOTIFY_TOKEN")})
    # # username = requests.get(url).json()['display_name']
    # username = response.json()['display_name']
    scope = "user-library-read user-top-read playlist-modify-public user-follow-read"
    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    os.environ['SPOTIFY_TOKEN'] = token

    return token

def authenticate():
    if os.getenv("SPOTIFY_TOKEN"):
        token = os.getenv("SPOTIFY_TOKEN")
        print('... Connected to Spotify ...')
        sp = spotipy.Spotify(auth=token)
        return sp
    else:
        print('... Unable to connect to Spotify ...')
        sys.exit(1)

