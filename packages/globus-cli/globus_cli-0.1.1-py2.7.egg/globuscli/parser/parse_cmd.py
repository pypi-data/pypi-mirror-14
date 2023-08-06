from globuscli.parser.shared_parser import GlobusCLISharedParser
from globuscli.services import add_subcommand_parsers
from globuscli.helpers import additional_params_checker


def _gen_parser():
    """
    Produces a top-level argument parser built out of all of the various
    subparsers for different services.
    """
    # create the top parser and give it subparsers
    top_level_parser = GlobusCLISharedParser()
    subparsers = top_level_parser.add_subparsers(
        title='Commands',
        parser_class=GlobusCLISharedParser, metavar='')

    add_subcommand_parsers(subparsers)

    # return the created parser in all of its glory
    return top_level_parser


def _load_args():
    """
    Load commandline arguments, and do any necessary post-processing.

    Mainly, check if `--supports-additional-params` was passed, and alters the
    func to call if it was.
    """
    parser = _gen_parser()
    args = parser.parse_args()

    # are we introspecting the command to see if it supports additional params?
    # note that this function will kill the run in place -- we'll exit here as
    # a result with status 0 or 1, indicating the result of the check
    if args.check_added_params:
        additional_params_checker(args.func)

    return args


def run_command():
    """
    Whatever arguments were loaded, they set a function to be invoked on the
    arguments themselves -- somewhat circular, but a nifty way of passing the
    args to a function that this module doesn't even know about
    """
    args = _load_args()
    args.func(args)
