import multiprocessing as mp
import os

from collections import Counter, defaultdict

from src.utils.inverted_index.tokenizer import Tokenizer
from src.utils.logger import Logger


class InvertedIndexBuilder:

    def __init__(self, documents_dir):
        self._index = defaultdict(dict)
        self._tokenizer = Tokenizer()
        self.__logger = Logger().get_logger(__name__)

        if os.path.isdir(documents_dir):
            self._documents_dir = documents_dir
        else:
            self.__logger.error('Documents directory not found.')
            raise NotADirectoryError
        documents = os.listdir(documents_dir)
        self.total_docs_count = len(documents)

        self.__logger.info(f'Started building index of {self.total_docs_count} documents.')
        self._build(documents)

    def _build(self, documents):
        cpu_count = mp.cpu_count()
        pool = mp.Pool(cpu_count)
        batch = self.total_docs_count // cpu_count

        if batch == 0:
            self._index = self._process_documents(documents)
        else:
            for cpu in range(cpu_count):
                cpu_files = documents[cpu * batch :] if cpu == cpu_count - 1 else documents[cpu * batch : (cpu + 1) * batch]
                pool.apply_async(self._process_documents, args=(cpu_files, ), callback=lambda res: self._index_callback(res))
        pool.close()
        pool.join()

        if self._index:
            self.__logger.info(f'Built the index of {len(self._index)} words.')
        else:
            self.__logger.warning('Built empty index.')

    def _index_callback(self, result):
        for word in result:
            self._index[word].update(result[word])

    # reading documents, counting words' term frequency
    def _process_documents(self, files):
        result = defaultdict(dict)
        for doc in files:
            with open(os.path.join(self._documents_dir, doc), 'r') as inf:
                tokenized_text = self._tokenizer.tokenize(inf.read())
                doc_bag = Counter(tokenized_text)
                for word in doc_bag:
                    result[word].update({doc: doc_bag[word] / len(tokenized_text)})
        return result

    def get(self):
        return self._index
