import os

from pymongo import MongoClient

from src import config
from src.utils.logger import Logger
from src.utils.singleton import singleton


@singleton
class IndexDatabase:
    def __init__(self):
        db = MongoClient(host=os.getenv('MONGO_HOST', config.MONGO['host']),
                         port=int(os.getenv('MONGO_PORT', config.MONGO['port']))).inverted_index
        self._constants = db.constants
        self._index = db.index
        self.__logger = Logger().get_logger(__name__)

    def get(self, word, doc=None):
        field = word if doc is None else f'{word}.{doc}'
        query = self._constants.find_one({}, {field: 1})
        if query is not None:
            return query[word] if doc is None else query[doc]
        else:
            self.__logger.error(f'No such field: {field}')
            raise KeyError

    def get_constant(self, name):
        constant_query = self._constants.find_one({}, {name: 1})
        if constant_query is not None:
            return constant_query[name]
        else:
            self.__logger.error(f'No such constant: {name}')
            raise KeyError

    def get_words_list(self):
        return list([index.keys() for index in self._index.find({}, {'_id': 0})][0])

    def write_index(self, index, total_docs_count):
        try:
            self._constants.drop()
            self._index.drop()
            self._constants.insert_one({'total_docs_count': total_docs_count})
            self._index.insert(index, check_keys=False)
        except Exception:
            self.__logger.exception('Error writing index to the database.')
