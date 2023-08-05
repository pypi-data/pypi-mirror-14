# -*- coding: utf8 -*-

import sys
import enum
import inspect
from functools import wraps
from inspect import ismethod
import argparse
from itertools import zip_longest

@enum.unique
class DocStyle(enum.Enum):
    PYTHON = (':param ')
    GOOGLE = ('{name} ({type}): ')

    def __init__(self, param_delimiter):
        self.delimiter = param_delimiter

class App():
    POSITIONAL_ARG = type('positional_arg', (object,), {})
    COMMAND_KEY = 'cmd'


    def __init__(self, name='cmdr', docstyle=DocStyle.PYTHON):
        self.parser = argparse.ArgumentParser()
        self.subparsers = self.parser.add_subparsers()
        self.docstyle = docstyle


    def cmd(self, *args, **kwargs):
        # to call without params
        ifarg = None
        if 'ifarg' in kwargs:
            ifarg = kwargs['ifarg']
            del kwargs['ifarg']

        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return self.add_command(args[0], *args, **kwargs)
        else:
            name = args[0] if type(args[0]) == str else None
            def _cmd(func):
                return self.add_command(func, name=name, ifarg=ifarg, *args, **kwargs)
            return _cmd


    def add_command(self, func, method=False, name=None, ifarg=None, **kwargs):
        func_name = name or func.__name__

        docs = self.parse_docstring(func)

        subparser = self.subparsers.add_parser(func_name, help=docs['full'])
        argspec = inspect.getargspec(func)


        cmd_args = reversed(list(zip_longest(
            reversed(argspec.args or []),
            reversed(argspec.defaults or []),
            fillvalue=self.POSITIONAL_ARG()
        )))


        def get_opt_list(opt):
            if ifarg:
                for k, v in ifarg.items():
                    if 'opt' in v and opt in v['opt']:
                        return k
            return False

        main_group = subparser.add_mutually_exclusive_group()
        arg_groups = {}
        if ifarg:
            for k in ifarg.keys():
                arg_groups[k] = main_group.add_argument_group()


        for k, v in cmd_args:
            args = []
            # TODO: optional args for subcommands.

            if isinstance(v, self.POSITIONAL_ARG):
                args.append(k)
                if ifarg and k in ifarg:
                    kwargs.update({'nargs': '?'})
                elif k in docs['params']:
                    kwargs.update({'help': docs['params'][k]})
            else:
                if len(k) > 1:
                    args.append('-{}'.format(k[0]))
                args.append('--{}'.format(k))
                kwarg = {
                    'dest': k,
                    'default': v
                }
                if isinstance(v, bool):
                    kwarg['action'] = 'store_true'
                if k in docs['params']:
                    kwarg['help'] = docs['params'][k]
                kwargs.update(kwarg)
            if k in arg_groups.keys():
                arg_groups[k].add_argument(*args, **kwargs)
            # elif get_opt_list(k):
            #     arg_groups[get_opt_list(k)].add_argument(*args, **kwargs)
            else:
                main_group.add_argument(*args, **kwargs)
        main_group.set_defaults(**{self.COMMAND_KEY: func})
        return func


    def parse_docstring(self, func):
        # google-style docs not yet supported.
        assert self.docstyle == DocStyle.PYTHON
        param_delim = ':param '

        doc = func.__doc__
        docs = {
            'name': func.__name__,
            'full': doc,
            'params': {}
        }

        try:
            ds = [line.strip() for line in doc.split('\n') if line.strip()]
            ps = [l for l in ds if l.startswith(param_delim)]

            for p in ps:
                p = ''.join(p.split(param_delim)[1:])
                p = p.split(': ')
                docs['params'][p[0]] = p[1]
        except Exception:
            pass

        return docs


    def __call__(self):
        arg_list = sys.argv[1:]
        arg_map = self.parser.parse_args(arg_list).__dict__
        command = arg_map.pop(self.COMMAND_KEY)
        return command(**arg_map)