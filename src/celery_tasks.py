from celery import Celery

from src.config import REDIS_URL
from src.redis import RedisClient
from src.utils import spigot_algorthm

c_app = Celery(broker=REDIS_URL)


@c_app.task(bind=True)
def calculate_pi_task(
        self,
        accuracy: int
):
    redis_client = RedisClient()
    current_id = redis_client.get(f"current_task_id").decode()
    if current_id is not None:
        c_app.control.revoke(str(current_id), terminate=True)
    redis_client.set("current_task_id", f"{self.request.id}")
    redis_client.delete("result")

    redis_client.set("state", "PROGRESS")
    res = spigot_algorthm(accuracy)
    redis_client.set("result", res)
    redis_client.set("state", "FINISHED")
    return True
