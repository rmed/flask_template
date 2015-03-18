from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

# Load default configuration
app.config.from_object('config.default')

# Load configuration from instance folder
app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')

# Setup database
db = SQLAlchemy(app)

# Blueprints
# from .views.MYVIEW import VIEW
# app.register_blueprint(VIEW, url_prefix='/URL')
