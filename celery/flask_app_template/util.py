# -*- coding: utf-8 -*-

# ...

# INCLUDE AT THE END OF THE FILE
class CeleryWrapper(object):
    """Wrapper for deferred initialization of Celery.

    The wrapper expects the following configuration parameters:

    - `CELERY_RESULT_BACKEND`: URL to the backend used for obtaining results.
    - `CELERY_BROKER_URL`: URL to the broker.
    """

    def __init__(self):
        self._celery = None
        self.task = None

    def __getattr__(self, attr):
        """Wrap internal celery attributes."""
        if attr == 'init_app':
            return getattr(self, attr)

        return getattr(self._celery, attr)

    def init_app(self, app):
        """Create a celery instance for the application.

        Args:
            app: Application instance.

        Raises:
            `KeyError` in case a configuration parameter is missing.
        """
        # Celery is optional, import it here rather than globally
        from celery import Celery

        celery_instance = Celery(
            app.import_name,
            backend=app.config['CELERY_RESULT_BACKEND'],
            broker=app.config['CELERY_BROKER_URL']
        )

        celery_instance.conf.update(app.config)
        TaskBase = celery_instance.Task

        class ContextTask(TaskBase):
            abstract = True
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery_instance.Task = ContextTask

        self._celery = celery_instance
        self.task = self._celery.task
