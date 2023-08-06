from __future__ import print_function
import sys
import json


# Format Enum for output formatting
# could use a namedtuple, but that's overkill
JSON_FORMAT = 'json'
TEXT_FORMAT = 'text'


def stderr_prompt(prompt):
    """
    Prompt for input on stderr.
    Good for not muddying redirected output while prompting the user.
    """
    print(prompt, file=sys.stderr, end='')
    return raw_input()


def outformat_is_json(args):
    return args.outformat == JSON_FORMAT


def outformat_is_text(args):
    return args.outformat == TEXT_FORMAT


def cliargs(helptext, arguments, arg_validator=None):
    """
    Decorator that takes a function and adds CLI arguments and helptext to it
    as function attributes. The function can then be placed directly into the
    command hierarchy of the _COMMAND_TREE and will be unpacked and inspected
    by parser building.
    """
    def inner_decorator(wrapped):
        """
        The decorator produced by invoking cliargs() on some arguments.
        Doesn't need to create a closure over the wrapped function or anything:
        just takes the arguments to cliargs() and puts them into attributes of
        the function.
        """
        wrapped.cli_help = helptext
        wrapped.cli_arguments = arguments
        wrapped.cli_argument_validator = arg_validator

        return wrapped

    return inner_decorator


class CLIArg(object):
    def __init__(self, name, **kwargs):
        self.kwargs = kwargs
        self.name = name

        self.kwargs.update({
            'dest': self.name.replace('-', '_')
        })

    def argparse_arglist(self):
        return ['--{}'.format(self.name)]

    def argparse_kwargs(self):
        return self.kwargs

    def is_required(self):
        return 'required' in self.kwargs and self.kwargs['required']


def print_json_response(res):
    print(json.dumps(res.data, indent=2))


def colon_formatted_print(data, named_fields):
    maxlen = max(len(n) for n, f in named_fields) + 1
    for name, field in named_fields:
        print('{} {}'.format((name + ':').ljust(maxlen), data[field]))


def not_implemented_func():
    """
    This is a dummy function used to stub parts of the command tree that
    haven't been implemented yet.
    It has the same signature as a typical command function (i.e. takes args
    and nothing else), but raises a NotImplementedError
    """
    raise NotImplementedError(('Hold yer horses! '
                               'This command has not been implemented yet!'))
