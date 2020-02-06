import logging
from logging.handlers import RotatingFileHandler


def set_up_logging(app):
    handler = RotatingFileHandler(app.config['log_file'], maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)