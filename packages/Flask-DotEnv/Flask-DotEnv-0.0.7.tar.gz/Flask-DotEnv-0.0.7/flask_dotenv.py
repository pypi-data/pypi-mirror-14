"""
FLask-DotEnv

:copyright: (c) 2015 by Yasuhiro Asaka.
:license: BSD 2-Clause License
"""

from __future__ import absolute_import
import ast
import os
import re
import warnings


class DotEnv(object):
    """The .env file support for Flask."""

    def __init__(self, app=None):
        self.app = app
        self.verbose_mode = False
        if app is not None:
            self.init_app(app)

    def init_app(self, app, env_file=None, verbose_mode=False):
        if self.app is None:
            self.app = app
        self.verbose_mode = verbose_mode

        if env_file is None:
            env_file = os.path.join(os.getcwd(), ".env")
        if not os.path.exists(env_file):
            warnings.warn("can't read {0} - it doesn't exist".format(env_file))
        else:
            self.__import_vars(env_file)

    def __import_vars(self, env_file):
        with open(env_file, "r") as f:
            for line in f:
                try:
                    key, val = line.strip().split('=', 1)
                    key = key.replace('export ', '')
                except ValueError:  # Take care of blank or comment lines
                    pass
                finally:
                    if not callable(val):
                        if self.verbose_mode:
                            if key in self.app.config:
                                print(
                                    " * Overwriting an existing config var:"
                                    " {0}".format(key))
                            else:
                                print(
                                    " * Setting an entirely new config var:"
                                    " {0}".format(key))
                        self.app.config[key] = re.sub(
                            r"\A[\"']|[\"']\Z", "", val)

    def eval(self, keys):
        """
        Examples:
            Specify type literal for key.

            >>> env.eval({MAIL_PORT: int})
        """
        for k, v in keys.items():
            if k in self.app.config:
                try:
                    val = ast.literal_eval(self.app.config[k])
                    if type(val) == v:
                        if self.verbose_mode:
                            print(
                                " * Casting a specified var as literal:"
                                " {0} => {1}".format(k, v)
                            )
                        self.app.config[k] = val
                    else:
                        print(
                            " ! Does not match with specified type:"
                            " {0} => {1}".format(k, v))
                except (ValueError, SyntaxError):
                    print(" ! Could not evaluate as literal type:"
                          " {0} => {1}".format(k, v))

    def alias(self, maps):
        """
        Examples:
            Make alias var -> as.

            >>> env.alias(maps={
              'TEST_DATABASE_URL': 'SQLALCHEMY_DATABASE_URI',
              'TEST_HOST': 'HOST'
            })
        """
        for k, v in maps.items():
            if self.verbose_mode:
                print(
                    " * Mapping a specified var as a alias:"
                    " {0} -> {1}".format(v, k))
            self.app.config[v] = self.app.config[k]
