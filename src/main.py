import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

import src.dependencies as dp
from src.celery_tasks import calculate_pi_task
from src.config import SESSION_SECRET
from src.redis import RedisClient
from src.schemas import ProgressResponse

from starlette.middleware.sessions import SessionMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = RedisClient()
    redis_client.set("state", "FINISHED")
    redis_client.set("progress", 1.0)
    yield
    RedisClient().close_connection()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def ensure_session_id(request: Request, call_next):
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())

    response = await call_next(request)
    return response

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    max_age=3600,
)


@app.get("/calculate_pi")
async def calculate_pi(n: int, request: Request):
    calculate_pi_task.delay(n, request.session["session_id"])
    return {
        "message": f"Request accepted! {n} signes of Pi are being evaluated..."
    }


@app.get("/check_progress")
async def check_progress(
        redis_client: dp.RedisDep,
        request: Request,
) -> ProgressResponse:
    session_id = request.session["session_id"]

    result = redis_client.get(f"result:{session_id}")
    progress = redis_client.get(f"progress:{session_id}")
    state = redis_client.get(f"state:{session_id}")

    result = result.decode() if result is not None else None
    progress = progress if progress is not None else 1.0
    state = state.decode() if state is not None else "FINISHED"

    return ProgressResponse(
        state=state,
        progress=progress,
        result=result,
    )
