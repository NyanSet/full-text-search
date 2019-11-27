import functools
import re

from flask import request

from src.utils.mongo_client import IndexDatabase
from src.utils.logger import Logger


logger = Logger().get_logger('auth')


def authorize(app_function):
    @functools.wraps(app_function)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('api-key')

        if not api_key:
            logger.warning(f'Error 401.')
            return utils.json_response(401, 'Api-key was not specified.')

        symbols_correct = re.fullmatch(r'\w+', api_key)

        if not symbols_correct:
            logger.warning(f'Error 400.')
            return utils.json_response(400, 'Invalid api-key format.')

        correct_key = IndexDatabase().validate_api_key(api_key)

        if not correct_key:
            logger.warning(f'Error 403.')
            return utils.json_response(403, 'User not found by provided api-key.')

        return app_function(*args, **kwargs)
    return wrapper
