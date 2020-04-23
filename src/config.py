DB = {
	"user": 'akorol',
	"password": "ComputerVision#69",
	"host": 'localhost',
	'port': 3306,
	'name': 'mydb',
}

DB_URL = f"mysql+mysqlconnector://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['name']}"


SPOTIFY_CONFIG = {
    "client_id": "a640dba5487449dbb2b9f1aa74775fd1",
    "secret": "13465664e65d4b6f8db3d89932f879cc",
    "search_limit": 10,
    }

BOT_SECURITY = {
    "token": "1157412145:AAHmaxbxOrZ-PLPSVNLD0cfd810iBil_yJA",
}


class BotCommands:
    GET_SONG = "Find a song"
    NOTHING = "Do Nothing"
    RELATED_ARTIST = "Find related artist"
    RELATED_SONG = "Find related song"


class BotMarkUp:
    COMMANDS_FSTROW = ("Find a song", "Do Nothing")
    COMMANDS_SCNDROW = ("Find related artist", "Find related song")
    
