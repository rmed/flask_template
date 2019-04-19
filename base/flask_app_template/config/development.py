"""Development configuration."""
import os

SECRET_KEY = "potato"
DEBUG = True
TESTING = True

# Database path
SQLALCHEMY_DATABASE_URI = "sqlite:////%s" % os.path.join(os.getcwd(), "testdb.sqlite")

# Debug toolbar
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Site name
SITENAME = 'flask_app_template'

# Items per page in pagination
PAGE_ITEMS = 10

# Hashids
HASHIDS_SALT = 'hashedpotatoes'
HASHIDS_LENGTH = 8

# Flask-User
USER_APP_NAME = SITENAME

# Flask-Mail
MAIL_SERVER = "localhost"
MAIL_PORT = 25
MAIL_USE_SSL = False
MAIL_USE_TLS = False
MAIL_DEFAULT_SENDER = ""
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
