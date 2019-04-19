# -*- coding: utf-8 -*-

"""This file contains celery tasks."""


from flask_mail import Message
from flask_user.emails import send_email

from flask_app_template import celery, mail


@celery.task()
def async_user_mail(*args):
    """Send Flask-User emails asynchronously."""
    send_email(*args)


@celery.task()
def async_mail(*args, **kwargs):
    """Send Flask-Mail emails asynchronously."""
    message = Message(*args, **kwargs)
    mail.send(message)
