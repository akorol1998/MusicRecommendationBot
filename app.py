import telebot
from src.spotify.bl import bot
from telebot.types import Message
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sqlalchemy as sa

from src.static import MUSIC_URL
from src.config import BotMarkUp, BotCommands
from src.interface import create_markup
from src.config import BOT_SECURITY, SPOTIFY_CONFIG, DB_URL
from src.spotify.queries import query_search, query_recommend, get_query
from src.spotify.bl import (
    send_text_message,
    song_recommendation_step,
    artist_recommendation_step,
    process_song_query,
    process_artist_query,
    process_song_search
    )

from src.database.tables import metadata, User

# COMMANDS: 1. Get a song, 2. Recommend by track, 3. Recommends by Artist,
# TODO 1) PRIORITY COMMANDS to add: 4. Get favourite Songs, 5.Get favourite artists, optional (6.Get My genres)
# TODO 4) Research google youtube API. Integrate it ti search the song`s tracks.
# In case of recommendation by artist, search for the most popular track of that artist and use it to request the video.
# TODO 3) Check the DB for the right structure and connect it to the app.
# TODO Add user to the DB table.
# TODO handle process of adding data to the database, should be happening all the time until certain amount of rows will be filled.
# after what data will be added only on condition of being marked as liked one.
# TODO Request user`s friend list to display friends latest recommendation requests ).
# TODO (Optionally) Add aditional table for tracks features.
# TODO (Optional) to solve problems of updated nicknames create class of Chat.
# Encapsulate bot objects and date field to compare the date of current message  and update user info if the one has changed


@bot.message_handler(commands=['help'])
def command_help(message: Message):
    text = f"Here are the available commands:\n"\
        "/help - Help menu\n"\
        "/get <song> <artist> - Search for song\n"\
        "/artist <artist> - get related artists\n"\
        "/song <song> <artist> - get related songs\n"\
        "/stats - Statistic menu"\
        "/commands - 'Basic menu'\n"
    send_text_message(text, message)    


@bot.message_handler(commands=['start'])
def command_get(message: Message):
    me = bot.get_me()
    print(me)



@bot.message_handler(commands=['get'])
def command_get(message: Message):
    query = get_query(message.text)
    process_song_search(raw_query=query, message=message)


@bot.message_handler(commands=['artist'])
def command_artist(message: Message):
    query = get_query(message.text)
    process_artist_query(query, message)


@bot.message_handler(commands=['song'])
def command_song(message: Message):
    query = get_query(message.text)
    process_song_query(raw_query=query, message=message)


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
        msg = bot.send_message(chat_id, f"Hello my pezduk\nnow enter the song and the artist in the following form\n<song> - <artist> example: My Propeller - Arctic Monkeys")
        bot.register_next_step_handler(msg, find_song)
    elif message.text == BotCommands.RELATED_ARTIST:
        msg = bot.send_message(chat_id, f"Good\nNow enter name of the band that you like")
        result = bot.register_next_step_handler(msg, artist_recommendation_step)
    elif message.text == BotCommands.RELATED_SONG:
        msg = bot.send_message(chat_id, f"Good\nNow enter name of the Song and band`s name")
        result = bot.register_next_step_handler(msg, song_recommendation_step)
    elif message.text == BotCommands.NOTHING:
        bot.send_message(chat_id, f"Okey doing nithing :)")


# TODO create tables-classes for the database
def _create_tables(engine):
    engine = _create_engine()
    metadata.create_all(engine)


def _create_engine():
    return sa.create_engine(DB_URL)


def _drop_tables():
    engine = _create_engine()
    metadata.drop_all(engine)


def db_init():
    engine = sa.create_engine(DB_URL)
    conn = engine.connect()
    _drop_tables()
    _create_tables()
    
    query = User.select()
    print(query)
    res = conn.execute(query)
    print(res.fetchall())


def main():
    db_init()
    bot.polling()


if __name__ == "__main__":
    main()
