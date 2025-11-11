import os
from pathlib import Path

from dotenv import load_dotenv

base_dir = Path(__file__).resolve().parent.parent
env_path = os.path.join(base_dir, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

BROKER_HOST = os.getenv("REDIS_HOST", "localhost")
BROKER_PORT = int(os.getenv("REDIS_PORT", 6379))
RUN_MODE = os.getenv("IS_DEV", "DEV")

if RUN_MODE == "DEV":
    SESSION_SECRET = os.getenv("SESSION_SECRET")
    if SESSION_SECRET is None:
        raise KeyError("SESSION_SECRET environment variable not configured! "
              "Terminating program...")
else:
    secret_fpath = os.path.join(base_dir, "/run/secrets/session_secret")
    if not os.path.exists(secret_fpath):
        raise KeyError("session_secret Docker secret is missing")
    SESSION_SECRET = open(secret_fpath).read().rstrip("\n")
