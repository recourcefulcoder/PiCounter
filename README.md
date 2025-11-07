# Startup guide

To run it, use docker!

```bash
docker compose up
```

# API documentation

What are endpoints, what http methods they accept and what parameters they requiremay be seen in _**SwaggerUI**_ - check out the `/docs` endpoint.

This documentation focuses more on details and nuances of realisation that may be curious to future developers.

### Regarding `/calculate_pi`
This endpoint sets a celery task each time endpoint is reached; however, it also terminates task which is currently in
progress in case it is reached during the calculation.

### Regarding `/check_progress`
No words to be said, checks progress of calculation being stored in Redis.
