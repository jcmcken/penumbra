__version__ = '0.1.0'

import logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import penumbra.config as CONFIG

app = Flask(__name__)
app.config.from_object('penumbra.config')

_hdlr = logging.FileHandler(CONFIG.LOG_FILE)
_hdlr.setFormatter(logging.Formatter(CONFIG.LOG_FORMAT))
app.logger.addHandler(_hdlr)
app.logger.setLevel(CONFIG.LOG_LEVEL)

# Set up database using Flask-SQLAlchemy plugin
app.logger.debug('Initializing database engine')
db = SQLAlchemy(app)

# ensure various parts of the app get loaded
import penumbra.models
import penumbra.api
import penumbra.auth
