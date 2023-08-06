from __future__ import print_function
import sys


def stderr_prompt(prompt):
    """
    Prompt for input on stderr.
    Good for not muddying redirected output while prompting the user.
    """
    print(prompt, file=sys.stderr, end='')
    return raw_input()


def additional_params_checker(func):
    bool_result = False
    if hasattr(func, 'supports_added_params'):
        bool_result = func.supports_added_params

    if bool_result:
        print('Yes, this command supports `--additional-params`')
        sys.exit(0)
    else:
        print('No, this command does not support `--additional-params`')
        sys.exit(1)


def supports_additional_params(func):
    func.supports_added_params = True
    return func
