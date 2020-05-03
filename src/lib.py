import json

def get_query(text: str):
    args = text.split()
    if text.startswith('/'):
        query = args[1:]
    else:
        query = args
    return ' '.join(query)


def format_query(
    response: dict,
    recommended: bool=False,
    song_search: bool=False,
    ):
    tracks = []
    artists = []
    if song_search:
        for idx, obj in enumerate(response['tracks']['items']):
            tracks.append(obj)
            artists.append(obj['artists'][0])
    elif recommended:
        for idx, obj in enumerate(response['tracks']):
            tracks.append(obj)
            artists.append(obj['artists'][0])
    return tracks, artists


def deserialize(payload):
        return json.loads(payload)

