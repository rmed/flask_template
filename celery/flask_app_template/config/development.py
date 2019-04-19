# -*- coding: utf-8 -*-

# ...

# INCLUDE AFTER HASHIDS CONFIGURATION

# Celery
USE_CELERY = False
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
