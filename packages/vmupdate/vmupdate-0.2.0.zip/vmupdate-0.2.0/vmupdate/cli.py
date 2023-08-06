"""
    Provide the main entry point and command line parsing.
"""

import argparse
import logging
import sys
import traceback

from vmupdate.config import config
from vmupdate.host import update_all_vms


def main():
    """
        Initialize environment and call :func:`.host.update_all_vms`.

        This is the main entry point for vmupdate.

        :return: exitcode
        :rtype: int
    """

    sys.excepthook = _unhandled_exception_handler

    args = _parse_args(sys.argv[1:])

    config.load(args.config, args.logdir)

    return update_all_vms()


def _parse_args(args):
    """
        Parse ``args`` and return a populated namespace.

        :param list args: command arguments to parse

        :return: populated namespace
        :rtype: :class:`argparse.Namespace`
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', help='use specified config path')
    parser.add_argument('-l', '--logdir', help='directory for log files')

    return parser.parse_args(args)


def _unhandled_exception_handler(ex_type, ex_value, ex_tb):
    """Log unhandled exceptions."""

    log = logging.getLogger(__name__)

    log.critical('Unhandled exception\n%s', ''.join(traceback.format_exception(ex_type, ex_value, ex_tb)))


if __name__ == '__main__':
    sys.exit(main())
