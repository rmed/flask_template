# Websocket support with Flask-SocketIO

This *recipe* adds websocket support to the application through [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/).

When a new websocket connection is established, the client sends a CSRF token to the backend. If this token is not valid, the server will not allow the connection and immediately disconnect the user.
