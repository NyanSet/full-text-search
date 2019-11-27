import functools
import re

from flask import request, Response

from src.utils.mongo_client import IndexDatabase
from src.utils.logger import Logger


def authorize(app_function):
    logger = Logger().get_logger('auth')

    @functools.wraps(app_function)
    def wrapper(*args, **kwargs):
        logger.info(request.headers)
        api_key = request.headers.get('api_key')
        if not api_key:
            logger.warning(f'Error 401.')
            return Response('API key was not specified.', status=401)

        symbols_correct = re.fullmatch(r'\w+', api_key)
        if not symbols_correct:
            logger.warning(f'Error 400.')
            return Response('Invalid API key format.', status=400)

        correct_key = IndexDatabase().validate_api_key(api_key)
        if not correct_key:
            logger.warning(f'Error 403.')
            return Response('User not found by provided API key.', status=403)

        return app_function(*args, **kwargs)

    return wrapper
