# coding: utf-8
"""

kitten python web-framework

"""

class Router(object):
    """WSGI middleware for routing

    @Router
    def application(environ, start_request):
        pass

    @application.route('/index')
    def index():
        pass

    """
    def __init__(self, application):
        self.entry = application
        self.apps = {}

    def route(self, path):
        def decorator(f):
            self.apps[path] = f
            return f

        return decorator

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')

        app = self.apps.get(path, None)
        app = app or self.apps.get('default', None)
        self.app = app

        return self.entry(environ, start_response)

    def call(self, *args, **kwargs):
        if not self.app:
            return None
        return self.app(*args, **kwargs)

class PostData(object):
    """WSGI middleware for parsing POST data

    app = PostData(app)

    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if environ['REQUEST_METHOD'].upper() != "POST":
            return self.app(environ, start_response)

        try:
            body_size = int(environ.get('CONTENT_LENGTH', 0))
        except(ValueError):
            body_size = 0
        body = environ['wsgi.input'].read(body_size)

        from cgi import parse_qs
        data = parse_qs(body)
        for k in data.keys():
            data[k] = ', '.join(data[k])

        environ['POST_DATA'] = data
        return self.app(environ, start_response)
