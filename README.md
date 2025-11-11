# Contents

- [About environment vairables](#environment-variables)
- [Startup guide](#startup-guide)
  - [Production mode](#production-mode)
  - [Development mode](#development-mode)
- [API documentation](#api-documentation)

## Environment variables

This application can be configured (to some measure) with environment 
variables; even though in production you generally don't need to change 
anything (everything is configured in Docker Compose), you may need it in [development process](#development-mode).

| Variable       | Desciption                                                                                                                                                               |
----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SESSION_SECRET | stores secret value for encoding session information; used only if RUN_MODE is set to DEV (and is required in this case).                                                |
| REDIS_HOST     | host for redis server (_optional_, considered localhost by default)                                                                                                      |
| REDIS_PORT     | port for redis server (_optional_, considered 6379 by default)                                                                                                           |
| RUN_MODE       | defines whether application is run in DEV mode or PROD mode. Any value but DEV (capital letter) is considered to be PROD. (_optional_, considered to be DEV by default)/ |

## Startup guide

There are two ways to start an application - dev mode 
(meaning no docker compose, hardcore "start redis/celery 
yourself" only) and production mode 

### Production mode
1. Provide session secret value for Docker Compose

To do that, create `session_secret.txt` file within project's root directory and enter secret value for sessions
(to get one you may, for example, use Linux's command `openssl rand -hex 32`).

2. Run docker compose

you can do it with following CLI command (executed from the project's root directory):
```bash
docker compose up
```

### Development mode
1. Create and fill in .env file in base directory

You are required to specify SESSION_SECRET variable, everything else is optional.

In case you will run redis on any server other than localhost, you may want to confgure REDIS_HOST and/or REDIS_PORT.
Full lise of variables may be seen [here](#environment-variables)

```text
REDIS_HOST=some_cool_host
SESSION_SECRET=extremely_secure_secret
```

3. Create venv and install dependencies

```bash
python3 -m venv venv
pip install -r requirements.txt 
```

3. run redis and celery

For that in separate CLI terminals run
```bash
redis-server
```
```bash
celery -A src.celery_tasks.c_app worker --loglevel=info
```

4. Run a fastapi dev server

for that from main directory run in your CLI (separate from those for redis and celery)

```bash
fastapi dev src/main.py
```

## API documentation

What are endpoints, what http methods they accept and what parameters they require may be seen in _**SwaggerUI**_ - check out the `/docs` endpoint.

This documentation focuses more on details and nuances of realisation that may be curious to future developers.

### Regarding `/calculate_pi`
This endpoint sets a celery task each time endpoint is reached; however, it also terminates task which is currently in
progress in case it is reached during the calculation. 

Tasks are attached to user sessions, so one user sending multiple requests for calculation will terminate his previous 
requests but will not affect requests of users with different session_id values.

### Regarding `/check_progress`
No words to be said, checks progress of calculation being stored in Redis.
