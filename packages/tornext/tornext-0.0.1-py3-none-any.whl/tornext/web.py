#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
# Copyright 2016 JZQT <tjy.jzqt@qq.com>

import importlib
from urllib.parse import urlencode

import tornado.web
from tornado.web import URLSpec, Application

from tornext.conf import Settings


class Tornext(object):
    """Tornext is used to replace ``tornado.web.Application``.

    Tornext encapsulates ``tornado.web.Application`` related operations.

    Typical usage::

        from tornext.web import Tornext, TornextRequestHandler

        app = Tornext()

        @app.route(r'/')
        class IndexHandler(TornextRequestHandler):
            def get(self):
                self.write('index')

        if __name__ == '__main__':
            app.settings.from_object({
                'TORNADO': {
                    'debug': True,
                    'static_path': 'static',
                    'template_path': 'templates',
                },
            })
            app.run(port=8888)

    ``tornext.web.Tornext`` is not subclass of ``tornado.web.Application``,
    but it has a property is a ``tornado.web.Application`` instance. This
    property access by ``.application``. Only when the web service is
    started ``.application`` will only be configured. Such as calls to
    ``.listen()`` and ``.run()`` these two methods.

    See ``tornado.web.Application`` for more information.
    """

    def __init__(self, routes=None, settings=None):
        self.routes.extend(routes or [])
        self.settings.from_object(settings or {})

    @property
    def settings(self):
        if not hasattr(self, '_settings'):
            self._settings = Settings()
            self._settings.from_object('tornext.conf.default_settings')
        return self._settings

    @property
    def application(self):
        if not hasattr(self, '_application'):
            self._application = None
        return self._application

    @property
    def routes(self):
        if not hasattr(self, '_routes'):
            self._routes = []
        return self._routes

    def route(self, pattern, kwargs=None, name=None):
        def decorator(handler):
            self.routes.append(URLSpec(pattern, handler, kwargs, name))
            return handler
        return decorator

    def add_route(self, pattern, handler, kwargs=None, name=None):
        self.routes.append(URLSpec(pattern, handler, kwargs, name))

    @property
    def ui_modules(self):
        if 'ui_modules' not in self.settings.TORNADO:
            self.settings.TORNADO['ui_modules'] = {}
        return self.settings.TORNADO['ui_modules']

    def ui_module(self, name):
        def decorator(ui):
            self.ui_modules[name] = ui
            return ui
        return decorator

    def add_ui_module(self, name, ui):
        self.ui_modules[name] = ui

    def configure(self):
        for app_name in self.settings.INSTALLED_APPS:
            app = importlib.import_module(app_name)
            if app.__file__.endswith('__init__.py'):
                for k, v in self.settings.APP_MODULE.items():
                    try:
                        importlib.import_module(''.join(
                            [app_name, '.', v]
                        ))
                    except ImportError:
                        pass
        self._application = Application(self.routes, **self.settings.TORNADO)

    def listen(self, port=8888, *args, **kwargs):
        if self.application is None:
            self.configure()
        return self.application.listen(port, *args, **kwargs)

    def run(self, port=8888, ioloop=None, *args, **kwargs):
        self.listen(port, *args, **kwargs)
        if ioloop is not None:
            self.ioloop.start()
        else:
            self.settings.IOLOOP.start()

    pass


class TornextRequestHandler(tornado.web.RequestHandler):

    @property
    def tkwargs(self):
        if not hasattr(self, '_tkwargs'):
            self._tkwargs = {
                'get_query_string': self.get_query_string,
            }
        return self._tkwargs

    @property
    def all_body_argument(self):
        if not hasattr(self, '_all_body_argument'):
            self._all_body_argument = {
                key: self.get_body_arguments(key)[-1]
                for key in self.request.body_arguments
            }
        return self._all_body_argument

    @property
    def all_body_arguments(self):
        if not hasattr(self, '_all_body_arguments'):
            self._all_body_arguments = {
                key: self.get_body_arguments(key)
                for key in self.request.body_arguments
            }
        return self._all_body_arguments

    @property
    def all_query_argument(self):
        if not hasattr(self, '_all_query_argument'):
            self._all_query_argument = {
                key: self.get_query_arguments(key)[-1]
                for key in self.request.query_arguments
            }
        return self._all_query_argument

    @property
    def all_query_arguments(self):
        if not hasattr(self, '_all_query_arguments'):
            self._all_query_arguments = {
                key: self.get_query_arguments(key)
                for key in self.request.query_arguments
            }
        return self._all_query_arguments

    def get_query_string(self, **merge):
        if merge:
            urlarg = {}
            urlarg.update(self.all_query_argument, **merge)
            return urlencode(urlarg)
        return self.request.query

    def render(self, template_name, **kwargs):
        kwargs.update(self.tkwargs)
        super(TornextRequestHandler, self).render(template_name, **kwargs)

    pass


def error_handler(request_handler):
    tornado.web.ErrorHandler = request_handler
    return request_handler
