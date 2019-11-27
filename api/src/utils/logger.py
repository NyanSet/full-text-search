import logging
import os

from logging.handlers import RotatingFileHandler

from src import config
from src.utils.wrappers.singleton import singleton


@singleton
class Logger:

    def __init__(self):
        log_dir = os.getenv('LOGS_PATH', config.LOGS['path'])
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)
        self._handler = RotatingFileHandler(os.path.join(log_dir, config.LOGS['filename']), maxBytes=10485760)  # 10 MB
        self._handler.setFormatter(logging.Formatter(config.LOGS['format']))

    def get_logger(self, name: str) -> logging:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(self._handler)
        return logger
