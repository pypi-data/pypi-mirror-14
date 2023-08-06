from __future__ import print_function

import getpass
import json

from globuscli.parser import GlobusCLISharedParser
from globuscli.helpers import stderr_prompt

from globus_sdk import NexusClient


def add_subcommand_parsers(subparsers):
    """
    Add Nexus commands (so far, only one)
    """
    nexus_parser = subparsers.add_parser(
        'nexus', help=(
            'Interact with legacy Nexus API. WARNING: Deprecated. '
            'Only use this if you need access to legacy tokens '
            'during the development of globuscli. These methods '
            'will be replaced in the near future with commands '
            'which use other services.'))

    subsubparsers = nexus_parser.add_subparsers(
        title='Commands', parser_class=GlobusCLISharedParser, metavar='')

    add_get_goauth_token_parser(subsubparsers)


def add_get_goauth_token_parser(subsubparsers):
    """
    Subcommand parser for `globuscli nexus get-goauth-token`
    """
    get_goauth_token_parser = subsubparsers.add_parser(
        'get-goauth-token', help=(
            'Get a Legacy GOAuth Token from Globus Nexus.')
        )
    get_goauth_token_parser.set_defaults(func=get_goauth_token)

    get_goauth_token_parser.add_argument(
        '-u', '--username', dest='username', default=None,
        help='Username for a GlobusID user to use to get a token.')
    get_goauth_token_parser.add_argument(
        '-p', '--password', dest='password', default=None,
        help='Password for a GlobusID user to use to get a token.')


def get_goauth_token(args):
    """
    Executor for `globuscli nexus get-goauth-token`
    Reads username and password from stdin if they aren't in the args.
    """
    # get username and/or password if not present
    if not args.username:
        args.username = stderr_prompt('GlobusID Username: ')
    if not args.password:
        args.password = getpass.getpass('GlobusID Password: ')

    # get the token itself
    client = NexusClient()
    tok = client.get_goauth_token(args.username, args.password)

    # print it out in JSON or TEXT format, then exit
    if args.outformat == 'json':
        print(json.dumps({'token': tok}))
    else:
        print(tok)
