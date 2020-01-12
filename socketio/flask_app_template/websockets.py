# -*- coding: utf-8 -*-

"""WebSocket endpoints."""

import functools

from flask import request
from flask_login import current_user
from flask_socketio import disconnect
from flask_wtf.csrf import validate_csrf

from flask_app_template import socketio


def ws_authenticated(f):
    """Decorator to require login when connecting to WebSocket endpoints."""
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()

        else:
            return f(*args, **kwargs)

    return wrapped


@socketio.on('connect')
@ws_authenticated
def conn_proxy():
    """Only allow logged in users to connect."""
    # Check for CSRF token before allowing connection
    token = request.args.get('token')

    try:
        validate_csrf(token)

    except:
        # Simply disconnect the user
        disconnect()
