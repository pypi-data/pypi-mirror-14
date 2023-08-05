from .messages import Notification
from .messages import Request


class Middleware(object):

    def process_message(self, message):
        if isinstance(message, Notification):
            return self.process_notification(message)
        if isinstance(message, Request):
            return self.process_request(message)

    def process_notification(self, request):
        pass

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass

    def process_exception(self, request, exception):
        pass


class MiddlewareStack(object):

    def __init__(self, middlewares):
        self.middlewares = middlewares or []

    def process_message(self, message):
        for middleware in self.middlewares:
            response = middleware.process_message(message)
            if response is not None:
                return response

    def process_response(self, message, response):
        for middleware in reversed(self.middlewares):
            response = middleware.process_response(message, response)
            if response is not None:
                return response

    def process_exception(self, message, exception):
        for middleware in reversed(self.middlewares):
            response = middleware.process_exception(message, exception)
            if response is not None:
                return response


class MiddlewareAwareRpcHandler(object):

    def __init__(self, handler, middleware):
        self.handler = handler
        self.middleware = middleware

    def __call__(self, request):
        self.middleware.process_message(request)
        try:
            response = self.handler(request)
        except Exception as e:
            middleware_response = self.middleware.process_exception(request, e)
            if middleware_response is not None:
                return middleware_response
            raise
        else:
            middleware_response = self.middleware.process_response(request, response)
            if middleware_response is not None:
                return middleware_response
            return response
