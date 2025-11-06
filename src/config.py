import os
from pathlib import Path
from dotenv import load_dotenv


base_dir = Path(__file__).resolve().parent
env_path = os.path.join(base_dir, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

broker_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
