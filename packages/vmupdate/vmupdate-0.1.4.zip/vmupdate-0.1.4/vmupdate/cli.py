import argparse
import sys

from vmupdate.config import config
from vmupdate.host import update_all_vms


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', help='use specified config path')
    parser.add_argument('-l', '--logdir', help='directory for log files')

    args = parser.parse_args()

    config.load(args.config, args.logdir)

    update_all_vms()

    return 0


if __name__ == '__main__':
    sys.exit(main())
