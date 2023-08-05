#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
# Copyright 2016 JZQT <tjy.jzqt@qq.com>

import os
from os.path import abspath, dirname, join
import argparse

from tornado.template import Template

__all__ = ['Manager', 'execute_command_line']


class Manager(object):

    builtin_subcommands = {'newproject', 'checkviews'}

    def __init__(self, tornext_app=None):
        self._tornext_app = tornext_app
        self._command_parser = argparse.ArgumentParser()
        self._subcommand_parser = self._command_parser.add_subparsers(
            dest='subcommand', title='subcommands'
        )
        self._subparser = {}
        self._subparser['newproject'] = self._subcommand_parser.add_parser(
            'newproject', help="Create a project use recommanded layout."
        )
        self._subparser['newproject'].add_argument(
            'name', type=str, help="Tornext project's name."
        )
        self._subparser['newproject'].add_argument(
            '--dir', type=str, help=("Tornext project's directory. "
                                     "default project name.")
        )
        self._subparser['checkviews'] = self._subcommand_parser.add_parser(
            'checkviews', help="Check and print registered views."
        )

    @property
    def tornext_app(self):
        if not hasattr(self, '_tornext_app'):
            self._tornext_app = None
        return self._tornext_app

    def newproject(self, project_name, project_dir):
        """Subcommand: ``newproject``

        Create a tornext project use recommanded layout.

        .. project layout::

            project_dir
            ├── project_name
            │   ├── __init__.py
            │   └── settings.py
            ├── static/
            ├── templates/
            └── manage.py

        :param str project_name: The tornext project name.
                                 It must be a Python identifier.
                                 It is recommended to use lower case.
        """
        if project_name.isidentifier():
            if project_dir is None:
                project_dir = join(abspath(os.curdir), project_name)
            else:
                project_dir = join(abspath(os.curdir), project_dir)
            template_dir = join(dirname(__file__), 'project_template')
            file_list = ('manage.py', 'app/__init__.py'.format(project_name),
                         'app/settings.py'.format(project_name))
            try:
                os.makedirs(project_dir)
            except FileExistsError:
                self._subparser['newproject'].error(
                    "Directory '{}' exists.".format(project_name)
                )
            else:
                def create_and_render_file(filename):
                    with open(join(project_dir, filename), 'x') as dst:
                        with open(join(template_dir, filename)) as src:
                            dst.write(Template(src.read()).generate(
                                project_name=project_name
                            ).decode())
                # Create directory and file.
                os.makedirs(join(project_dir, 'app'))
                os.makedirs(join(project_dir, 'static'))
                os.makedirs(join(project_dir, 'templates'))
                [create_and_render_file(filename) for filename in file_list]
                # chmod u+x manage.py
                os.chmod(join(project_dir, 'manage.py'), 0o764)
                # Rename project name.
                os.chdir(project_dir)
                os.rename('app', project_name)
        else:   # `project_name` is not identifier.
            self._subparser['newproject'].error(
                "Project name must is a Python identifier."
            )

    def checkviews(self):
        """Subcommand: ``checkviews``"""
        if self.tornext_app is None:
            self._subparser['checkviews'].error(
                "Manager not register a tornext application."
            )
            return
        self._tornext_app.configure()
        print(self._tornext_app.routes)

    def execute(self):
        args = self._command_parser.parse_args()
        if args.subcommand not in self.builtin_subcommands:
            self._command_parser.parse_args(['-h'])
        elif args.subcommand == 'newproject':
            self.newproject(args.name, args.dir)
        elif args.subcommand == 'checkviews':
            self.checkviews()
        else:
            pass

    pass


def execute_command_line():
    Manager().execute()
