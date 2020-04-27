import telebot
import json
from telebot.types import Message
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from src.config import BotMarkUp

from src.lib import get_query

from src.telegram import bot

from src.spotify.bl import process_song_search, handle_artist_query
from src.spotify.queries import query_album_by_id, query_artist_by_id

from src.database.tables import User, Album, Track, Artist, Genre
from src.database.queries import insert, select_by_uid


def create_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)    
    markup.row(*BotMarkUp.COMMANDS_FSTROW)
    markup.row(*BotMarkUp.COMMANDS_SCNDROW)
    return 


def search_song(message):
    try:
        query = get_query(message.text)
        result_query = process_song_search(query)
    except IndexError as e:
        raise IndexError
    except ValueError as e:
        raise ValueError
    else:
        return result_query


def search_artist(message):
    try:
        query = get_query(message.text)
        result_query = handle_artist_query(query)
    except IndexError as e:
        raise IndexError
    except ValueError as e:
        raise ValueError
    else:
        return result_query


def send_text_message(text: str, message: Message, markup=None):
    chat_id = message.chat.id
    bot.send_message(chat_id, text, reply_markup=markup)


def get_artist_queries(artists):
    artist_queries = []
    for obj in artists:
        artist = query_artist_by_id(obj['id'])
        artist_query = {
            'uid': artist['id'],
            'name': artist['name'],
            'followers': artist['followers']['total'],
            'popularity': artist['popularity']
        }
        artist_queries.append(artist_query)
    return artist_queries


def get_genre_queries(artist_queries):
    genre_queries = []
    for obj in artist_queries:
        artist = query_artist_by_id(obj['uid'])
        for genre in artist['genres']:
            genre_query = {
                'name': genre,
            }
            genre_queries.append(genre_query)
    return genre_queries

# TODO add logging to the file
def call_insertions(album_queries, track_queries, genre_queries, artists):
    for track_query, album_query in zip(track_queries, album_queries):
        try:
            inserted_album = insert(Album, album_query)
        except IntegrityError:
            album = select_by_uid(Album, album_query['uid'])
            track_query['album_id'] = album['id']
        else:
            track_query['album_id'] = inserted_album.inserted_primary_key[0]
        try:
            insert(Track, track_query)
        except IntegrityError:
            pass
        artist_queries = get_artist_queries(artists)
        new_genre_queries = get_genre_queries(artist_queries)
        genre_queries.extend(new_genre_queries)
        for query in artist_queries:
            try:
                insert(Artist, query)
            except IntegrityError:
                pass
        for query in genre_queries:
            try:
                insert(Genre, query)
            except IntegrityError:
                pass
        


def handle_insert(tracks, artists, message: Message):
    album_queries = []
    track_queries = []
    genre_queries = []
    for track in tracks:
        album = query_album_by_id(track['album']['id'])
        if album['release_date_precision'] == 'day':
            date = datetime.strptime(album['release_date'], '%Y-%m-%d')
        if album['release_date_precision'] == 'year':
            date = datetime.strptime(album['release_date'], '%Y')
        album_query = {
            'uid': album['id'],
            'name': album['name'],
            'type': album['type'],
            'release': date,
            'label': album['label']
        }
        track_query = {
            'uid': track['id'],
            'name': track['name'],
            'duration': track['duration_ms'],
            'explicit': track['explicit'],
            'album_id': None
        }
        album_queries.append(album_query)
        track_queries.append(track_query)
        for genre in album['genres']:
            genre_queries.append({
                'name': genre
            })
    call_insertions(album_queries, track_queries, genre_queries, artists)

