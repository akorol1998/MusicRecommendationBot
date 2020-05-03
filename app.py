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
from src.telegram.lib import create_markup
from src.telegram.bl import (
    handle_song_recommendation,
    handle_artist_recommendation,
    handle_song_search,
    handle_commands
)


# TODO Request user`s friend list to display friends latest recommendation requests).
# TODO (Optionally) Add aditional table for tracks features.
# TODO (Optional) to solve problems of updated nicknames create class of Chat.
# Encapsulate bot objects and date field to compare the date of current message  and update user info if the one has changed
# TODO (Optional) on Redis try to implement the cache vault for fetched results, which are retrieved after user request. 
# TODO (Optional) find lyrics video


@bot.message_handler(commands=['help'])
def command_help(message: Message):
    handle_commands(message)


@bot.message_handler(commands=['start'])
def command_get(message: Message):
    handle_commands(message)


@bot.message_handler(commands=['get'])
def command_get(message: Message):
    handle_commands(message)


@bot.message_handler(commands=['artist'])
def command_artist(message: Message):
    handle_commands(message)


@bot.message_handler(commands=['song'])
def command_song(message: Message):
    handle_commands(message)
    


# @bot.message_handler(commands=['commands'])
# def command_commands(message: Message):
#     chat_id = message.chat.id
#     markup = create_markup()
#     text = "Use this commands to communicate with bot"
#     bot.send_message(chat_id, text=text, reply_markup=markup)


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
