from globuscli.parser import GlobusCLISharedParser
from globuscli.helpers import supports_additional_params

from globus_sdk.auth import AuthClient


def add_subcommand_parsers(subparsers):
    """
    Add Globus Auth commands
    """
    auth_parser = subparsers.add_parser(
        'auth', help=(
            'Interact with Globus Auth API. '
            'Used to inspect tokens, identities, identity sets, '
            'consent to service terms, revoke and manage consents, '
            'manage OAuth Clients, and a variety of other '
            'Authorization and Authentication based activities.'))

    subsubparsers = auth_parser.add_subparsers(
        title='Commands', parser_class=GlobusCLISharedParser, metavar='')

    add_get_identities_parser(subsubparsers)
    add_token_introspect_parser(subsubparsers)


def add_get_identities_parser(subsubparsers):
    """
    Subcommand parser for `globuscli auth get-identities`
    """
    get_identities_parser = subsubparsers.add_parser(
        'get-identities', help=(
            'Inspect Globus Auth Identities')
        )
    get_identities_parser.set_defaults(func=get_identities)


def add_token_introspect_parser(subsubparsers):
    """
    Subcommand parser for `globuscli auth token_introspect`
    TODO: implement me
    """
    pass


@supports_additional_params
def get_identities(args):
    """
    Executor for `globuscli auth get-identities`
    """
    client = AuthClient()
    client.set_auth_token('AQBW4E04AAAAAAACxO1aAWUzNjCMRGF1q0l4Y_eM5C8gP8Hxi6Uhimz5IuYapY1dZKHuqX__7AQFkwnSdPBz')
    res = client.get('/v2/api/identities', params=args.additional_params)

    print(res.text)
