#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
# Copyright (c) 2016 JZQT <tjy.jzqt@qq.com>

import os
import errno
import importlib


class Settings(dict):
    """ Tornext Application Settings.

    You can fill settings from a pyfile::

        app.settings.from_pyfile('your_settings.py')

    Or use absolute path::

        app.settings.from_pyfile('/path/to/your/settings.py')

    Of course, you can load settings from a settings module,
    a string of module or a dict object.

    These following ways is equivalent::

        app.settings.from_object('app_module.settings')

        import app_module.settings
        app.settings.from_object(app_module.settings)

    See `tornext.web.Tornext` for more information.
    """

    def __getattr__(self, name):
        if name in self:
            return self[name]
        return dict.__getattr__(self, name)

    def __repr__(self):
        return "<{}, {}>".format(self.__class__.__name__, dict.__repr__(self))

    def from_envvar(self, variable_name, silent=False):
        value = os.environ.get(variable_name)
        if not value:
            if silent:
                return False
            raise RuntimeError("Unset environment variable"
                               "{}".format(variable_name))
        return self.from_pyfile(value)

    def from_pyfile(self, filename, silent=False):
        config = {}
        try:
            with open(filename) as config_file:
                exec(compile(config_file.read(), filename, 'exec'), config)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = "Unable to from config file ({})".format(e.strerror)
            raise
        self.from_object(config)
        return True

    def from_object(self, obj):
        """Load settings from a string, a dict or a module object, etc.

        :param any obj: If `obj` is a string object, it will be as a string
                        can be import. Then was used as a module to load.
                        If `obj` is a `dict` object, its items will be loaded
                        as setting.
                        If `obj` is a module object or other, its attributes
                        will be loaded as setting.
        """
        if isinstance(obj, str):
            obj = importlib.import_module(obj)
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key.isupper():
                    self[key] = value
        else:
            for key in dir(obj):
                if key.isupper():
                    self[key] = getattr(obj, key)

    def replace_by(self, obj):
        self.clear()
        self.from_object(obj)

    pass
