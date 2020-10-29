import json
from flask import Flask , request, redirect, render_template, Blueprint
import requests
from src.application.spotify_auth import SpotifyAuth
import os
from src.application.bootstrap import postgresql_artists_repository

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
api = Blueprint("api", __name__, template_folder = os.path.join(template_dir, 'src', 'templates'))

# Spotify URLS
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000

spotify_auth = SpotifyAuth()

@api.route('/', methods=['GET'])
def index():
    return redirect(spotify_auth.getUser())

@api.route('/auth/callback', methods=['GET', 'POST'])
def callback():
    auth_token = request.args['code']
    response_data = spotify_auth.getUserToken(auth_token)

    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    expires_in = response_data["expires_in"]
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # Push new releases in database
    new_releases_api_endpoint = "{}/browse/new-releases".format(SPOTIFY_API_URL)
    new_releasess_response = requests.get(new_releases_api_endpoint, headers=authorization_header)
    new_releases_data = json.loads(new_releasess_response.text)

    new_releases = [{'id_new_releases': x['id'], 'album_type': x['album_type'], 'available_markets': ','.join(x['available_markets']), 'href_api': x['href'], 'href_spotify': x['external_urls']['spotify'], 'name': x['name'], 'release_date': x['release_date'], 'type': x['type'], 'uri': x['uri'], 'artists':x['artists']} for x in new_releases_data['albums']['items']]
    postgresql_artists_repository.add_new_releases(new_releases)

    display_arr = new_releases_data['albums']['items']
    return render_template("index.html", sorted_array=display_arr)

@api.route('/new_releases', methods=['GET'])
def new_releases():
    return postgresql_artists_repository.get_new_releases()

@api.route('/api/artists', methods=['GET'])
def get_artists_of_new_releases():
    return postgresql_artists_repository.get_artists_new_releases()
