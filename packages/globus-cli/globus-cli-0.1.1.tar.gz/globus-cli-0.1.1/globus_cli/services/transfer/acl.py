from __future__ import print_function
import json

from globus_cli.helpers import outformat_is_json, cliargs, CLIArg
from globus_cli.services.transfer.helpers import (
    print_json_from_iterator, text_header_and_format, get_client)


@cliargs('List of Access Control List rules on an Endpoint', [
    CLIArg('endpoint-id', required=True, help=(
        'ID of the endpoint, typically fetched from endpoint-search'))
    ])
def acl_list(args):
    """
    Executor for `globus transfer access acl-list`
    """
    client = get_client()

    rule_iterator = client.endpoint_acl_list(args.endpoint_id)

    if outformat_is_json(args):
        print_json_from_iterator(rule_iterator)
    else:
        text_col_format = text_header_and_format(
            [(36, 'Rule ID'), (16, 'Principal Type'), (36, 'Principal'),
             (None, 'Permissions'), (None, 'Path')])

        for result in rule_iterator:
            print(text_col_format.format(
                result.data['id'],
                result.data['principal_type'], result.data['principal'],
                result.data['permissions'], result.data['path']))


@cliargs('Get detailed info on a specific ACL rule', [
    CLIArg('endpoint-id', required=True, help=(
        'ID of the endpoint, typically fetched from endpoint-search')),
    CLIArg('rule-id', required=True, help='ID of the rule to display')
    ])
def show_acl_rule(args):
    """
    Executor for `globus transfer access show-acl-rule`
    """
    client = get_client()

    res = client.get_endpoint_acl_rule(args.endpoint_id, args.rule_id)

    print(json.dumps(res.data, indent=2))


@cliargs('Add an ACL rule', [
    CLIArg('endpoint-id', required=True, help='ID of the endpoint'),
    CLIArg('permissions', required=True, choices=('r', 'rw'), type=str.lower,
           help='Permissions to add. Read-Only or Read/Write.'),
    CLIArg('principal', required=True,
           help='Principal to grant permissions to'),
    CLIArg('principal-type', required=True, choices=(
        'identity', 'group', 'anonymous', 'all_authenticated_users'),
        type=str.lower, help='Principal type to grant permissions to'),
    CLIArg('path', required=True,
           help='Path on which the rule grants permissions')
    ])
def add_acl_rule(args):
    """
    Executor for `globus transfer access add-acl-rule`
    """
    client = get_client()

    rule_data = {
        'DATA_TYPE': 'access',
        'permissions': args.permissions,
        'principal': args.principal,
        'principal_type': args.principal_type,
        'path': args.path
    }

    res = client.add_endpoint_acl_rule(args.endpoint_id, rule_data)

    print(json.dumps(res.data, indent=2))


@cliargs('Remove an ACL rule', [
    CLIArg('endpoint-id', required=True, help='ID of the endpoint'),
    CLIArg('rule-id', required=True, help='ID of the rule to display')
    ])
def del_acl_rule(args):
    """
    Executor for `globus transfer access del-acl-rule`
    """
    client = get_client()

    res = client.delete_endpoint_acl_rule(args.endpoint_id, args.rule_id)

    print(json.dumps(res.data, indent=2))


@cliargs('Update an ACL rule', [
    CLIArg('endpoint-id', required=True, help='ID of the endpoint'),
    CLIArg('rule-id', required=True, help='ID of the rule to display'),
    CLIArg('permissions', default=None, choices=('r', 'rw'), type=str.lower,
           help='Permissions to add. Read-Only or Read/Write.'),
    CLIArg('principal', default=None,
           help='Principal to grant permissions to'),
    CLIArg('principal-type', default=None, choices=(
        'identity', 'group', 'anonymous', 'all_authenticated_users'),
        type=str.lower, help='Principal type to grant permissions to'),
    CLIArg('path', default=None,
           help='Path on which the rule grants permissions')
    ])
def update_acl_rule(args):
    """
    Executor for `globus transfer access update-acl-rule`
    """
    client = get_client()

    rule_data = {
        'DATA_TYPE': 'access'
    }
    for key, val in (('permissions', args.permissions),
                     ('principal', args.principal),
                     ('principal_type', args.principal_type),
                     ('path', args.path)):
        if val is not None:
            rule_data[key] = val

    res = client.update_endpoint_acl_rule(args.endpoint_id, args.rule_id,
                                          rule_data)

    print(json.dumps(res.data, indent=2))
