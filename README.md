# Startup guide

To run it, use docker!

```bash
docker compose up
```

# API documentation

this application consists of 2 endpoints:

1. /calculate_pi (requires parameter "n", defining amount
of decimals to count from)

Starts a celery task for calculation of n numbers of pi; declines previous task (if uncompleted) on adressing
2. /check_progress - provides information about progress of ordered calculation. <br> Response format (JSON):

```json
{
  "state": "FINISHED", // defines state of calculation; can take one of two possible values - "FINISHED" or "PROGRESS"
  "progress": 0.76,  // number between 0 and 1, defines percent of completed calculation
  "result": null  // represent result of calculation (pi with given accuracy); takes value null if calculation is in progress
}

```
