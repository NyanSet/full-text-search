from src.http_handlers import SearchHTTPHandler


class Router:
    @staticmethod
    def apply_routes(app):
        app.add_url_rule('/', 'search',
                         view_func=SearchHTTPHandler.as_view('search'),
                         methods=['GET'])
        return app
