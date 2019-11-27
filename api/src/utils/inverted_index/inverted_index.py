import math

from collections import defaultdict

from src.utils.inverted_index.tokenizer import Tokenizer
from src.utils.logger import Logger
from src.utils.mongo_client import IndexDatabase


class InvertedIndex:

    def __init__(self):
        self._db = IndexDatabase()
        self._tokenizer = Tokenizer()
        self.__logger = Logger().get_logger(__name__)

    def calculate_relevance(self, request):
        scores = defaultdict(float)
        for target_word in request:
            target_docs = self._db.get(target_word).keys()
            for doc in target_docs:
                idf = math.log(self._db.get_constant('total_docs_count') / len(target_docs))
                scores[doc] += self._db.get(target_word, doc) * abs(idf) / len(request)
        return scores

    def search(self, request, result_size):
        parsed_request = self._tokenizer.tokenize(request)
        if not parsed_request:
            self.__logger.error('Empty search request.')
            return None

        target_request = [word for word in parsed_request if word in self._db.get_words_list()]
        relevance = self.calculate_relevance(target_request)
        return sorted(relevance.items(), key=lambda item: item[1], reverse = True)[:result_size]
