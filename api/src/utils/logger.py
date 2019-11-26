import logging
import os

from logging.handlers import RotatingFileHandler
from src import config


def singleton(_class):
    instances = {}

    def getinstance(*args, **kwargs):
        if _class not in instances:
            instances[_class] = _class(*args, **kwargs)
        return instances[_class]

    return getinstance


@singleton
class Logger:

    def __init__(self):
        if not os.path.isdir(config.LOG_DIR):
            os.mkdir(config.LOG_DIR)
        log_file = os.path.join(config.LOG_DIR, config.LOG_FILE)
        formatter = logging.Formatter(config.LOG_FORMAT)
        self._handler = RotatingFileHandler(log_file, maxBytes=10485760)  # 10 MB
        self._handler.setFormatter(formatter)

    def get_logger(self, name: str) -> logging:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(self._handler)
        return logger
