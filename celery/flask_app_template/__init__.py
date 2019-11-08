# -*- coding: utf-8 -*-

# INCLUDE IN THE IMPORTS SECTION
from flask_user.emails import send_email

from flask_app_template.bootstrap import CeleryWrapper

# ...

# INCLUDE BEFORE init_app()
celery = CeleryWrapper()


def init_app():
    # ...

    # INCLUDE REPLACING FLASK-USER INITIALIZATION

    # Enable Celery support (optional)
    if app.config.get('USE_CELERY', False):
        celery.make_celery(app)

        # Import tasks
        from flask_app_template.tasks import async_user_mail, async_mail

    # Setup Flask-User
    def _send_user_mail(*args):
        """Specify the function for sending mails in Flask-User.

        If celery has been initialized, this will be asynchronous. Defaults to
        the original function used by Flask-User.
        """
        if app.config.get('USE_CELERY', False):
            # Asynchronous
            async_user_mail.delay(*args)

        else:
            # Synchronous
            send_email(*args)


    user_db_adapter = SQLALchemyAdapter(db, models.User)
    user_manager.init_app(
        app,
        db_adapter=user_db_adapter,
        send_email_function=_send_user_mail
    )
