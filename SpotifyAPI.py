import os, sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

env_path = resource_path('.env')
load_dotenv(env_path)

class SpotifyClient:

    def get_current_playback():
        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')
        redirect_uri = os.getenv('redirect_uri')
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                            client_secret=client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope="user-read-playback-state"))
        current_playback = sp.current_playback()
        if current_playback and current_playback['is_playing']:
            track = current_playback['item']
            track_name = track['name']
            track_artists = ', '.join(artist['name'] for artist in track['artists'])
            track_length = track['duration_ms'] // 1000  #to seconds
            current_time = current_playback['progress_ms'] // 1000  #to seconds
            thumbnail = track['album']['images'][2]['url']
            
            return {
                'track_name': track_name,
                'track_artists': track_artists,
                'track_length': track_length,
                'current_time': current_time,
                'thumbnail' : thumbnail
            }
        else:
            return None

        
