from __future__ import annotations
from telebot.types import Message
from src.spotify.queries import query_search, query_recommend
from src.config import SpotifyConfig

# from src.telegram.bl import send_text_message


def recommend_song(query: str):
    track_uid = query['tracks']['items'][0]['id']
    recommended = query_recommend(track_id=[track_uid], limit=SpotifyConfig.RECOMMENDATION_LIMIT)
    return recommended

# TODO DELETE from the recommendation response the original artist
def recommend_artist(query: str, message: Message):
    artist_uid = query['artists']['items'][0]['id']
    recommended = query_recommend([artist_uid], limit=SpotifyConfig.RECOMMENDATION_LIMIT)
    return recommended


def handle_artist_query(search_query: str) -> str:
    try:
        if not search_query:
            raise ValueError
        result_query = query_search(search_query, type='artist')
        result_query['artists']['items'][0]['id']
    except IndexError:
        raise IndexError
    except ValueError:
        raise ValueError
    else:
        return result_query


def handle_song_query(search_query: str, limit: int=1) -> str:
    result_query = query_search(search_query, type='track')
    try:
        result_query['tracks']['items'][0]['id']
    except IndexError:
        raise IndexError
    else:
        return result_query


def process_song_search(raw_query: str):
    try:
        if not raw_query:
            raise ValueError
        result_query = handle_song_query(raw_query, limit=SpotifyConfig.SEARCH_LIMIT)
    except IndexError:
        raise IndexError
    except ValueError:
        raise ValueError
    return result_query


# 403820486