# -*- coding: utf-8 -*-

# ...

# INCLUDE AT THE END OF THE FILE

# Celery
USE_CELERY = False
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
