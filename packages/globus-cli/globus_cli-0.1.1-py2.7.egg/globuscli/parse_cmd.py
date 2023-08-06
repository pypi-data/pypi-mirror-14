#!/usr/bin/env python

import argparse
import textwrap

import globuscli
from globuscli.nexus import parse_nexus_cmd
from globuscli.auth import parse_auth_cmd
from globuscli.transfer import parse_transfer_cmd


class GlobusCLISharedParser(argparse.ArgumentParser):
    """
    A base parser type from which all other command parsers inherit. Provides
    shared arguments, top level description, and other common attributes.
    """
    def __init__(self, *args, **kwargs):
        # TODO: Update this description to be more informative, accurate
        description = textwrap.dedent("""Run a globuscli command.
        globuscli is structured to provide a uniform command line interface to
        all Globus services. For more information and tutorials, see
        docs.globus.org
        """)

        # this is marginally nicer than trying to stuff explicit kwargs
        # inbetween *args and **kwargs in the initializer invocation below
        newkwargs = {
            'prog': 'globuscli',
            'description': description
        }
        newkwargs.update(kwargs)
        argparse.ArgumentParser.__init__(self, *args, **newkwargs)

        # shared arguments

        # output format -- all commands must support these, although they
        # are free to implement the TEXT format however they see fit
        self.add_argument(
            '-F', '--format', dest='outformat',
            default='json', choices=['json', 'text'], type=str.lower,
            help='Output format for stdout.')
        # version of globuscli -- ignores all other passed arguments and prints
        # the version
        self.add_argument('--version', action='version',
                          version='%(prog)s ' + globuscli.__version__)


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

    # TODO: is there a nicer/cleaner way of doing this?
    # for each of the command parsing modules, attach the relevant subparser
    # easiest to handle this way because it should be done with
    # subparsers.add_parser(), but then we want a set of add_argument calls on
    # the returned parser object defined by the module
    for mod in (parse_nexus_cmd, parse_auth_cmd, parse_transfer_cmd):
        mod.add_subparser(subparsers, GlobusCLISharedParser)

    # return the created parser in all of its glory
    return top_level_parser


def _load_args():
    """
    Load commandline arguments, and do any necessary post-processing.
    Right now, there is none.
    """
    parser = _gen_parser()
    return parser.parse_args()


def run_command():
    """
    Whatever arguments were loaded, they set a function to be invoked on the
    arguments themselves -- somewhat circular, but a nifty way of passing the
    args to a function that this module doesn't even know about
    """
    args = _load_args()
    args.func(args)
