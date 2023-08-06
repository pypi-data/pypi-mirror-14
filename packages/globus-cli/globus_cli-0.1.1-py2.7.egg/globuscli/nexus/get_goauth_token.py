#!/usr/bin/env python

from __future__ import print_function

import getpass
import json

from globuscli.helpers import (stderr_prompt, require_interactive_input,
                               require_interactive_err)
from globus_sdk import NexusClient


def main(args):
    # get username and/or password if not present
    if not args.username:
        require_interactive_input()
        require_interactive_err()
        args.username = stderr_prompt('GlobusID Username: ')
    if not args.password:
        require_interactive_input()
        require_interactive_err()
        args.password = getpass.getpass('GlobusID Password: ')

    # get the token itself
    ncl = NexusClient()
    tok = ncl.get_goauth_token(args.username, args.password)

    # print it out in JSON or TEXT format, then exit
    if args.outformat == 'json':
        print(json.dumps({'token': tok}))
    else:
        print(tok)
