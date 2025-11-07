from contextlib import asynccontextmanager

from fastapi import FastAPI

import src.dependencies as dp
from src.celery_tasks import calculate_pi_task
from src.redis import RedisClient
from src.schemas import ProgressResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = RedisClient()
    redis_client.set("state", "FINISHED")
    redis_client.set("progress", 1.0)
    yield
    RedisClient().close_connection()


app = FastAPI(lifespan=lifespan)


@app.get("/calculate_pi")
async def calculate_pi(n: int):
    calculate_pi_task.delay(n)
    return {
        "message": f"Request accepted! {n} signes of Pi are being evaluated..."
    }


@app.get("/check_progress")
async def check_progress(redis_client: dp.RedisDep) -> ProgressResponse:
    result = redis_client.get("result")
    if result is not None:
        result = result.decode()
    return ProgressResponse(
        state=redis_client.get("state").decode(),
        progress=redis_client.get("progress"),
        result=result,
    )
