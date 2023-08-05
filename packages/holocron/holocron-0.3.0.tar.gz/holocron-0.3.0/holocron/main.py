# coding: utf-8
"""
    holocron.main
    ~~~~~~~~~~~~~

    This module provides a command line interface and an entry point for
    end users.

    :copyright: (c) 2014 by the Holocron Team, see AUTHORS for details.
    :license: 3-clause BSD, see LICENSE for details.
"""

import sys
import logging
import argparse
import warnings

from dooku.ext import ExtensionManager

from holocron import __version__ as holocron_version
from holocron.app import create_app


def configure_logger(level):
    """
    Configure a root logger to print records in pretty format.

    The format is more readable for end users, since it's not necessary at
    all to know a record's dateime and a source of the record.

    Examples::

        [INFO] message
        [WARN] message
        [ERRO] message

    :param level: a minimum logging level to be printed
    """
    class _Formatter(logging.Formatter):
        def format(self, record):
            record.levelname = record.levelname[:4]
            return super(_Formatter, self).format(record)

    # create stream handler with custom formatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(_Formatter('[%(levelname)s] %(message)s'))

    # configure root logger
    logger = logging.getLogger()
    logger.addHandler(stream_handler)
    logger.setLevel(level)

    # capture warnings issued by 'warnings' module
    logging.captureWarnings(True)


def parse_command_line(args, commands):
    """
    Builds a command line interface, and parses its arguments. Returns
    an object with attributes, that are represent CLI arguments.

    :param args: a list of command line arguments
    :param commands: a dict with available commands (name -> instance)
    :returns: a parsed object with cli options
    """
    parser = argparse.ArgumentParser(
        description=(
            'Holocron is an easy and lightweight static blog generator, '
            'based on markup text and Jinja2 templates.'),
        epilog=(
            'With no CONF, read _config.yml in the current working dir. '
            'If no CONF found, the default settings will be used.'))

    parser.add_argument(
        '-c', '--conf', dest='conf', default='_config.yml',
        help='set path to the settings file')

    parser.add_argument(
        '-q', '--quiet', dest='verbosity', action='store_const',
        const=logging.CRITICAL, help='show only critical errors')

    parser.add_argument(
        '-v', '--verbose', dest='verbosity', action='store_const',
        const=logging.INFO, help='show additional messages')

    parser.add_argument(
        '-d', '--debug', dest='verbosity', action='store_const',
        const=logging.DEBUG, help='show all messages')

    parser.add_argument(
        '--version', action='version', version=holocron_version,
        help='show the holocron version and exit')

    command_parser = parser.add_subparsers(
        dest='command', help='command to execute')

    # declare commands
    for name, command in commands.items():
        subparser = command_parser.add_parser(name)
        command.set_arguments(subparser)

    # parse cli and form arguments object
    arguments = parser.parse_args(args)

    # if no commands are specified display help
    if arguments.command is None:
        parser.print_help()
        parser.exit(1)

    # this hack's used to bypass lack of user's config file when init invoked
    if arguments.command in ('init', ):
        arguments.conf = None

    return arguments


def main(args=sys.argv[1:]):
    # get available commands and build cli based on it
    commands_manager = ExtensionManager('holocron.ext.commands')
    commands = {name: command() for name, command in commands_manager}
    arguments = parse_command_line(args, commands)

    # initial logger configuration - use custom format for records
    # and print records with WARNING level and higher.
    configure_logger(arguments.verbosity or logging.WARNING)

    # show deprecation warnings in order to be prepared for backward
    # incompatible changes
    warnings.filterwarnings('always', category=DeprecationWarning)

    # create app instance
    holocron = create_app(arguments.conf)
    if holocron is None:
        sys.exit(1)

    # execute passed command
    commands[arguments.command].execute(holocron, arguments)
