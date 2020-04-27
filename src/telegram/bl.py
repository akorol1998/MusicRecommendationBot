from src.telegram import bot
import json
import itertools

from typing import List
from datetime import datetime
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from src.lib import format_query

from src.database.tables import User, Album, Track
from src.database.queries import insert, select_by_uid

from src.telegram.lib import send_text_message, search_song, search_artist, handle_insert

from src.spotify.bl import (
    recommend_song,
    recommend_artist,
    )

from src.youtube.bl import YouTubeAPI

from src.config import TelegramConfig


def handle_start_command(message: Message):
    res = select_by_uid(User, message.chat.id)
    if not res:
        uid = message.chat.id
        username = message.chat.username
        current_time = datetime.now()
        insert_query = {
            'uid': uid,
            'username': username,
            'last_search': current_time,
            'liked_tracks': 0,
            'liked_artists': 0,
            'liked_albums': 0,
        }
        insert(User, insert_query)
    else:
        send_text_message(f"Wellcome back {message.chat.first_name}", message)


def send_songs(response, message: Message):
    for idx, context in enumerate(response):
        send_text_message(context['link'], message)
        if idx + 1 == TelegramConfig.OUTPUT_LIMIT:
            break
   
# TODO can do even without callback_data
# just add to Redis data with a key = {username + uid} when there is request for recommendation
# After load more is pressed load from Redis information about tracks and artists
# TODO Leave it to be done later, concentrate on DataBase.
# BAD Solution but can not serialize generator ((
#         payload = json.dumps(context)
#         markup = InlineKeyboardMarkup()
#         button = InlineKeyboardButton(text='Load more', callback_data=payload)
#         markup.add(button)

# TODO Need asynchronous calls.... too slow
def handle_artist_recommendation(message: Message):
    try:
        search_response = search_artist(message)
        recommended = recommend_artist(search_response, message)
        tracks, artists = format_query(recommended, recommended=True)
        handle_insert(tracks, artists, message)
        response = YouTubeAPI.youtube_search_requests(tracks, artists)
        send_songs(response, message)
    except IndexError as e:
        send_text_message("Oops, no corresponding result", message)
    except ValueError as e:
        send_text_message('Oops, you are missing additional argument', message)

# TODO Need asynchronous calls.... too slow
def handle_song_recommendation(message: Message):
    try:
        result_query = search_song(message)
        recommended = recommend_song(result_query)
        tracks, artists = format_query(recommended, recommended=True)
        handle_insert(tracks, artists, message)
        response = YouTubeAPI.youtube_search_requests(tracks, artists)
        send_songs(response, message)
    except IndexError as e:
        send_text_message("Oops, no corresponding result", message)
    except ValueError as e:
        send_text_message('Oops, you are missing additional argument', message)

# TODO Need asynchronous calls.... too slow
def handle_song_search(message: Message):
    try:
        result_query = search_song(message)
        tracks, artists = format_query(result_query, song_search=True)
        handle_insert(tracks, artists, message)
        response = YouTubeAPI.youtube_search_requests(tracks, artists)
        send_songs(response, message)
    except IndexError as e:
        send_text_message("Oops, no corresponding result", message)
    except ValueError as e:
        send_text_message('Oops, you are missing additional argument', message)

