from telebot.types import Message
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from src.config import SPOTIFY_CONFIG


sp = Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CONFIG['client_id'],
        client_secret=SPOTIFY_CONFIG['secret']
    )
)


def get_query(text: str):
    args = text.split()
    query = args[1:]
    return ' '.join(query)


def query_search(q: str, type: str='track', limit: int=1):
    return sp.search(q=q, limit=limit, type=type)


def query_recommend(artist_id: list=None, track_id: list=None, limit: int=1):
    return sp.recommendations(seed_artists=artist_id, seed_tracks=track_id, limit=limit)
