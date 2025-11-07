import redis

from src.config import BROKER_HOST, BROKER_PORT


class RedisClient:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.__initialized = False

        return cls.__instance

    def __init__(self, host: str = BROKER_HOST, port: int = BROKER_PORT):
        if self.__initialized:
            return
        self._redis = redis.Redis(host=host, port=port)
        self.__initialized = True

    def set(self, *args, **kwargs):
        return self._redis.set(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._redis.get(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._redis.delete(*args)

    def close_connection(self):
        self._redis.close()
