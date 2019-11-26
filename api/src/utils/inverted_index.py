import math
import multiprocessing as mp
import os
import pymorphy2

from src.utils.logger import Logger
from collections import Counter, defaultdict


class InvertedIndex:

    _index = defaultdict(dict)

    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()
        self._meaningless_lexemes = ['CONJ', 'PREP', None]  # conjunctions, prepositions, empty words
        self.__logger = Logger().get_logger(__name__)

    def _tokenize_text(self, text):
        # splitting the text into words, removing punctuations, transforming to normal form, removing unwanted words
        result = []
        for word in text.replace('\n', ' ').split(' '):
            parsed_word = self._morph.parse(''.join(filter(str.isalpha, word)))[0]
            if parsed_word.tag.POS not in self._meaningless_lexemes:
                result.append(parsed_word.normal_form)
        return result

    def _process_documents(self, documents_dir, files):
        result = defaultdict(dict)
        for doc in files:
            with open(os.path.join(documents_dir, doc), 'r') as inf:
                tokenized_text = self._tokenize_text(inf.read())
                doc_bag = Counter(tokenized_text)
                for word in doc_bag:
                    result[word].update({doc: doc_bag[word] / len(tokenized_text)})
        return result

    @staticmethod
    def _index_callback(result):
        for word in result:
            InvertedIndex._index[word].update(result[word])

    def build(self, documents_dir):
        if not os.path.isdir(documents_dir):
            self.__logger.error('The documents directory not found.')
            raise NotADirectoryError

        cpu_count = mp.cpu_count()
        pool = mp.Pool(cpu_count)
        files = os.listdir(documents_dir)
        batch = len(files) // cpu_count

        if batch == 0:
            InvertedIndex._index = self._process_documents(documents_dir, files)
        else:
            for cpu in range(cpu_count):
                cpu_files = files[cpu * batch :] if cpu == cpu_count - 1 else files[cpu * batch : (cpu + 1) * batch]
                pool.apply_async(self._process_documents, args=(documents_dir, cpu_files),
                                 callback=lambda res: self._index_callback(res))
        pool.close()
        pool.join()

        if InvertedIndex._index:
            self.__logger.info(f'Built the index of {len(InvertedIndex._index)} words.')
        else:
            self.__logger.warning('Built empty index.')

    @staticmethod
    def calculate_relevance(request, all_docs_count):
        scores = defaultdict(float)
        for target_word in request:
            target_docs = InvertedIndex._index[target_word].keys()
            for doc in target_docs:
                idf = math.log(all_docs_count / len(target_docs))
                scores[doc] += InvertedIndex._index[target_word][doc] * abs(idf) / len(request)
        return scores

    def search(self, request, result_size):
        parsed_request = self._tokenize_text(request)
        if not parsed_request:
            self.__logger.error('Empty search request.')
            return None

        target_request = [word for word in parsed_request if word in InvertedIndex._index.keys()]
        all_docs_count = len(set().union(*[InvertedIndex._index[word].keys() for word in InvertedIndex._index]))
        relevance = self.calculate_relevance(target_request, all_docs_count)

        return sorted(relevance.items(), key=lambda item: item[1], reverse = True)[:result_size]
