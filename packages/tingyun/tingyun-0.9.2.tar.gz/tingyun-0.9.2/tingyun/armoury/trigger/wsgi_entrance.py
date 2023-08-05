
"""define the trigger for the specified weapon

"""

import logging
import sys

from tingyun.logistics.basic_wrapper import wrap_object, FunctionWrapper
from tingyun.logistics.object_name import callable_name
from tingyun.armoury.ammunition.function_tracker import FunctionTracker, function_trace_wrapper
from tingyun.armoury.ammunition.tracker import current_tracker
from tingyun.battlefield.tracer import Tracer
from tingyun.battlefield.proxy import proxy_instance
from tingyun.armoury.trigger.browser_rum import TingYunWSGIBrowserRumMiddleware
from tingyun.armoury.trigger.cross_trace import process_header


console = logging.getLogger(__name__)


class WSGIApplicationResponse(object):

    def __init__(self, tracer, generator):
        self.tracer = tracer
        self.generator = generator

    def __iter__(self):

        try:
            with FunctionTracker(self.tracer, name='Response', group='Python.WSGI'):
                for item in self.generator:
                    yield item
        except GeneratorExit:
            raise
        except:  # Catch all
            self.tracer.record_exception(*sys.exc_info())
            raise

    def close(self):
        """Server/gateway will call this close method to indicate that the task for tracing the request finished.
        :return:
        """

        try:
            if hasattr(self.generator, 'close'):
                self.generator.close()
        except:  # Catch all
            self.tracer.finish_work(*sys.exc_info())
            raise
        else:
            self.tracer.finish_work(None, None, None)


def wsgi_wrapper_inline(wrapped, framework="Python", version=None):
    """ wrap the uwsgi application entrance
    :param wrapped: the method need to be wrapped
    :param framework: framework of current used web framework
    :param version: version of current used web framework
    :return:
    """
    console.info("wrap the wsgi entrance with framework(%s), version(%s)", framework, version)

    def wrapper(wrapped, instance, args, kwargs):
        """More detail about the argument, read the wrapper doc
        """
        tracker = current_tracker()
        if tracker:
            return wrapped(*args, **kwargs)

        def wsgi_args(environ, start_response, *args, **kwargs):
            return environ, start_response

        environ, start_response = wsgi_args(*args, **kwargs)
        tracker = Tracer(proxy_instance(), environ, framework)
        tracker.start_work()

        # respect the wsgi protocol
        def _start_response(status, response_headers, *args):
            # deal the response header/data
            process_header(tracker, response_headers)
            tracker.deal_response(status, response_headers, *args)
            _write = start_response(status, response_headers, *args)

            return _write

        result = []
        try:
            tracker.set_tracker_name(callable_name(wrapped), priority=1)
            application = function_trace_wrapper(wrapped)
            with FunctionTracker(tracker, name='Application', group='Python.WSGI'):
                result = TingYunWSGIBrowserRumMiddleware(tracker, application, _start_response, environ)()
                # result = application(environ, start_response)
        except:
            tracker.finish_work(*sys.exc_info())
            raise

        return WSGIApplicationResponse(tracker, result)

    return FunctionWrapper(wrapped, wrapper)


def wsgi_application_wrapper(module, object_path, *args):
    """
    :param module:
    :param object_path:
    :return:
    """
    wrap_object(module, object_path, wsgi_wrapper_inline, *args)


def wsgi_application_decorator(framework='xx', version='xx'):
    """
    :param framework: the framework of current use.
    :return:
    """
    framework = 'xx' if framework is None else framework
    version = 'xx' if version is None else version

    def decorator(wrapped):
        """
        :param wrapped:
        :return:
        """
        return wsgi_wrapper_inline(wrapped, framework, version)

    return decorator


wsgi_app_wrapper_entrance = wsgi_wrapper_inline
