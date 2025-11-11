from math import floor

from src.redis import RedisClient


def spigot_calculation(accuracy: int, session_id: str):
    # this function not only calculates digits of pi,
    # but also sends progress info to redis.

    redis_client = RedisClient()

    if accuracy < 1:
        redis_client.set(f"progress:{session_id}", 1)
        return "INVALID PRECISION GIVEN"
    if accuracy == 1:
        redis_client.set(f"progress:{session_id}", 1)
        return "3"

    res = ""
    length = floor(10 * accuracy / 3) + 1
    a = [2 for _ in range(length)]
    nines = 0
    predigit = 0

    for i in range(1, accuracy + 1):
        q = 0
        for j in range(length, 0, -1):
            x = 10 * a[j - 1] + q * j
            a[j - 1] = x % (2 * j - 1)
            q = x // (2 * j - 1)
        a[0] = q % 10
        q //= 10
        if q == 9:
            nines += 1
        else:
            if q == 10:
                res += str(predigit + 1)
                res += ("0" * nines)
                predigit, nines = 0, 0
            else:
                res += str(predigit)
                predigit = q
                if nines != 0:
                    res += ("9" * nines)
                    nines = 0
        redis_client.set(f"progress:{session_id}", round(i / accuracy, 2))
    res += str(predigit)
    res = "3," + res[2:]
    return res
