from telebot.types import Message
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from src.config import SpotifyConfig


sp = Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=SpotifyConfig.CLIENT_ID,
        client_secret=SpotifyConfig.SECRET
    )
)


def query_search(q: str, type: str='track', limit: int=1):
    return sp.search(q=q, limit=limit, type=type)


def query_recommend(artist_id: list=None, track_id: list=None, limit: int=1):
    return sp.recommendations(seed_artists=artist_id, seed_tracks=track_id, limit=limit)


def query_album_by_id(album_id: str) -> dict:
    return sp.album(album_id)


def query_artist_by_id(artist_id: str) -> dict:
    return sp.artist(artist_id)


def query_artist_by_id(artist_id: str) -> dict:
    return sp.artist(artist_id)