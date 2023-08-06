#!/usr/bin/env python

from globuscli.nexus import get_goauth_token


def add_subparser(subparsers, shared_parser_class):
    """
    Add Nexus commands (so far, only one)
    """
    nexus_parser = subparsers.add_parser(
        'nexus', help=(
            'Interact with legacy Nexus API. WARNING: Deprecated.'
            'Only use this if you need access to legacy tokens '
            'during the development of globuscli. These methods '
            'will be replaced in the near future with commands '
            'which use other services.'))

    subsubparsers = nexus_parser.add_subparsers(
        title='Commands', parser_class=shared_parser_class, metavar='')

    add_get_goauth_token_parser(subsubparsers)


def add_get_goauth_token_parser(subsubparsers):
    get_goauth_token_parser = subsubparsers.add_parser(
        'get-goauth-token', help=(
            'Get a Legacy GOAuth Token from Globus Nexus.')
        )
    get_goauth_token_parser.set_defaults(func=get_goauth_token.main)

    get_goauth_token_parser.add_argument(
        '-u', '--username', dest='username', default=None,
        help='Username for a GlobusID user to use to get a token.')
    get_goauth_token_parser.add_argument(
        '-p', '--password', dest='password', default=None,
        help='Password for a GlobusID user to use to get a token.')
