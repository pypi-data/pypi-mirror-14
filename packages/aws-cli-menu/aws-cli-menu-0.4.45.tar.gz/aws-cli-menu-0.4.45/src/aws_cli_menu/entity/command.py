from __future__ import division, print_function, absolute_import, unicode_literals

import six
from aws_cli_menu.commons.case_class import CaseClass
from aws_cli_menu.commons.string import to_unicode
from aws_cli_menu.commons.collection import get_single_item
from aws_cli_menu.commons.types import *
from aws_cli_menu.entity import Item, Meta
from aws_cli_menu.entity.command_line import CommandLine
import inspect

DEBUG=0

class Command(Item):
    @types(title=Unicode, command_lines=ListOf(CommandLine))
    def __init__(self, title, command_lines):
        """
        :param title:
        :param command_lines:
        :return:
        """
        if (DEBUG):
            print('entity.command.py - Command - __init__(self,title,command_lines) - caller:'+str(inspect.stack()[1][3]))

        CaseClass.__init__(self, ('title', title), ('command_lines', command_lines))

    @staticmethod
    @types(Item, data=dict, meta=Meta)
    def parse(data, meta, loader, encoding='utf-8', depth=0):
        """
        Parse one command operation.
        :param data: dict:
        :param meta: Meta: meta configuration inherited from the parent menu
        :param loader: not used
        :param encoding: string:
        :param depth: not used
        :return: Command:
        """
        if (DEBUG):
            print('entity.command.py - Command -parse(data,meta,loader,encoding,depth) - caller:'+str(inspect.stack()[1][3]))

        if len(data) != 1:
            raise ValueError('Command should have only one element, not %s.' % len(data))

        title, content = get_single_item(data)
        assert isinstance(title, six.string_types), 'Command title must be string, not %s' % type(title).__name__
        title = to_unicode(title, encoding)

        if isinstance(content, six.string_types):
            # single command
            return Command(title, [CommandLine.parse(content, meta, encoding)])
        elif isinstance(content, list):
            # command list
            return Command(title, [CommandLine.parse(d, meta, encoding) for d in content])
        else:
            raise ValueError('Invalid command content type: %s' % type(content).__name__)

    @types(Unicode)
    def formatted(self):
        if (DEBUG):
            print('entity.command.py - Command  formatted()- caller:'+str(inspect.stack()[1][3]))

        return '\n'.join(
            ['* %s:' % self.title] + ['  %s' % line for x in self.command_lines for line in x.formatted().splitlines()])
