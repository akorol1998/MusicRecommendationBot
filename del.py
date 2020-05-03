
from src.config import REDIS
import redis
from uuid import uuid1



def main():
	client = redis.Redis(**REDIS)
	client.hset('uuid', 'track_id', 1)
	client.hset('uuid', 'album_id', 1)
	client.hset('uuid', 'artist_id', 1)
	print(client.hget('uuid', 'album_id'))


if __name__ == '__main__':
	main()
	