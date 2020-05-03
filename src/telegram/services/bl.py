from src.telegram.services import redis


def hset(name: str, key: str, value: str):
	redis.client.hset(name, key, value)


def hget(name: str, key: str):
	return redis.client.hget(name, key)


def get(key: str):
	return redis.client.get(key)


def set(key: str, value: str, ex=None):
	redis.client.set(key, value, ex=ex)


def delete(*names):
	redis.client.delete(*names)