import telebot
from src.telegram import bot
from telebot.types import Message
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from requests.exceptions import ReadTimeout
import sqlalchemy as sa
import logging

from src.static import MUSIC_URL

from src.config import BotMarkUp, BotCommands
from src.config import BOT_SECURITY, DB_URL
from src.spotify.queries import query_search, query_recommend
from src.telegram.lib import create_markup, send_text_message
from src.telegram.bl import (
    handle_song_recommendation,
    handle_artist_recommendation,
    handle_start_command,
    handle_song_search
)


# COMMANDS: 1. Get a song, 2. Recommend by track, 3. Recommends by Artist,
# TODO 1) PRIORITY COMMANDS to add: 4. Get favourite Songs, 5.Get favourite artists, optional (6.Get My genres)
# TODO 4) Research google youtube API. Integrate it ti search the song`s tracks.
# In case of recommendation by artist, search for the most popular track of that artist and use it to request the video.
# TODO handle process of adding data to the database, should be happening all the time until certain amount of rows will be filled.
# after what data will be added only on condition of being marked as liked one.
# TODO Request user`s friend list to display friends latest recommendation requests ).
# TODO (Optionally) Add aditional table for tracks features.
# TODO (Optional) to solve problems of updated nicknames create class of Chat.
# Encapsulate bot objects and date field to compare the date of current message  and update user info if the one has changed
# TODO (Optional) on Redis try to implement the cache vault for fetched results, which are retrieved after user request. 
# TODO (Optional) find lyrics video


@bot.message_handler(commands=['help'])
def command_help(message: Message):
    text = f"Here are the available commands:\n"\
        "/help - Help menu\n"\
        "/get <song> <artist> - Search for song\n"\
        "/artist <artist> - get related artists\n"\
        "/song <song> <artist> - get related songs\n"\
        "/stats - Statistic menu\n"\
        "/commands - 'Basic menu'\n"
    send_text_message(text, message) 


@bot.message_handler(commands=['start'])
def command_get(message: Message):
    handle_start_command(message)


@bot.message_handler(commands=['get'])
def command_get(message: Message):
    handle_song_search(message=message)


@bot.message_handler(commands=['artist'])
def command_artist(message: Message):
    handle_artist_recommendation(message)


@bot.message_handler(commands=['song'])
def command_song(message: Message):
    handle_song_recommendation(message)


@bot.message_handler(commands=['commands'])
def command_commands(message: Message):
    chat_id = message.chat.id
    markup = create_markup()
    text = "Use this commands to communicate with bot"
    bot.send_message(chat_id, text=text, reply_markup=markup)


@bot.message_handler(content_types=['document', 'text'])
def text_handler(message: Message):
    chat_id = message.chat.id
    if message.text not in (*BotMarkUp.COMMANDS_FSTROW, *BotMarkUp.COMMANDS_SCNDROW):
        markup = create_markup()
        bot.send_message(chat_id,
            "Ooops, did not get it. What you say?\n",
            reply_markup=markup)
    elif message.text == BotCommands.GET_SONG:
        msg = bot.send_message(chat_id, f"Hello my pezduk\nNow enter the song and the artist")
        bot.register_next_step_handler(msg, handle_song_search)
    elif message.text == BotCommands.RELATED_ARTIST:
        msg = bot.send_message(chat_id, f"Good\nNow enter name of the band that you like")
        result = bot.register_next_step_handler(msg, handle_artist_recommendation)
    elif message.text == BotCommands.RELATED_SONG:
        msg = bot.send_message(chat_id, f"Good\nNow enter name of the Song and band`s name")
        result = bot.register_next_step_handler(msg, handle_song_recommendation)
    elif message.text == BotCommands.NOTHING:
        bot.send_message(chat_id, f"Okey doing nithing :)")


def main():
    try:
        bot.polling(none_stop=True)
    except ReadTimeout as e:
        print(e)
        


if __name__ == "__main__":
    main()
