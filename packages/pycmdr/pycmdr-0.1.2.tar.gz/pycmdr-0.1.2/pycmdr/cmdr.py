# -*- coding: utf8 -*-

import sys
import inspect
import argparse
from itertools import zip_longest


class App:
    POSITIONAL_ARG = type('positional_arg', (object,), {})
    COMMAND_KEY = 'cmd'

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.subparsers = self.parser.add_subparsers()


    def cmd(self, *args, **kwargs):
        def _cmd(func):
            return self.add_command(func, *args, **kwargs)
        return _cmd


    def add_command(self, func, name=None, **kwargs):
        help = func.__doc__ and func.__doc__.strip()
        func_name = name or func.__name__

        subparser = self.subparsers.add_parser(func_name, help=help)
        argspec = inspect.getargspec(func)
        cmd_args = reversed(list(zip_longest(
                reversed(argspec.args or []),
                reversed(argspec.defaults or []),
                fillvalue=self.POSITIONAL_ARG()
        )))

        for k, v in cmd_args:
            args = []
            #TODO: optional args for subcommands.
            if isinstance(v, self.POSITIONAL_ARG):
                args.append(k)
            else:
                args.append('--%s' % k)
                kwargs.update({
                    'dest': k,
                    'default': v
                })
            subparser.add_argument(*args, **kwargs)
        subparser.set_defaults(**{self.COMMAND_KEY: func})
        return func


    def __call__(self):
        arg_list = sys.argv[1:]
        arg_map = self.parser.parse_args(arg_list).__dict__
        command = arg_map.pop(self.COMMAND_KEY)
        return command(**arg_map)


app = App()
cmd = app.cmd