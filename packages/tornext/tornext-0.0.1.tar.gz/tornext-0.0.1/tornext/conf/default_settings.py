""" Tornext settings.
"""

import tornado.web
import tornado.ioloop

# Tornado Application Settings
# For the full list of settings and their values, see
# http://www.tornadoweb.org/en/latest/web.html#tornado.web.Application.settings
TORNADO = {
    # ================
    # General settings
    # ================

    # If True, the server process will restart when any source files change,
    # as described in Debug mode and automatic reloading.
    # This option is new in Tornado 3.2;
    # previously this functionality was controlled by the debug setting.
    # 'autoreload': ???,

    # Shorthand for several debug mode settings,
    # described in Debug mode and automatic reloading.
    # Setting ``debug=True`` is equivalent to ``autoreload=True``,
    # ``compiled_template_cache=False``, ``static_hash_cache=False``,
    # ``serve_traceback=True``.
    'debug': False,

    # This handler will be used if no other match is found;
    # use this to implement custom 404 pages (new in Tornado 3.2).
    # Hint: 建议使用Tornext推荐的方式设置.
    # 'default_handler_class': ???,
    # 'default_handler_args': {},

    # If True, responses in textual formats will be compressed automatically.
    # New in Tornado 4.0.
    # 'compress_response': ???,

    # This function will be called at the end of every request to log the
    # result (with one argument, the ``tornado.web.RequestHandler`` object).
    # The default implementation writes to the logging module’s root logger.
    # May also be customized by overriding ``Application.log_request``.
    # 'log_function': ???,

    # If true, the default error page will include the traceback of the error.
    # This option is new in Tornado 3.2;
    # previously this functionality was controlled by the debug setting.
    # 'serve_traceback': ???,

    # May be set to a mapping of UIModule or UI methods to be
    # made available to templates. May be set to a module, dictionary,
    # or a list of modules and/or dicts. See UI modules for more details.
    # Hint: 建议使用Tornext推荐的方式设置.
    # 'ui_modules': {},
    # 'ui_methods': {},

    # ====================================
    # Authentication and security settings
    # ====================================

    # Used by ``RequestHandler.get_secure_cookie``
    # and ``set_secure_cookie`` to sign cookies.
    'cookie_secret': None,

    # Used by ``RequestHandler.set_secure_cookie`` to sign cookies with a
    # specific key when ``cookie_secret`` is a key dictionary.
    'key_version': None,

    # The authenticated decorator will redirect
    # to this url if the user is not logged in.
    # Can be further customized by overriding ``RequestHandler.get_login_url``
    'login_url': None,

    # If true, Cross-site request forgery protection will be enabled.
    'xsrf_cookies': False,

    # Controls the version of new XSRF cookies produced by this server.
    # Should generally be left at the default (which will always
    # be the highest supported version),
    # but may be set to a lower value temporarily during version transitions.
    # New in Tornado 3.2.2, which introduced XSRF cookie version 2.
    'xsrf_cookie_version': 2,

    # May be set to a dictionary of additional arguments to be passed to
    # ``RequestHandler.set_cookie`` for the XSRF cookie.
    'xsrf_cookie_kwargs': {},

    # Used in the tornado.auth module to authenticate to various APIs.
    # 'twitter_consumer_key': None,
    # 'twitter_consumer_secret': None,
    # 'friendfeed_consumer_key': None,
    # 'friendfeed_consumer_secret': None,
    # 'google_consumer_key': None,
    # 'google_consumer_secret': None,
    # 'facebook_api_key': None,
    # 'facebook_secret': None,

    # =================
    # Template settings
    # =================

    # Controls automatic escaping for templates. May be set to ``None``
    # to disable escaping, or to the name of a function that
    # all output should be passed through. Defaults to ``"xhtml_escape"``.
    # Can be changed on a per-template basis with
    # the ``{% autoescape %}`` directive.
    # 'autoescape': ???,

    # Default is ``True``; if ``False`` templates will be recompiled on
    # every request. This option is new in Tornado 3.2;
    # previously this functionality was controlled by the ``debug`` setting.
    # 'compiled_template_cache': ???,

    # Directory containing template files.
    # Can be further customized by overriding
    # ``RequestHandler.get_template_path``
    'template_path': None,

    # Assign to an instance of ``tornado.template.BaseLoader``
    # to customize template loading.
    # If this setting is used the ``template_path`` and ``autoescape`` settings
    # are ignored. Can be further customized by overriding
    # ``RequestHandler.create_template_loader``.
    # 'template_loader': ???,

    # Controls handling of whitespace in templates;
    # see ``tornado.template.filter_whitespace`` for allowed values.
    # New in Tornado 4.3.
    # 'template_whitespace': ???,

    # ====================
    # Static file settings
    # ====================

    # Default is ``True``; if ``False`` static urls will be recomputed on
    # every request. This option is new in Tornado 3.2;
    # previously this functionality was controlled by the debug setting.
    # 'static_hash_cache': ???,

    # Directory from which static files will be served.
    'static_path': None,

    # Url prefix for static files, defaults to "/static/".
    'static_url_prefix': "/static/",

    # May be set to use a different handler for static files
    # instead of the default ``tornado.web.StaticFileHandler``.
    # ``static_handler_args``, if set, should be a dictionary of
    # keyword arguments to be passed to the handler’s ``initialize`` method.
    # Hint: 建议使用Tornext推荐的方式设置.
    # 'static_handler_class': tornado.web.StaticFileHandler,
    # 'static_handler_args': {},
}

IOLOOP = tornado.ioloop.IOLoop.current()

APP_MODULE = {
    'views': 'views',
    'ui': 'ui',
}

INSTALLED_APPS = (
)
