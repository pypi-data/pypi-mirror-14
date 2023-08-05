import cmd
from argcomplete.completers import ChoicesCompleter


class ReplCmdr(cmd.Cmd):
    def __init__(self, name='cmdr'):
        self.intro = 'welcome to {} Type help or ? to list commands.\n'.format(name)
        self.prompt = '{} -> '.format(name)

        super(ReplCmdr, self).__init__(self)
