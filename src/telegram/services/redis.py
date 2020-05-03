from redis import Redis
from src.config import REDIS

client = Redis(**REDIS)