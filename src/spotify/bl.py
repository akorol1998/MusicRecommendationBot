from __future__ import annotations
import telebot
from telebot.types import Message
from src.spotify.queries import query_search, query_recommend
from src.config import BOT_SECURITY, SPOTIFY_CONFIG


bot = telebot.TeleBot(BOT_SECURITY['token'])


def song_recommendation_step(message: Message):
    raw_query = message.text
    process_song_query(raw_query=raw_query, message=message)


def artist_recommendation_step(message: Message):
    query = message.text
    process_artist_query(raw_query=query, message=message)


def recommend_song(query: str, message: Message):
    origin_id = query['tracks']['items'][0]['id']
    track_uid = query['tracks']['items'][0]['id']
    recommended = query_recommend(track_id=[track_uid], limit=SPOTIFY_CONFIG['search_limit'])
    track_uid = recommended['tracks'][0]['id']
    for idx, obj in enumerate(recommended['tracks']):
        text = f"{obj['name']} - {obj['artists'][0]['name']}"
        if origin_id != obj['id']:
            send_text_message(text=text, message=message)


def recommend_artist(query: str, message: Message):
    origin_id = query['artists']['items'][0]['id']
    artist_uid = query['artists']['items'][0]['id']
    recommended = query_recommend([artist_uid], limit=SPOTIFY_CONFIG['search_limit'])
    for idx, obj in enumerate(recommended['tracks']):
        text = obj['artists'][0]['name']
        if origin_id != obj['artists'][0]['id']:
            send_text_message(text=text, message=message)


def send_song(query: str, message: Message):
    for idx, track in enumerate(query['tracks']['items']):
        send_text_message(f"{track['artists'][0]['name']} - {track['name']}", message)
        if idx == 0:
            break


def handle_artist_query(search_query: str) -> str:
	result_query = query_search(search_query, type='artist')
	try:
		result_query['artists']['items'][0]['id']
	except IndexError:
		raise IndexError
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


def process_song_query(raw_query: str, message: Message):
	if not raw_query:
		send_text_message('Oops, you are missing additional argument', message)
	else:
		try:
			recommend_query = handle_song_query(raw_query)
		except IndexError:
			send_text_message("Oops, no corresponding result", message)
		else:
			recommend_song(recommend_query, message)


def process_artist_query(raw_query: str, message: Message):
	if not raw_query:
		send_text_message('Oops, you are missing additional argument', message)
	else:
		try:
			recommend_query = handle_artist_query(raw_query)
		except IndexError:
			send_text_message("Oops, no corresponding result", message)
		else:
			recommend_artist(recommend_query, message)


def process_song_search(raw_query: str, message: Message):
	if not raw_query:
		send_text_message('Oops, you are missing additional argument', message)
	else:
		try:
			result_query = handle_song_query(raw_query, limit=SPOTIFY_CONFIG['search_limit'])
		except IndexError:
			send_text_message("Oops, no corresponding result", message)
		else:
			send_song(result_query, message)


def send_text_message(text: str, message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, text)

# 403820486