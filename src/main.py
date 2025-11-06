from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.celery_tasks import calculate_pi_task
from src.redis import RedisClient
import src.dependencies as dp


@asynccontextmanager
async def lifespan(app: FastAPI):
    RedisClient()
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
async def check_progress(redis_client: dp.RedisDep):
	return {
		"state": redis_client.get("state"),
		"progress": redis_client.get("progress"),
		"result": redis_client.get("result"),
	}
