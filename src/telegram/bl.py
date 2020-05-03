from src.telegram import bot
import telebot
from uuid import uuid1
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
import json

from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from src.lib import format_query, deserialize

from src.database.tables import Track, Artist
from src.database.bl import insert_liked_tracks, insert_user, select_by_id

from src.telegram.lib import (
    search_song,
    search_artist,
    handle_insert,
    aggregate_response)

from src.spotify.bl import (
    recommend_song,
    recommend_artist,
    )

from src.youtube.bl import YouTubeAPI

from src.config import TelegramConfig, RESPONSE_LIFETIME
from src.telegram.services import bl as redis

def handle_commands(message: Message):
    with ThreadPoolExecutor(thread_name_prefix='Check user') as executor:
        t1 = executor.submit(partial(insert_user, message))
        command = message.text.split()[0]
        if command == '/get':
            handle_song_search(message=message)
        elif command == '/song':
            handle_song_recommendation(message)
        elif command == '/artist':
            handle_artist_recommendation(message)
        elif command == '/help':
            handle_help_command(message)
        t1.result()


def send_video(key: str, call: CallbackQuery):
    payload = redis.get(key)
    if not payload:
        print(f"Timeout for video payload - {key}")
        return 
    data = deserialize(payload)
    track = select_by_id(Track, data['track_id'])
    # TODO start adding to the video table in another tread
    artist = select_by_id(Artist, data['artist_id'])
    search_response = YouTubeAPI.youtube_search(artist=artist['name'], track=track['name'])
    url = YouTubeAPI.extract_url(search_response)
    send_text_message(url, call.message)


# Message_Id editMessage
@bot.callback_query_handler(func=lambda arg: True)
def callback_handler(call):
    data = call.data.split()
    if data[0] == 'like':
        insert_liked_tracks(data[1], call)
    elif data[0] == 'video':
        send_video(data[1], call)
        

def send_songs(response, message: Message):
    def hash_response(context: dict, uuid):
        payload = json.dumps(context)
        redis.set(uuid, payload, RESPONSE_LIFETIME)

    for idx, context in enumerate(response):
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        uuid = uuid1()
        like_btn = InlineKeyboardButton('Like', callback_data=f"like {str(uuid)}")
        video_btn = InlineKeyboardButton('Video', callback_data=f"video {str(uuid)}")
        markup.row(like_btn, video_btn)
        hash_response(context, str(uuid))
        send_text_message(context['text'], message, markup=markup)
        if idx + 1 == TelegramConfig.OUTPUT_LIMIT:
            break

# TODO Need asynchronous calls.... too slow
def handle_artist_recommendation(message: Message):
    try:
        search_response = search_artist(message)
        recommended = recommend_artist(search_response, message)
        tracks, artists = format_query(recommended, recommended=True)
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix='handle_inserts') as executor:
            t1 = executor.submit(partial(handle_insert, tracks, artists, message))
            insert_ids = t1.result()
        response = aggregate_response(insert_ids, tracks, artists)
        # response = YouTubeAPI.youtube_search_requests(tracks, artists)
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
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix='handle_inserts') as executor:
            t1 = executor.submit(partial(handle_insert, tracks, artists, message))
            insert_ids = t1.result()
        response = aggregate_response(insert_ids, tracks, artists)
        # response = YouTubeAPI.youtube_search_requests(tracks, artists)
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
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix='handle_inserts') as executor:
            t1 = executor.submit(partial(handle_insert, tracks, artists, message))
            insert_ids = t1.result()
        response = aggregate_response(insert_ids, tracks, artists)
        # response = YouTubeAPI.youtube_search_requests(tracks, artists)
        send_songs(response, message)
    except IndexError as e:
        send_text_message("Oops, no corresponding result", message)
    except ValueError as e:
        send_text_message('Oops, you are missing additional argument', message)


def handle_help_command(message):
    text = f"Here are the available commands:\n"\
        "/help - Help menu\n"\
        "/get <song> <artist> - Search for song\n"\
        "/artist <artist> - get related artists\n"\
        "/song <song> <artist> - get related songs\n"\
        "/stats - Statistic menu\n"\
        "/commands - 'Basic menu'\n"
    send_text_message(text, message)


def send_text_message(text: str, message: Message, markup=None):
    chat_id = message.chat.id
    bot.send_message(chat_id, text, reply_markup=markup)

