import os
from pathlib import Path

from dotenv import load_dotenv


base_dir = Path(__file__).resolve().parent
env_path = os.path.join(base_dir, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

BROKER_HOST = os.getenv("REDIS_HOST", "localhost")
BROKER_PORT = int(os.getenv("REDIS_PORT", 6379))
