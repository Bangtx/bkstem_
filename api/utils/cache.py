import redis
from functools import lru_cache

from config.setting import REDIS_DB, REDIS_HOST, REDIS_PORT


@lru_cache(maxsize=1)
def client():
    return redis.StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
    )


def get(key: str):
    return client().get(key)


def set(key: str, value, ttl=None):
    return client().set(key, value, ex=ttl)


def delete(key: str):
    return client().delete(key)


def clear():
    c = client()
    for key in c.scan_iter("*"):
        c.delete(key)
