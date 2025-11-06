# Startup guide

At the moment docker isn't implemented, so all sources should be run manually.

1. Run redis server 
```bash
sudo service redis-sevrer start  
```
2. Start celery worker

```bash
celery -A src.celery_tasks.c_app worker --loglevel=info
```

3. Start a fastapi application

```bash
cd src
fastapi dev main.py
```

# API documentation

--
