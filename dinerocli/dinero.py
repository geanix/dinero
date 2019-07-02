import configparser
import argparse
import logging
import sys
import os

from .contacts import contacts_arguments
from .organizations import organizations_arguments

def global_arguments(subparser, config):
    # global arguments
    subparser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])
    subparser.add_argument('--url', default='https://authz.dinero.dk/dineroapi/oauth/token', help='Dinero oauth url')
    subparser.add_argument('--client_id', help='Dinero client id')
    subparser.add_argument('--client_secret', help='Dinero client secret')
    subparser.add_argument('--organization_key', help='Dinero organization key')
    subparser.add_argument('--organization_name', help='Dinero organization name')
    subparser.add_argument('--organization_id', help='Dinero organization id')

    # set defaults for the dinero arguments from config file
    if 'dinero' in config.sections():
        d = dict(config.items('dinero'))
        subparser.set_defaults(**d)

def main():
    # condig file argument
    top_parser = argparse.ArgumentParser(description='Access Dinero accounting service', add_help=False)
    top_parser.add_argument(
        '--config',
        default=os.path.expanduser('~/.config/dinero.conf'),
        help='path to config file'
    )

    # parse known arguments to get config file
    args,remaining = top_parser.parse_known_args()

    # read config file for default values
    config = configparser.SafeConfigParser()
    if args.config:
        config.read([args.config])

    # add sub-parser for subcommands
    parser = argparse.ArgumentParser(parents=[top_parser],)
    subparsers = parser.add_subparsers(dest='subcommand')

    # add subcommands
    contacts_arguments(subparsers, config, global_arguments)
    organizations_arguments(subparsers, config, global_arguments)

    # parse arguments
    args = parser.parse_args(remaining)

    # setup logging for dinero library
    logger = logging.getLogger('libdinero')
    logger.setLevel(args.loglevel.upper())
    logger.addHandler(logging.StreamHandler())

    # validate required arguments
    if args.client_id is None:
        logging.error('missing --client_id')
        sys.exit(1)

    if args.client_secret is None:
        logging.error('missing --client_secret')
        sys.exit(1)

    if args.organization_key is None:
        logging.error('missing --organization_key')
        sys.exit(1)

    # call subcommand function
    if args.subcommand:
        args.func(args)
