import os

from src import config
from src.utils import IndexDatabase, InvertedIndexBuilder, Logger


if __name__ == '__main__':
    logger = Logger().get_logger(__name__)
    doc_dir = os.getenv('DOCUMENTS_PATH', config.DOCUMENTS_PATH)

    try:
        index = InvertedIndexBuilder(doc_dir)
    except Exception:
        logger.exception('Error building index.')
    else:
        IndexDatabase().write_index(index.get(), index.total_docs_count)
