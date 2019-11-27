import os

from flask import Flask

from src import config
from src.utils import Router


app = Router().apply_routes(Flask(config.API['name']))

if __name__ == '__main__':
    app.run(debug=False,
            host=os.getenv('API_HOST', config.API['host']),
            port=int(os.getenv('API_PORT', config.API['port'])))
