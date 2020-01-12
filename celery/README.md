# Asynchronous tasks with Celery

This *recipe* adds asynchronous tasks with Celery and Redis. An example of asynchronous delivery of emails is provided.

This *recipe* supports conditional initialization of Celery tasks (note that the celery workers must be started externally, such as through `uWSGI` or `supervisord`).


## Configuration

The *recipe* requires both `celery` and `redis` modules installed in the environment (use `requirements.txt`). In your **production** configuration write the following lines:

```python
USE_CELERY = True
CELERY_BROKER_URL = "redis://localhost:6379/N"
CELERY_RESULT_BACKEND = "redis://localhost:6379/N"
```

Where `N` is the database number from 0 to 15 (can be extended in Redis configuration). Make sure the database does not cause conflict with other applications using the same redis instance Redis.