import argparse
import logging
import sys
import traceback

from vmupdate.config import config
from vmupdate.host import update_all_vms


def main():
    sys.excepthook = unhandled_exception_handler

    args = parse_args(sys.argv[1:])

    config.load(args.config, args.logdir)

    return update_all_vms()


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', help='use specified config path')
    parser.add_argument('-l', '--logdir', help='directory for log files')

    return parser.parse_args(args)


def unhandled_exception_handler(type, value, tb):
    log = logging.getLogger(__name__)

    log.critical('Unhandled exception\n%s', ''.join(traceback.format_exception(type, value, tb)))


if __name__ == '__main__':
    sys.exit(main())
