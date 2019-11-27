import json

from flask import request, Response
from flask.views import MethodView

from src.utils import authorize, InvertedIndex, Logger


class SearchHTTPHandler(MethodView):

    def __init__(self):
        self._empty_query_msg = 'Empty search query.'
        self._invalid_result_size_msg = 'Invalid result size.'

        self.__index = InvertedIndex()
        self.__logger = Logger().get_logger(__name__)

    @authorize
    def get(self):
        search_query = request.args.get('query')
        if not isinstance(search_query, str):
            self.__logger.error(self._empty_query_msg)
            return Response(self._empty_query_msg, status=400)

        result_size = request.args.get('result_size', 1)
        try:
            result_size = int(result_size)
            assert result_size > 0
        except Exception:
            self.__logger.error(self._invalid_result_size_msg)
            return Response(self._invalid_result_size_msg, status=400)

        try:
            result = self.__index.search(search_query, result_size)
        except Exception:
            self.__logger.exception('Error during search.')
            return Response(status=500)

        if result is None:
            return Response(self._empty_query_msg, status=400)
        if not result:
            return Response('Nothing found.', status=200)
        return Response(json.dumps(result, ensure_ascii=False).encode('utf8'), status=200)
