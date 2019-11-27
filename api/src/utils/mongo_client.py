import os

from pymongo import MongoClient

from src import config
from src.utils.logger import Logger
from src.utils.wrappers.singleton import singleton


@singleton
class IndexDatabase:
    def __init__(self):
        db = MongoClient(host=os.getenv('MONGO_HOST', config.MONGO['host']),
                         port=int(os.getenv('MONGO_PORT', config.MONGO['port']))).inverted_index
        self._constants = db.constants
        self._index = db.index
        self._userdata = db.userdata
        self.__logger = Logger().get_logger(__name__)

    def get(self, word, doc=None):
        query = self._index.find_one({word: {'$exists': True}})
        if query is not None:
            return query[word] if doc is None else query[word][doc]
        else:
            self.__logger.error(f'No such word: {word}')
            raise KeyError

    def get_constant(self, name):
        query = self._constants.find_one({name: {'$exists': True}})
        if query is not None:
            return query[name]
        else:
            self.__logger.error(f'No such constant: {name}')
            raise KeyError

    def get_words_list(self):
        return [list(word.keys())[0] for word in self._index.find({}, {'_id': 0})]

    def write_index(self, index, total_docs_count):
        try:
            self._constants.drop()
            self._index.drop()
            self._constants.insert_one({'total_docs_count': total_docs_count})
            for word in index:
                self._index.insert({word: index[word]}, check_keys=False)
        except Exception:
            self.__logger.exception('Error writing index to the database.')

    def insert_api_keys(self, tokens):
        for token in tokens:
            self._userdata.update({'api_key': token}, {"$set": {'api_key': token}}, upsert=True)

    def validate_api_key(self, key):
        return self._userdata.find_one({'api_key': key}) is not None
