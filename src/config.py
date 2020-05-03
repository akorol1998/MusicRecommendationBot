# Docker version
DB = {
    "host": 'localhost',
    'port': '3306',
    "user": 'root',
    "password": "1234admin",
    'name': 'Test_db'
}

# DB = {
#     "user": 'akorol',
#     "password": "ComputerVision#69",
#     "host": 'localhost',
#     'port': 3306,
#     'name': 'mydb',
# }

DB_URL = f"mysql+mysqlconnector://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['name']}"

BOT_SECURITY = {
    "token": "1157412145:AAHmaxbxOrZ-PLPSVNLD0cfd810iBil_yJA",
}

REDIS = {
	'host': "localhost",
	'port': "6379"
}

USERNAME_LIFETIME = 60
RESPONSE_LIFETIME = 60


class TelegramConfig:
    OUTPUT_LIMIT = 3


class SpotifyConfig:
    CLIENT_ID = 'a640dba5487449dbb2b9f1aa74775fd1'
    SECRET = '13465664e65d4b6f8db3d89932f879cc'
    SEARCH_LIMIT = 1
    RECOMMENDATION_LIMIT = 10


class BotCommands:
    GET_SONG = "Find a song"
    NOTHING = "Do Nothing"
    RELATED_ARTIST = "Find related artist"
    RELATED_SONG = "Find related song"


class BotMarkUp:
    COMMANDS_FSTROW = ("Find a song", "Do Nothing")
    COMMANDS_SCNDROW = ("Find related artist", "Find related song")
    

class YouTubeUtils:
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    PART_ID = 'id'
    PART_SNIPPET = 'snippet'
    MAX_RESULTS = 1
    VIDEO_BASE_URL = 'https://www.youtube.com/watch?v='
    YOUTUBE_DEVELOPER_KEY = 'AIzaSyCe3AJV9GVyKH_iWugYgmZKkkBsSII3Paw'

