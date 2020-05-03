import telebot
from telebot.types import Message
from datetime import datetime
from concurrent.futures.thread import ThreadPoolExecutor
import json

from src.config import BotMarkUp

from src.lib import get_query

from src.telegram import bot

from src.spotify.bl import (
    process_song_search,
    handle_artist_query,
    get_artist_queries)

from src.spotify.queries import query_album_by_id

from src.database.bl import track_album_artist_insert, artist_album_insert, artist_track_insert



def create_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)    
    markup.row(*BotMarkUp.COMMANDS_FSTROW)
    markup.row(*BotMarkUp.COMMANDS_SCNDROW)
    return 


def search_song(message):
    try:
        query = get_query(message.text)
        result_query = process_song_search(query)
    except IndexError:
        raise IndexError
    except ValueError:
        raise ValueError
    else:
        return result_query


def search_artist(message):
    try:
        query = get_query(message.text)
        result_query = handle_artist_query(query)
    except IndexError:
        raise IndexError
    except ValueError:
        raise ValueError
    else:
        return result_query


def make_album_query(album: dict):
    if album['release_date_precision'] == 'day':
        date = datetime.strptime(album['release_date'], '%Y-%m-%d')
    if album['release_date_precision'] == 'month':
        date = datetime.strptime(album['release_date'], '%Y-%m')
    if album['release_date_precision'] == 'year':
        date = datetime.strptime(album['release_date'], '%Y')
    return {
            'uid': album['id'],
            'name': album['name'],
            'type': album['type'],
            'release': date,
            'label': album['label']
            }


def make_track_query(track: dict):
    return {
            'uid': track['id'],
            'name': track['name'],
            'duration': track['duration_ms'],
            'explicit': track['explicit'],
            'album_id': None
        }


def call_insertions(generator):
    # with ThreadPoolExecutor(max_workers=3) as executor:
    inserted_ids = []
    for artist_query, album_query, track_query in generator:
        id_pack = track_album_artist_insert(
                track_query,
                album_query,
                artist_query)
        artist_track_insert(id_pack)
        artist_album_insert(id_pack)
        inserted_ids.append(id_pack)
        # t1 = executor.submit(artist_track_insert, id_pack)
        # id_pack_2 = deepcopy(id_pack)
        # t2 = executor.submit(artist_album_insert, id_pack_2)
    return inserted_ids


def handle_insert(tracks, artists, message: Message):
    album_queries = []
    track_queries = []
    for track in tracks:
        album = query_album_by_id(track['album']['id'])
        # insert genre_has_album
        album_query = make_album_query(album)
        track_query = make_track_query(track)
        album_queries.append(album_query)
        track_queries.append(track_query)
    artist_queries = get_artist_queries(artists)
    return call_insertions(zip(artist_queries, album_queries, track_queries))


def aggregate_response(insert_ids, tracks, artists):
    for inserted, track, artist in zip(insert_ids, tracks, artists):
        yield {
            'text':f"{track['name']} - {artist['name']}",
            'track_uid': track['id'],
            'artist_id': inserted['artist_id'],
            'album_id': inserted['album_id'],
            'track_id': inserted['track_id'],
            }

# {'album_id': None, 'duration': 239000, 'explicit': False, 'name': 'The Crazy Ones', 'uid': '0TSyISpqnV0Q3wsYtnJFyl'}
