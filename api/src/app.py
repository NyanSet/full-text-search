from flask import Flask

from src import config
from src.utils import InvertedIndex, Logger, Router


app = Router().apply_routes(Flask(config.API['name']))

if __name__ == '__main__':
    logger = Logger().get_logger(__name__)

    try:
        InvertedIndex().build(config.DOCUMENTS_DIR)
    except Exception:
        logger.exception('Error building index.')
        exit(1)

    app.run(debug=False, host=config.API['host'], port=config.API['port'])
