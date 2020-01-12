"""Run the application inside SocketIO server."""

from flask_app_template import socketio, init_app

if __name__ == '__main__':
    app = init_app()
    socketio.run(app)