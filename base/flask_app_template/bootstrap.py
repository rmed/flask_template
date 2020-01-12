# -*- coding: utf-8 -*-

"""This file contains miscelaneous bootstrapping code."""

import os

from flask_babel import lazy_gettext as _l


# Available locales
LANGUAGES = ('en', 'es')
LANGUAGES_LOCALIZED = (_l('English'), _l('Spanish'))


# Static configuration values
BASE_CONFIG = {
    # Localization
    'BABEL_DEFAULT_LOCALE': 'en',
    'BABEL_DEFAULT_TIMEZONE': 'UTC',

    # Flask-SQLAlchemy
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,

    # Flask-Login
    'SESSION_PROTECTION': 'strong',

    # Passlib
    'PASSLIB_SCHEMES': ['bcrypt'],
    'PASSLIB_ALG_BCRYPT_ROUNDS': 14,

    'LANGUAGES': LANGUAGES
}


# Development defaults applied on top of BASE_CONFIG if no configuration
# is specified
DEV_CONFIG = {
    'SECRET_KEY': 'potato',
    'DEBUG': True,
    'TESTING': True,

    # Database path
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////{}'.format(os.path.join(os.getcwd(), "testdb.sqlite")),

    # Debug toolbar
    'DEBUG_TB_INTERCEPT_REDIRECTS': False,

    # Site name
    'SITENAME': 'flask_app_template',

    # Items per page in pagination
    'PAGE_ITEMS': 10,

    # Hashids
    'HASHIDS_SALT': 'hashedpotatoes',
    # Minimum length
    'HASHIDS_LENGTH': 8,

    # Flask-Mail
    'MAIL_SERVER': 'localhost',
    'MAIL_PORT': 25,
    'MAIL_USE_SSL': False,
    'MAIL_USE_TLS': False,
    'MAIL_DEFAULT_SENDER': '',
    'MAIL_USERNAME': '',
    'MAIL_PASSWORD': ''
}
