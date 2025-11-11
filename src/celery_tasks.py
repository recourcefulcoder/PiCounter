from celery import Celery

from src.config import BROKER_HOST, BROKER_PORT
from src.redis import RedisClient
from src.utils import spigot_calculation

c_app = Celery(broker=f"redis://{BROKER_HOST}:{BROKER_PORT}/0")


@c_app.task(bind=True)
def calculate_pi_task(
        self,
        accuracy: int,
        session_id: str
):
    redis_client = RedisClient()
    current_id = redis_client.get(f"task_per_session:{session_id}")
    if current_id is not None:
        c_app.control.revoke(current_id.decode(), terminate=True)

    redis_client.set(f"task_per_session:{session_id}", f"{self.request.id}")
    redis_client.delete(f"result:{session_id}")
    redis_client.set(f"state:{session_id}", "PROGRESS")

    res = spigot_calculation(accuracy, session_id)

    redis_client.set(f"result:{session_id}", res)
    redis_client.set(f"state:{session_id}", "FINISHED")
    return True
