#!/usr/bin/env python3
'''\
Run a command using a modified environment configured in an INI file.
'''
from __future__ import print_function
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os.path

DESCRIPTION = __doc__
EPILOG = '''\
example:
  %(prog)s --clear printenv
'''


def run(config, section, upper, clear, command, args):
    env = {} if clear else os.environ.copy()

    fp = open(config)
    cp = configparser.RawConfigParser()
    cp.readfp(fp, config)

    if section is None:
        section = os.path.basename(command)

    if upper:
        env.update((k.upper(), v) for k, v in cp.items(section))
    else:
        env.update(cp.items(section))

    os.execvpe(command, [command] + args, env)


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description=DESCRIPTION, epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--config', '-c', default='envfile.ini',
        help="configuration file (default: envfile.ini)")
    parser.add_argument(
        '--section', '-s',
        help="configuration section (default: command basename)")
    parser.add_argument(
        '--upper', action='store_true',
        help="uppercase environment variable names")
    parser.add_argument(
        '--clear', action='store_true',
        help="don't include the current environment")
    parser.add_argument(
        'command', help='command to run')
    parser.add_argument(
        'args', metavar='arg', nargs='*', help='arguments to command')
    args = parser.parse_args()

    try:
        run(**vars(args))
    except OSError as err:
        print(err, file=sys.stderr)
        return err.errno
    except Exception as err:
        print(err, file=sys.stderr)
        return -1


if __name__ == '__main__':
    main()
