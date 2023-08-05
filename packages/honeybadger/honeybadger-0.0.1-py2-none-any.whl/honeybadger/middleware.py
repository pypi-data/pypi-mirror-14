from honeybadger import honeybadger

class DjangoHoneybadgerMiddleware(object):
    def __init__(self):
        from django.conf import settings
        if getattr(settings, 'DEBUG'):
            honeybadger.configure(environment='development')
        config_kwargs = dict([(k.lower(), v) for k, v in getattr(settings, 'HONEYBADGER', {}).items()])
        honeybadger.configure(**config_kwargs)
        honeybadger.config.set_12factor_config() # environment should override Django settings

    def process_request(self, request):
        honeybadger.begin_request(request)
        return None

    def process_exception(self, request, exception):
        honeybadger.notify(exception)
        return None

    def process_response(self, request, response):
        honeybadger.reset_context()
        return response

# TODO: finish Flask support
class FlaskHoneybadgerMiddleware(object):
    def __init__(self, app, **kwargs):
        raise NotImplemented
        # return app
