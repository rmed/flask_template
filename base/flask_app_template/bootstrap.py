# -*- coding: utf-8 -*-

"""This file contains miscelaneous bootstrapping code."""

from flask_babel import lazy_gettext as _l
from hashids import Hashids


# Available locales
LANGUAGES = ['en', 'es']
LANGUAGES_LOCALIZED = [_l('English'), _l('Spanish')]


# Static configuration values
BASE_CONFIG = {
    # Localization
    'BABEL_DEFAULT_LOCALE': 'en',
    'BABEL_DEFAULT_TIMEZONE': 'UTC',

    # Flask-SQLAlchemy
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,

    # Flask-User
    'USER_APP_NAME': 'flask_app_template',
    'USER_ENABLE_EMAIL': True,
    'USER_ENABLE_FORGOT_PASSWORD': True,
    # 'USER_ENABLE_INVITATION': True,
    'USER_INVITE_EXPIRATION': 7*24*3600, # One week
    # 'USER_REQUIRE_INVITATION': True,
    'USER_REQUIRE_RETYPE_PASSWORD': True,

    'USER_CHANGE_PASSWORD_TEMPLATE': 'extensions/flask_user/change_password.html',
    'USER_FORGOT_PASSWORD_TEMPLATE': 'extensions/flask_user/forgot_password.html',
    'USER_INVITE_TEMPLATE': 'extensions/flask_user/invite.html',
    'USER_INVITE_ACCEPT_TEMPLATE': 'extensions/flask_user/register.html',
    'USER_LOGIN_TEMPLATE': 'extensions/flask_user/login.html',
    'USER_REGISTER_TEMPLATE': 'extensions/flask_user/register.html',
    'USER_RESET_PASSWORD_TEMPLATE': 'extensions/flask_user/reset_password.html',

    'USER_CONFIRM_EMAIL_EMAIL_TEMPLATE': 'extensions/flask_user/emails/confirm_email',
    'USER_FORGOT_PASSWORD_EMAIL_TEMPLATE': 'extensions/flask_user/emails/forgot_password',
    'USER_INVITE_EMAIL_TEMPLATE': 'extensions/flask_user/emails/invite',
    'USER_PASSWORD_CHANGED_EMAIL_TEMPLATE': 'extensions/flask_user/emails/password_changed',
    'USER_REGISTERED_EMAIL_TEMPLATE': 'extensions/flask_user/emails/registered',
    'USER_USERNAME_CHANGED_EMAIL_TEMPLATE': 'extensions/flask_user/emails/username_changed',


    'USER_CHANGE_PASSWORD_URL': '/profile/change-password',
    # 'USER_EMAIL_ACTION_URL': '/dashboard/users/email/<id>/<action>',
    'USER_FORGOT_PASSWORD_URL': '/forgot-password',
    # 'USER_INVITE_URL': '/profile/invite-user',
    'USER_LOGIN_URL': '/login',
    'USER_LOGOUT_URL': '/logout',
    'USER_REGISTER_URL': '/register',
    'USER_RESET_PASSWORD_URL': '/reset-password/<token>',

    # 'USER_AFTER_CHANGE_PASSWORD_ENDPOINT': 'profile.show_profile',
    'USER_AFTER_FORGOT_PASSWORD_ENDPOINT': 'user.forgot_password',
    # 'USER_AFTER_LOGIN_ENDPOINT': 'general.home',
    # 'USER_INVITE_ENDPOINT': 'profile.invite',
    'USER_AFTER_RESET_PASSWORD_ENDPOINT': 'general.home',
    'USER_UNAUTHORIZED_ENDPOINT': 'general.home',

    'USER_PASSWORD_HASH': 'sha512_crypt',

    # Cookie notice
    'COOKIE_NOTICE': True,

    # Default number of items per page
    'PAGE_ITEMS': 50,

    'LANGUAGES': LANGUAGES
}


class HashidsWrapper(object):
    """Wrapper for deferred initialization of Hashids."""

    def __init__(self):
        self._hasher = None

    def __getattr__(self, attr):
        """Wrap internal Hashids attributes."""
        if attr == 'init_hasher':
            return getattr(self, attr)

        return getattr(self._hasher, attr)

    def init_hasher(self, app):
        """Create a Hashids instance for the application.

        Args:
            app: Application instance
        """
        self._hasher = Hashids(
            salt=app.config['HASHIDS_SALT'],
            min_length=app.config.get('HASHIDS_LENGTH', 8)
        )
