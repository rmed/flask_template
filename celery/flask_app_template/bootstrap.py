# -*- coding: utf-8 -*-

# ...

# INCLUDE AFTER HASHIDS WRAPPER
class CeleryWrapper(object):
    """Wrapper for deferred initialization of Celery."""

    def __init__(self):
        self._celery = None
        self.task = None

    def __getattr__(self, attr):
        """Wrap internal celery attributes."""
        if attr == 'make_celery':
            return getattr(self, attr)

        return getattr(self._celery, attr)

    def make_celery(self, app):
        """Create a celery instance for the application.
        Args:
            app: Application instance
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
