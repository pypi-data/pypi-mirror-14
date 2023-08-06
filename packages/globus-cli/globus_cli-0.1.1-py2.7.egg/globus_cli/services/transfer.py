from __future__ import print_function

import json

from globus_sdk import TransferClient

from globus_cli.helpers import outformat_is_json, outformat_is_text


def _display_name_or_cname(ep_doc):
    return ep_doc['display_name'] or ep_doc['canonical_name']


def endpoint_search(args):
    """
    Executor for `globus transfer endpoint-search`
    """
    client = TransferClient()

    text_col_format = '{:<32} | {:<36} | {}'
    if outformat_is_text(args):
        print(text_col_format.format('Owner', 'ID', 'Display Name'))
        print(text_col_format.format('-'*32, '-'*36, '-'*len('Display Name')))

    json_output_dict = {'DATA': []}

    for result in client.endpoint_search(
            args.fulltext, filter_scope=args.scope):
        if outformat_is_json(args):
            json_output_dict['DATA'].append(result)
        else:
            print(text_col_format.format(
                result['owner_string'], result['id'],
                _display_name_or_cname(result)))

    if outformat_is_json(args):
        print(json.dumps(json_output_dict))


def endpoint_autoactivate(args):
    """
    Executor for `globus transfer endpoint-autoactivate`
    """
    client = TransferClient()
    res = client.endpoint_autoactivate(args.endpoint_id)
    print(res.text_body)


def task_list(args):
    """
    Executor for `globus transfer task-list`
    """
    client = TransferClient()

    json_output_dict = {'DATA': []}

    for result in client.task_list(num_results=10):
        if outformat_is_json(args):
            json_output_dict['DATA'].append(result)
        else:
            print(json.dumps(result))

    if outformat_is_json(args):
        print(json.dumps(json_output_dict))


def op_ls(args):
    """
    Executor for `globus transfer ls`
    """
    client = TransferClient()
    res = client.operation_ls(args.endpoint_id, path=args.path)
    print(res.text_body)
