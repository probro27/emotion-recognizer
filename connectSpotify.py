from tokenize import group
from dotenv import load_dotenv
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util
import requests
import random

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

def aggregate_top_artists(sp):
    print('... Aggregating top artists ...')
    top_artists_name = []
    top_artists_uri = []

    ranges = ['short_term', 'medium_term', 'long_term']
    for range in ranges:
        top_artists_all_data = sp.current_user_top_artists(limit=50, time_range=range)
        top_artists_data = top_artists_all_data['items']
        for artist in top_artists_data:
            top_artists_name.append(artist['name'])
            top_artists_uri.append(artist['uri'])
    
    followed_artists_all_data = sp.current_user_followed_artists(limit=50)
    followed_artists_data = followed_artists_all_data['artists']
    for artist in followed_artists_data['items']:
        if artist['name'] not in top_artists_name:
            top_artists_name.append(artist['name'])
            top_artists_uri.append(artist['uri'])
    return top_artists_uri

def aggregate_top_tracks(sp, top_artists_uri):
    print('... Aggregating top tracks ...')
    top_tracks_uri = []
    for artist in top_artists_uri:
        top_tracks_all_data = sp.artist_top_tracks(artist)
        top_tracks_data = top_tracks_all_data['tracks']
        for track in top_tracks_data:
            top_tracks_uri.append(track['uri'])
    return top_tracks_uri

def select_tracks(sp, top_tracks_uri):
    print('... Selecting tracks ...')
    mood = os.getenv("MOOD")

    tracks_selected = []
    random.shuffle(top_tracks_uri)
    for track in top_tracks_uri[0:100]:
        track_all_data = sp.audio_features(track)
        for track_data in track_all_data:
            try:
                if mood == 'happy':
                    if track_data['valence'] > 0.5:
                        tracks_selected.append(track_data['uri'])
                elif mood == 'calm':
                    if track_data['valence'] < 0.5:
                        tracks_selected.append(track_data['uri'])
                elif mood == 'fearful':
                    if track_data['valence'] < 0.5:
                        tracks_selected.append(track_data['uri'])
                elif mood == 'disgust':
                    if track_data['valence'] < 0.5:
                        tracks_selected.append(track_data['uri'])
                else:
                    tracks_selected.append(track_data['uri'])
            except:
                pass
    return tracks_selected


def create_playlist(sp, selected_tracks):
    print('... Creating playlist ...')
    user_all_data = sp.current_user()
    user_id = user_all_data['id']

    play_list_name = os.getenv("MOOD") + ' playlist'
    playlist_data = sp.user_playlist_create(user_id, play_list_name)
    playlist_uri = playlist_data['external_urls']['spotify']
    playlist_id = playlist_data['id']
    sp.user_playlist_add_tracks(user_id, playlist_id, selected_tracks[0:30])
    return playlist_uri

