import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from telebot.types import Message
from datetime import datetime
import json

from src.lib import deserialize
from src.database.tables import (
    User,
    Album,
    Track,
    Artist,
    ArtistTrack,
    ArtistAlbum,
    UserAlbum,
    UserArtist,
    UserTrack)
from src.database.queries import insert, select_by_uid, select_with_id, update_by_id
from src.telegram.services import bl as redis
from src.config import USERNAME_LIFETIME


# TODO add logging to the file


def insert_user(message: Message):
    def converter(o):
        if isinstance(o, datetime):
            return o.__str__
    

    def cache_user(fetched, current_time, uid):
        context = represent_user(fetched, current_time)
        payload = json.dumps(context, default=converter)
        redis.set(uid, payload, USERNAME_LIFETIME)

    def aggergate_query(uid: int, current_time):
        username = message.chat.username
        return {
            'uid': uid,
            'username': username,
            'last_search': current_time,
            'liked_tracks': 0,
            'liked_artists': 0,
            'liked_albums': 0,
        }
    
    def represent_user(fetched, time):
        context = {key: value for key, value in fetched.items()}
        context['last_search'] = time
        return context
    
    def get_current_time():
        return datetime.now()


    def exception_insert(uid: int):
        fetched = select_by_uid(User, uid)
        current_time = get_current_time()
        if fetched:
            update_by_id(User, {'last_search': current_time}, fetched['id'])
            cache_user(fetched, current_time, uid)
        else:
            query = aggergate_query(uid, current_time)
            inserted_user = insert(User, query)
            query['id'] = inserted_user.inserted_primary_key[0]
            cache_user(query, current_time, uid)

    res = redis.get(message.chat.id)
    if not res:
        exception_insert(message.chat.id)


def track_album_artist_insert(track_query, album_query, artist_query):
    try:
        inserted_album = insert(Album, album_query)
    except IntegrityError:
        album = select_by_uid(Album, album_query['uid'])
        track_query['album_id'] = album['id']
    else:
        track_query['album_id'] = inserted_album.inserted_primary_key[0]
    try:
        inserted_track = insert(Track, track_query)
    except IntegrityError:
        track = select_by_uid(Track, track_query['uid'])
        track_id = track['id']
    else:
        track_id = inserted_track.inserted_primary_key[0]
    try:
        inserted_artist = insert(Artist, artist_query)
    except IntegrityError:
        artist = select_by_uid(Artist, artist_query['uid'])
        artist_id = artist['id']

    else:
        artist_id = inserted_artist.inserted_primary_key[0]
    return {
        'artist_id': artist_id,
        'album_id': track_query['album_id'],
        'track_id': track_id
        }


def artist_track_insert(id_pack):
    query = {
        'artist_id': id_pack['artist_id'],
        'track_id': id_pack['track_id']
    }
    try:
        result = insert(ArtistTrack, query)
    except IntegrityError as e:
        print(f"Add logger {e} database/bl.py")


def artist_album_insert(id_pack):
    query = {
        'artist_id': id_pack['artist_id'],
        'album_id': id_pack['album_id']
    }
    try:
        result = insert(ArtistAlbum, query)
    except IntegrityError as e:
        print(f"Add logger {e} database/bl.py")

def insert_user_track(user_id, track_id):
    try:
        insert(UserTrack, {'user_id': user_id, 'track_id': track_id})
    except IntegrityError as e:
        print(f"Add logger {e} database/bl.py")


def insert_user_album(user_id, album_id):
    try:
        insert(UserAlbum, {'user_id': user_id, 'album_id': album_id})
    except IntegrityError as e:
        print(f"Add logger {e} database/bl.py")


def insert_user_artist(user_id, artist_id):
    try:
        insert(UserArtist, {'user_id': user_id, 'artist_id': artist_id})
    except IntegrityError as e:
        print(f"Add logger {e} database/bl.py")

# TODO delete the hash after timeout
# TODO add timeout
# TODO make call to cache to retrieve user_id
def insert_liked_tracks(key: str, call):
        
    payload = redis.get(key)
    if not payload:
        print(f"Timeout for track payload - {key}")
        return 
    context = deserialize(payload)
    res = redis.get(call.message.chat.id)
    if not res:
        user = select_by_uid(User, call.message.chat.id)
    else:
        user = deserialize(res)
    user_id = user['id']
    insert_user_track(user_id, context['track_id'])
    insert_user_album(user_id, context['album_id'])
    insert_user_artist(user_id, context['artist_id'])


def select_by_id(table: sa.Table, id: int):
    return select_with_id(table=table, id=id)

    


