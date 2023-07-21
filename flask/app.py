from flask import Flask, request, jsonify, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from datetime import datetime


CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

app = Flask(__name__)

app.secret_key = "your_secret_key"
app.config['SESSION_COOKIE_NAME'] = 'Session Cookie'
TOKEN_INFO = "token_info"


# Creates the initial login/authentication page
@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


# This is the page the site takes you to after authentication
@app.route('/redirect')
def redirectPage():
    
    # Create new auth objecct and clear session
    sp_oauth = create_spotify_oauth()
    session.clear()

    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("getTracks", _external=True))


# Retrieve user's current top 10 songs for the month
@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")  # Change if redirect changes

    sp = spotipy.Spotify(auth=token_info['access_token'])
    song_objects = (sp.current_user_top_tracks(
        time_range='short_term', limit=15, offset=0)['items'])

    # adding function to extract only necessary data 
    return clean_song_data(song_objects)

# create playlist for input song data
@app.route('/createPlaylist')
def create_playlist():
    # copy from getTracks, only called once user is logged in
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    song_objects = (sp.current_user_top_tracks(
        time_range='short_term', limit=15, offset=0)['items'])

    track_ids = []
    track_names = []
    for track in song_objects:
        track_ids.append(track['id'])
        track_names.append(track['name'])

    username = sp.me()['id']
    month_year = datetime.today().strftime('%B %Y')
    playlist_name = f"My Top 15 Songs - {month_year}"
    playlist = sp.user_playlist_create(username, playlist_name)

    sp.playlist_add_items(playlist['id'], track_ids)

    return "Your playlist has been created"


# Exrtracts just the necessary data needed from the song JSON data
def clean_song_data(json_data):
    new_json = []
    
    for song in json_data:
        song_data = {}

        song_data['name'] = song['name']
        song_data['artist'] = song['artists'][0]['name']
        song_data['album_name'] = song['album']['name']
        song_data['cover_art'] = song['album']['images'][1]['url']
        song_data['audio_sample_url'] = song['preview_url']

        new_json.append(song_data)

    return new_json


# checks if authorization token is available, refreshes as needed
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = (token_info['expires_at'] - now) < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


# Create spotify authentication object
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for("redirectPage", _external=True),
        scope="user-top-read playlist-modify-public"
    )


if __name__ == "__main__":
    app.run()

