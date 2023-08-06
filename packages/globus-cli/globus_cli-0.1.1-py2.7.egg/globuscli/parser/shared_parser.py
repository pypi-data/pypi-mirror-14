import argparse
import textwrap
import json

import globuscli


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

        # additional params -- only useable on a select subset of commands;
        # many will ignore it
        # this is used to pass parameters to API calls when they support a
        # wider range of options than the base CLI commands
        self.add_argument('--additional-params', dest='additional_params',
                          default={}, type=json.loads,
                          help=('Additional parameters for API calls. '
                                'Encoded as query params for commands '
                                'which map directly onto API calls. '
                                'Usage and meaning will depend on command.'))
        self.add_argument('--supports-additional-params',
                          dest='check_added_params',
                          default=False, action='store_true',
                          help=('Check if a command supports the '
                                '`--additional-params` argument.'))
