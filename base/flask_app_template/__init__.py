# -*- coding: utf-8 -*-

"""This file contains initialization code."""

import os

from babel import dates as babel_dates
from flask import Flask, render_template, request
from flask_assets import Environment, Bundle
from flask_babel import Babel
from flask_mail import Mail
from flask_migrate import Migrate
from flask_misaka import Misaka
from flask_sqlalchemy import SQLAlchemy
from flask_user import SQLAlchemyAdapter, UserManager, current_user
from flask_wtf.csrf import CSRFProtect

import flask
import pytz
import webassets

from flask_app_template.bootstrap import BASE_CONFIG, LANGUAGES, HashidsWrapper
from flask_app_template.errors import forbidden, page_not_found, server_error

__version__ = '0.1.0'


# Debug toolbar (for development)
try:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension()

    _USING_TOOLBAR = True

except ImportError:
    _USING_TOOLBAR = False


# Hashids
hashids_hasher = HashidsWrapper()

# Babel
babel = Babel()

# CSRF
csrf = CSRFProtect()

# SQLAlchemy
db = SQLAlchemy()

# Flask-Migrate
migrate = Migrate()

# Flask-Mail
mail = Mail()

# Flask-User
user_manager = UserManager()

# Flask-Misaka
md = Misaka(
    fenced_code=False,
    underline=True,
    no_intra_emphasis=False,
    strikethrough=True,
    superscript=True,
    tables=True,
    no_html=True,
    escape=True
)

# Flask-Assets
assets = Environment()


@babel.localeselector
def get_locale():
    """Get locale from user record or from browser locale."""
    if not current_user or not current_user.is_authenticated:
        # Not logged in user
        return request.accept_languages.best_match(LANGUAGES)

    return current_user.locale


def url_for_self(**kwargs):
    """Helper to return current endpoint in Jinja template."""
    return flask.url_for(
        flask.request.endpoint,
        **dict(flask.request.view_args, **kwargs)
    )


def format_datetime(value):
    """Jinja filter to format datetime using user defined timezone.

    If not a valid timezone, defaults to UTC.

    Args:
        value (datetime): Datetime object to represent.
    """
    user_tz = current_user.timezone

    if not user_tz or user_tz not in pytz.common_timezones:
        user_tz = 'UTC'

    tz = babel_dates.get_timezone(user_tz)

    return babel_dates.format_datetime(
        value,
        'yyyy-MM-dd HH:mm:ss',
        tzinfo=tz
    )


def init_app():
    """Initialize app."""
    app = Flask(__name__)
    app.config.update(BASE_CONFIG)

    # Load configuration specified in environment variable or default
    # development one.
    # Production configurations shold be stored in a separate directory, such
    # as `instance`.
    if 'FLASK_APP_CONFIG' in os.environ:
        app.config.from_envvar('FLASK_APP_CONFIG')

    else:
        app.config.from_object('flask_app_template.config.development')


    # Custom jinja helpers
    app.jinja_env.globals['url_for_self'] = url_for_self
    app.jinja_env.filters['datetime'] = format_datetime


    # Whitespacing Jinja
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True


    # Setup debug toolbar in development
    if app.config.get('DEBUG') and _USING_TOOLBAR:
        toolbar.init_app(app)


    # Setup Hashids
    hashids_hasher.init_hasher(app)


    # Setup localization
    babel.init_app(app)


    # Setup CSRF protection
    csrf.init_app(app)


    # Setup database
    db.init_app(app)
    # Force model registration
    from flask_app_template import models

    # Database migrations
    migrations_dir = os.path.join(app.root_path, 'migrations')
    migrate.init_app(app, db, migrations_dir)


    # Setup Flask-Mail
    mail.init_app(app)


    # Setup Flask-User
    user_db_adapter = SQLAlchemyAdapter(db, models.User)
    user_manager.init_app(app, db_adapter=user_db_adapter)


    # Setup Flask-Misaka
    md.init_app(app)


    # Setup Flask-Assets and bundles
    assets.init_app(app)
    libsass = webassets.filter.get_filter(
        'libsass',
        style='compressed'
    )

    scss_bundle = Bundle(
        'app.scss',
        depends='scss/custom.scss',
        filters=libsass
    )

    css_bundle = Bundle(
        scss_bundle,
        filters='cssmin',
        output='gen/packed.css'
    )

    js_bundle = Bundle(
        'js/vendor/zepto.min.js',
        'js/vendor/noty.min.js',
        'js/vendor/bulma-tagsinput.min.js',
        'js/navigation.js',
        'js/init.js',
        filters='rjsmin',
        output='gen/packed.js'
    )

    assets.register('css_pack', css_bundle)
    assets.register('js_pack', js_bundle)


    # Register blueprints
    from flask_app_template.views.general import bp_general

    app.register_blueprint(bp_general)


    # Custom commands
    from flask_app_template import commands


    # Custom error handlers
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)


    return app
