from celery import Celery

from src.config import BROKER_HOST, BROKER_PORT
from src.redis import RedisClient
from src.utils import spigot_calculation

c_app = Celery(broker=f"redis://{BROKER_HOST}:{BROKER_PORT}/0")


@c_app.task(bind=True)
def calculate_pi_task(
        self,
        accuracy: int
):
    redis_client = RedisClient()
    current_id = redis_client.get("current_task_id")
    if current_id is not None:
        c_app.control.revoke(current_id.decode(), terminate=True)

    redis_client.set("current_task_id", f"{self.request.id}")
    redis_client.delete("result")
    redis_client.set("state", "PROGRESS")

    res = spigot_calculation(accuracy)

    redis_client.set("result", res)
    redis_client.set("state", "FINISHED")
    return True
