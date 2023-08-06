from . import nexus
from . import auth
from . import transfer


def add_subcommand_parsers(subparsers):
    """
    Add the subcommand parser for each service
    (order doesn't matter)
    """
    nexus.add_subcommand_parsers(subparsers)
    auth.add_subcommand_parsers(subparsers)
    transfer.add_subcommand_parsers(subparsers)
