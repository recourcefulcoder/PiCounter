from typing import Annotated

from fastapi import Depends

from .redis import RedisClient


def get_redis_client():
    return RedisClient()


RedisDep = Annotated[RedisClient, Depends(get_redis_client)]
