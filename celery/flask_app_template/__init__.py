# -*- coding: utf-8 -*-

# INCLUDE IN THE IMPORTS SECTION

from flask_app_template.util import CeleryWrapper

# ...

# INCLUDE BEFORE init_app()
celery = CeleryWrapper()


def init_app():
    # ...

    # INCLUDE AFTER FLASK-LOGIN INITIALIZATION

    # Enable Celery support (optional)
    if app.config.get('USE_CELERY', False):
        celery.make_celery(app)

        # Import tasks
        from flask_app_template.async_tasks import async_mail
