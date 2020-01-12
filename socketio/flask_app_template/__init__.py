# -*- coding: utf-8 -*-

# INCLUDE IN THE IMPORTS SECTION

from flask_socketio import SocketIO

# ...

# INCLUDE BEFORE init_app()
# Flask-SocketIO
socketio = SocketIO()


def init_app():
    # ...

    # INCLUDE BEFORE DB INITIALIZATION

    # Setup SocketIO
    socketio.init_app(
        app,
        message_queue=app.config.get('ENGINEIO_MESSAGE_QUEUE')
    )

    # Force endpoint registration
    from flask_app_template import websockets


    # MODIFY JS BUNDLE
    js_bundle = Bundle(
        # AFTER ZEPTO
        'js/vendor/socket.io.js', # 2.2.0
        # ...
    )