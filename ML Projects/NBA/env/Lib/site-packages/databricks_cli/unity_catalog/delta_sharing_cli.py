# Databricks CLI
# Copyright 2022 Databricks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"), except
# that the use of services to which certain application programming
# interfaces (each, an "API") connect requires that the user first obtain
# a license for the use of the APIs from Databricks, Inc. ("Databricks"),
# by creating an account at www.databricks.com and agreeing to either (a)
# the Community Edition Terms of Service, (b) the Databricks Terms of
# Service, or (c) another written agreement between Licensee and Databricks
# for the use of the APIs.
#
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
from json import loads as json_loads

import click

from databricks_cli.click_types import JsonClickType
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.unity_catalog.api import UnityCatalogApi
from databricks_cli.unity_catalog.utils import hide, json_file_help, json_string_help, \
    mc_pretty_format
from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS, json_cli_base, \
    merge_dicts_shallow


##############  Share Commands  ##############


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Create a new share.')
@click.option('--name', required=True, help='Name of new share.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def create_share_cli(api_client, name):
    """
    Create a new share.
    """
    share_json = UnityCatalogApi(api_client).create_share(name)
    click.echo(mc_pretty_format(share_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List shares.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_shares_cli(api_client):
    """
    List shares.
    """
    shares_json = UnityCatalogApi(api_client).list_shares()
    click.echo(mc_pretty_format(shares_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get a share.')
@click.option('--name', required=True,
              help='Name of the share to get.')
@click.option('--include-shared-data', default=True,
              help='Whether to include shared data in the response.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_share_cli(api_client, name, include_shared_data):
    """
    Get a share.
    """
    share_json = UnityCatalogApi(api_client).get_share(name, include_shared_data)
    click.echo(mc_pretty_format(share_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List permissions on a share.')
@click.option('--name', required=True,
              help='Name of the share to list permissions on.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_share_permissions_cli(api_client, name):
    """
    List permissions on a share.
    """
    perms_json = UnityCatalogApi(api_client).list_share_permissions(name)
    click.echo(mc_pretty_format(perms_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Update permissions on a share.')
@click.option('--name', required=True,
              help='Name of the share whose permissions are updated.')
@click.option('--json-file', default=None, type=click.Path(),
              help=json_file_help(method='POST', path='/shares/{name}/permissions'))
@click.option('--json', default=None, type=JsonClickType(),
              help=json_string_help(method='POST', path='/shares/{name}/permissions'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def update_share_permissions_cli(api_client, name, json_file, json):
    """
    Update permissions on a share.

    The public specification for the JSON request is in development.
    """
    json_cli_base(json_file, json,
                  lambda json: UnityCatalogApi(api_client).update_share_permissions(name, json))

@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Update a share.')
@click.option('--name', required=True,
              help='Name of the share to update.')
@click.option('--new-name', default=None, help='New name of the share.')
@click.option('--comment', default=None, required=False,
              help='Free-form text description.')
@click.option('--owner', default=None, required=False,
              help='Owner of the share.')
# These options are hidden to encourage the usage of the new commands: add-table/update-table
@click.option('--add-table', default=None, multiple=True,
              metavar='NAME', hidden=True,
              help='Full name of table to add to share (can be specified multiple times).')
@click.option('--remove-table', default=None, multiple=True,
              metavar='NAME', hidden=True,
              help='Full name of table to remove from share (can be specified multiple times).')
@click.option('--json-file', default=None, type=click.Path(),
              help=json_file_help(method='PATCH', path='/shares/{name}'))
@click.option('--json', default=None, type=JsonClickType(),
              help=json_string_help(method='PATCH', path='/shares/{name}'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def update_share_cli(api_client, name, new_name, comment, owner,
                     add_table, remove_table, json_file, json):
    """
    Update a share.

    The public specification for the JSON request is in development.
    """
    if ((new_name is not None) or (comment is not None) or (owner is not None) or
        len(add_table) > 0 or len(remove_table) > 0):
        if (json_file is not None) or (json is not None):
            raise ValueError('Cannot specify JSON if any other update flags are specified')
        updates = []
        for a in add_table:
            updates.append({'action': 'ADD', 'data_object': shared_table_object(a)})
        for r in remove_table:
            updates.append({'action': 'REMOVE', 'data_object': shared_table_object(r)})
        data = {'name': new_name, 'comment': comment, 'owner': owner, 'updates': updates}
        share_json = UnityCatalogApi(api_client).update_share(name, data)
        click.echo(mc_pretty_format(share_json))
    else:
        json_cli_base(json_file, json,
                      lambda json: UnityCatalogApi(api_client).update_share(name, json))

def shared_schema_object(name=None, comment=None):
    val = {
        'data_object_type': 'SCHEMA'
    }
    if name is not None:
        val['name'] = name
    if comment is not None:
        val['comment'] = comment
    return val

def create_common_shared_schema_options(f):
    @click.option('--schema', default=None,
                  help='Full name of the shared schema.')
    @click.option('--comment', default=None,
                  help='New comment of the shared schema.')
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)
    return wrapper

@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Add a shared schema.')
@click.option('--share', required=True,
              help='Name of the share to update.')
@create_common_shared_schema_options
@click.option('--json-file', default=None, type=click.Path(),
              help="Adds a shared schema based on shared data object represented in JSON file.")
@click.option('--json', default=None, type=JsonClickType(),
              help="Adds a shared schema based on shared data object represented in JSON.")
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def add_share_schema_cli(api_client, share, schema, comment, json_file, json):
    """
    Adds a shared schema.

    The public specification for the JSON request is in development.
    """
    if (json_file is not None) or (json is not None):
        def api_call(d):
            if 'data_object_type' not in d or d['data_object_type'] != "SCHEMA":
                raise ValueError('Must specify data_object_type as "SCHEMA"')
            UnityCatalogApi(api_client).update_share(share, { 
                'updates': [
                    {
                        'action': 'ADD',
                        'data_object': d,
                    }
                ]
            })
        json_cli_base(json_file, json, api_call)
    else:
        if schema is None:
            raise ValueError("Must specify full schema name when adding shared schema")
        data = { 
            'updates': [
                {
                    'action': 'ADD',
                    'data_object': shared_schema_object(
                        name=schema,
                        comment=comment
                    )
                }
            ]
        }
        share_json = UnityCatalogApi(api_client).update_share(share, data)
        click.echo(mc_pretty_format(share_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Update a shared schema.')
@click.option('--share', required=True,
              help='Name of the share to update.')
@create_common_shared_schema_options
@click.option('--json-file', default=None, type=click.Path(),
              help="Updates the shared schema to shared data object represented in JSON file.")
@click.option('--json', default=None, type=JsonClickType(),
              help="Updates the shared schema to shared data object represented in JSON.")
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def update_share_schema_cli(api_client, share, schema, comment, json_file, json):
    """
    Updates a shared schema.

    The public specification for the JSON request is in development.
    """
    if (json_file is not None) or (json is not None):
        def api_call(d):
            if 'data_object_type' not in d or d['data_object_type'] != "SCHEMA":
                raise ValueError('Must specify data_object_type as "SCHEMA"')
            UnityCatalogApi(api_client).update_share(share, { 
                'updates': [
                    {
                        'action': 'UPDATE',
                        'data_object': d,
                    }
                ]
            })
        json_cli_base(json_file, json, api_call)
    else:
        if schema is None:
            raise ValueError("Must specify full schema name when updating shared schema")
        data = { 
            'updates': [
                {
                    'action': 'UPDATE',
                    'data_object': shared_schema_object(
                        name=schema,
                        comment=comment
                    )
                }
            ]
        }
        share_json = UnityCatalogApi(api_client).update_share(share, data)
        click.echo(mc_pretty_format(share_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Remove a shared schema.')
@click.option('--share', required=True,
              help='Name of the share to update.')
@click.option('--schema', default=None,
              help='Full name of the schema to remove from share.')
@click.option('--json-file', default=None, type=click.Path(),
              help="Removes the shared schema based on shared data object" + 
              "represented in JSON file.")
@click.option('--json', default=None, type=JsonClickType(),
              help="Removes the shared schema based on shared data object represented in JSON.")
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def remove_share_schema_cli(api_client, share, schema, json_file, json):
    """
    Removes a shared schema by full schema name.

    The public specification for the JSON request is in development.
    """
    if (json_file is not None) or (json is not None):
        def api_call(d):
            if 'data_object_type' not in d or d['data_object_type'] != "SCHEMA":
                raise ValueError('Must specify data_object_type as "SCHEMA"')
            UnityCatalogApi(api_client).update_share(share, { 
                'updates': [
                    {
                        'action': 'REMOVE',
                        'data_object': d,
                    }
                ]
            })
        json_cli_base(json_file, json, api_call)
    else:
        if schema is None:
            raise ValueError("Must specify full schema name when removing shared schema")
        data = { 
            'updates': [
                {
                    'action': 'REMOVE',
                    'data_object': shared_schema_object(
                        name=schema,
                    )
                }
            ]
        }
        share_json = UnityCatalogApi(api_client).update_share(share, data)
        click.echo(mc_pretty_format(share_json))
        

def shared_table_object(name=None, comment=None, shared_as=None, 
                       cdf_enabled=None, partitions=None, start_version=None):
    val = {
        'data_object_type': 'TABLE'
    }
    if name is not None:
        val['name'] = name
    if comment is not None:
        val['comment'] = comment
    if shared_as is not None:
        val['shared_as'] = shared_as
    if cdf_enabled is not None:
        val['cdf_enabled'] = cdf_enabled
    if partitions is not None:
        val['partitions'] = partitions
    if start_version is not None:
        val['start_version'] = start_version
    return val

def create_common_shared_table_options(f):
    @click.option('--table', default=None,
                  help='Full name of the shared table.')
    @click.option('--shared-as', default=None,
                  help='New name of the table to be shared as.')
    @click.option('--comment', default=None,
                  help='New comment of the shared table.')
    @click.option('--partitions', default=None, type=JsonClickType(),
                  help='New partition specification of the shared table represented in JSON.')
    @click.option('--cdf/--no-cdf', is_flag=True, default=None,
                  help='Toggles the change data feed for the shared table.')
    @click.option('--start-version', default=None, type=int,
                  help='Specifies the current version of the shared table.')
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)
    return wrapper


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Add a shared table.')
@click.option('--share', required=True,
              help='Name of the share to update.')
@create_common_shared_table_options
@click.option('--json-file', default=None, type=click.Path(),
              help="Adds a shared table based on shared data object represented in JSON file.")
@click.option('--json', default=None, type=JsonClickType(),
              help="Adds a shared table based on shared data object represented in JSON.")
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def add_share_table_cli(api_client, share, table, shared_as, comment,
                        partitions, cdf, start_version, json_file, json):
    """
    Adds a shared table.

    The public specification for the JSON request is in development.
    """
    if (json_file is not None) or (json is not None):
        def api_call(d):
            if 'data_object_type' in d and d['data_object_type'] != "TABLE":
                raise ValueError('Must specify data_object_type as "TABLE" '
                                 'or not specify data_object_type at all')
            UnityCatalogApi(api_client).update_share(share, { 
                'updates': [
                    {
                        'action': 'REMOVE',
                        'data_object': d,
                    }
                ]
            })
        json_cli_base(json_file, json, api_call)
    else:
        if table is None:
            raise ValueError('Must specify table name when adding shared table')
        data = { 
            'updates': [
                {
                    'action': 'ADD',
                    'data_object': shared_table_object(
                        name=table,
                        shared_as=shared_as,
                        comment=comment,
                        cdf_enabled=cdf,
                        partitions=json_loads(partitions) if partitions is not None else None,
                        start_version=start_version,
                    )
                }
            ]
        }
        share_json = UnityCatalogApi(api_client).update_share(share, data)
        click.echo(mc_pretty_format(share_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Update a shared table.')
@click.option('--share', required=True,
              help='Name of the share to update.')
@create_common_shared_table_options
@click.option('--json-file', default=None, type=click.Path(),
              help="Updates the shared table to shared data object represented in JSON file.")
@click.option('--json', default=None, type=JsonClickType(),
              help="Updates the shared table to shared data object represented in JSON.")
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def update_share_table_cli(api_client, share, table, shared_as, comment,
                           partitions, cdf, start_version, json_file, json):
    """
    Updates a shared table.

    The public specification for the JSON request is in development.
    """
    if (json_file is not None) or (json is not None):
        def api_call(d):
            if 'data_object_type' in d and d['data_object_type'] != "TABLE":
                raise ValueError('Must specify data_object_type as "TABLE" '
                                 'or not specify data_object_type at all')
            UnityCatalogApi(api_client).update_share(share, { 
                'updates': [
                    {
                        'action': 'UPDATE',
                        'data_object': d,
                    }
                ]
            })
        json_cli_base(json_file, json, api_call)
    else:
        if table is None:
            raise ValueError('Must specify table name when updating shared table')
        data = { 
            'updates': [
                {
                    'action': 'UPDATE',
                    'data_object': shared_table_object(
                        name=table,
                        shared_as=shared_as,
                        comment=comment,
                        cdf_enabled=cdf,
                        partitions=json_loads(partitions) if partitions is not None else None,
                        start_version=start_version,
                    )
                }
            ]
        }
        share_json = UnityCatalogApi(api_client).update_share(share, data)
        click.echo(mc_pretty_format(share_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Remove a shared table.')
@click.option('--share', required=True,
              help='Name of the share to update.')
@click.option('--table', default=None,
              help='Full name of the table to remove from share.')
@click.option('--shared-as', default=None,
              help='New name of the table inside the share.')
@click.option('--json-file', default=None, type=click.Path(),
              help="Removes the shared table based on shared data object represented in JSON file.")
@click.option('--json', default=None, type=JsonClickType(),
              help="Removes the shared table based on shared data object represented in JSON.")
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def remove_share_table_cli(api_client, share, table, shared_as, json_file, json):
    """
    Removes a shared table either by table name or the shared-as table name.

    The public specification for the JSON request is in development.
    """
    if table is not None and shared_as is not None:
        raise ValueError("You can only pass in either --table or --shared_as and not both.")

    if (json_file is not None) or (json is not None):
        def api_call(d):
            if 'data_object_type' in d and d['data_object_type'] != "TABLE":
                raise ValueError('Must specify data_object_type as "TABLE" '
                                 'or not specify data_object_type at all')
            UnityCatalogApi(api_client).update_share(share, { 
                'updates': [
                    {
                        'action': 'REMOVE',
                        'data_object': d,
                    }
                ]
            })
        json_cli_base(json_file, json, api_call)
    else:
        if table is None and shared_as is None:
            raise ValueError('Must specify full or shared as table name when removing shared table')
        data = { 
            'updates': [
                {
                    'action': 'REMOVE',
                    'data_object': shared_table_object(
                        name=table,
                        shared_as=shared_as,
                    )
                }
            ]
        }
        share_json = UnityCatalogApi(api_client).update_share(share, data)
        click.echo(mc_pretty_format(share_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Delete a share.')
@click.option('--name', required=True,
              help='Name of the share to delete.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_share_cli(api_client, name):
    """
    Delete a share.
    """
    UnityCatalogApi(api_client).delete_share(name)


##############  Recipient Commands  ##############

def parse_recipient_custom_properties(custom_property_list):
    custom_properties = []
    for property_str in custom_property_list:
        tokens = property_str.split('=', 2)
        if len(tokens) != 2:
            raise ValueError('Invalid format for property. '
                             + 'The format should be <key>=<value>.')
        custom_properties.append({"key": tokens[0], "value": tokens[1]})
    return custom_properties    


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Create a new recipient.')
@click.option('--name', required=True, help='Name of new recipient.')
@click.option('--comment', default=None, required=False,
              help='Free-form text description.')
@click.option('--sharing-id', default=None, required=False,
              help='The sharing identifier provided by the data recipient offline.')
@click.option('--allowed-ip-address', default=None, required=False, multiple=True,
              help=(
                  'IP address in CIDR notation that is allowed to use delta sharing. '
                  '(can be specified multiple times).'))
@click.option('--property', 'custom_property', default=None, required=False, multiple=True,
              help=(
                  'Properties of the recipient. Key and value should be provided '
                  'at the same time separated by an equal sign. '
                  'Example: --property country=US.'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def create_recipient_cli(api_client, name, comment, sharing_id,
                         allowed_ip_address, custom_property):
    """
    Create a new recipient.
    """
    recipient_json = UnityCatalogApi(api_client).create_recipient(
        name, comment, sharing_id,
        allowed_ip_address, parse_recipient_custom_properties(custom_property))
    click.echo(mc_pretty_format(recipient_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List recipients.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_recipients_cli(api_client):
    """
    List recipients.
    """
    recipients_json = UnityCatalogApi(api_client).list_recipients()
    click.echo(mc_pretty_format(recipients_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get a recipient.')
@click.option('--name', required=True,
              help='Name of the recipient to get.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_recipient_cli(api_client, name):
    """
    Get a recipient.
    """
    recipient_json = UnityCatalogApi(api_client).get_recipient(name)
    click.echo(mc_pretty_format(recipient_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Update a recipient.')
@click.option('--name', required=True,
              help='Name of the recipient who needs to be updated.')
@click.option('--new-name', default=None, help='New name of the recipient.')
@click.option('--comment', default=None, required=False,
              help='Free-form text description.')
@click.option('--owner', default=None, required=False,
              help='Owner of the recipient.')
@click.option('--allowed-ip-address', default=None, required=False, multiple=True,
              help=(
                  'IP address in CIDR notation that is allowed to use delta sharing '
                  '(can be specified multiple times). Specify a single empty string to disable '
                  'IP allowlist.'))
@click.option('--property', 'custom_property', default=None, required=False, multiple=True,
              help=(
                  'Properties of the recipient. Key and value should be provided '
                  'at the same time separated by an equal sign. '
                  'Example: --property country=US. '
                  'Specify a single empty string to remove all properties.'))
@click.option('--json-file', default=None, type=click.Path(),
              help=json_file_help(method='PATCH', path='/recipients/{name}'))
@click.option('--json', default=None, type=JsonClickType(),
              help=json_string_help(method='PATCH', path='/recipients/{name}'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def update_recipient_cli(api_client, name, new_name, comment, owner,
                         allowed_ip_address, custom_property, json_file, json):
    """
    Update a recipient.

    The public specification for the JSON request is in development.
    """
    if ((new_name is not None) or (comment is not None) or (owner is not None) or
        len(allowed_ip_address) or len(custom_property) > 0):
        if (json_file is not None) or (json is not None):
            raise ValueError('Cannot specify JSON if any other update flags are specified')
        data = {'name': new_name, 'comment': comment, 'owner': owner}
        if len(allowed_ip_address) > 0:
            data['ip_access_list'] = {}
            if len(allowed_ip_address) != 1 or allowed_ip_address[0] != '':
                data['ip_access_list']['allowed_ip_addresses'] = allowed_ip_address
        if len(custom_property) > 0:
            data['properties_kvpairs'] = {}
            if len(custom_property) != 1 or custom_property[0] != '':
                data['properties_kvpairs']['properties'] = parse_recipient_custom_properties(
                    custom_property)
        recipient_json = UnityCatalogApi(api_client).update_recipient(name, data)
        click.echo(mc_pretty_format(recipient_json))
    else:
        json_cli_base(json_file, json,
                      lambda json: UnityCatalogApi(api_client).update_recipient(name, json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Rotate token for the recipient.')
@click.option('--name', required=True, help='Name of new recipient.')
@click.option('--existing-token-expire-in-seconds', default=None, required=False,
              type=int,
              help='Expire the existing token in number of seconds from now,' +
                   ' 0 to expire it immediately.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def rotate_recipient_token_cli(api_client, name, existing_token_expire_in_seconds):
    """
    Rotate recipient token.
    """
    recipient_json = \
        UnityCatalogApi(api_client).rotate_recipient_token(name, existing_token_expire_in_seconds)
    click.echo(mc_pretty_format(recipient_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List share permissions of a recipient.')
@click.option('--name', required=True,
              help='Name of the recipient.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_recipient_permissions_cli(api_client, name):
    """
    List a recipient's share permissions.
    """
    recipient_json = UnityCatalogApi(api_client).get_recipient_share_permissions(name)
    click.echo(mc_pretty_format(recipient_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Delete a recipient.')
@click.option('--name', required=True,
              help='Name of the recipient to delete.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_recipient_cli(api_client, name):
    """
    Delete a recipient.
    """
    UnityCatalogApi(api_client).delete_recipient(name)


##############  Provider Commands  ##############

@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Create a provider.')
@click.option('--name', required=True, help='Name of the new provider.')
@click.option('--comment', default=None, required=False,
              help='Free-form text description.')
@click.option('--recipient-profile-json-file', default=None, required=False, type=click.Path(),
              help='File containing recipient profile in JSON format.')
@click.option('--recipient-profile-json', default=None, required=False, type=JsonClickType(),
              help='JSON string containing recipient profile.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def create_provider_cli(api_client, name, comment, recipient_profile_json_file,
                        recipient_profile_json):
    """
    Create a provider.

    The public specification for the JSON request is in development.
    """
    json_cli_base(recipient_profile_json_file, recipient_profile_json,
                  lambda json: UnityCatalogApi(api_client).create_provider(name, comment, json),
                  error_msg='Either --recipient-profile-json-file or ' +
                  '--recipient-profile-json should be provided')


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List providers.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_providers_cli(api_client):
    """
    List providers.
    """
    proviers_json = UnityCatalogApi(api_client).list_providers()
    click.echo(mc_pretty_format(proviers_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get a provider.')
@click.option('--name', required=True,
              help='Name of the provider to get.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_provider_cli(api_client, name):
    """
    Get a provider.
    """
    provier_json = UnityCatalogApi(api_client).get_provider(name)
    click.echo(mc_pretty_format(provier_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Update a provider.')
@click.option('--name', required=True, help='Name of the provider to update.')
@click.option('--new-name', default=None, help='New name of the provider.')
@click.option('--comment', default=None, required=False,
              help='Free-form text description.')
@click.option('--owner', default=None, required=False,
              help='Owner of the provider.')
@click.option('--recipient-profile-json-file', default=None, type=click.Path(),
              help='File containing recipient profile in JSON format.')
@click.option('--recipient-profile-json', default=None, type=JsonClickType(),
              help='JSON string containing recipient profile.')
@click.option('--json-file', default=None, type=click.Path(),
              help=json_file_help(method='PATCH', path='/providers/{name}'))
@click.option('--json', default=None, type=JsonClickType(),
              help=json_string_help(method='PATCH', path='/providers/{name}'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def update_provider_cli(api_client, name, new_name, comment, owner, recipient_profile_json_file,
                        recipient_profile_json, json_file, json):
    """
    Update a provider.

    The public specification for the JSON request is in development.
    """
    if ((new_name is not None) or (comment is not None) or (owner is not None) or
        (recipient_profile_json_file is not None) or (recipient_profile_json) is not None):
        if (json_file is not None) or (json is not None):
            raise ValueError('Cannot specify JSON if any other update flags are specified')
        data = {'name': new_name, 'comment': comment, 'owner': owner}

        if (recipient_profile_json_file is None) and (recipient_profile_json is None):
            provider_json = UnityCatalogApi(api_client).update_provider(name, provider_spec=data)
            click.echo(mc_pretty_format(provider_json))
        else:
            json_cli_base(recipient_profile_json_file, recipient_profile_json,
                          lambda profile_json: UnityCatalogApi(api_client).update_provider(
                              name,
                              provider_spec=merge_dicts_shallow(
                                  data,
                                  {'recipient_profile_str': mc_pretty_format(profile_json)})),
                          error_msg='Either --recipient-profile-json-file or ' +
                          '--recipient-profile-json should be provided')
    else:
        json_cli_base(json_file, json,
                      lambda json: UnityCatalogApi(api_client).update_provider(
                          name, provider_spec=json))
            

@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List shares of a provider.')
@click.option('--name', required=True,
              help='Name of the provider.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_provider_shares_cli(api_client, name):
    """
    List a provider's shares.
    """
    shares_json = UnityCatalogApi(api_client).list_provider_shares(name)
    click.echo(mc_pretty_format(shares_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Delete a provider.')
@click.option('--name', required=True,
              help='Name of the provider to delete.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_provider_cli(api_client, name):
    """
    Delete a provider.
    """
    UnityCatalogApi(api_client).delete_provider(name)


@click.group()
def shares_group():  # pragma: no cover
    pass


def register_shares_commands(cmd_group):
    # Register deprecated "verb-noun" commands for backward compatibility.
    cmd_group.add_command(hide(create_share_cli), name='create-share')
    cmd_group.add_command(hide(list_shares_cli), name='list-shares')
    cmd_group.add_command(hide(get_share_cli), name='get-share')
    cmd_group.add_command(hide(update_share_cli), name='update-share')
    cmd_group.add_command(hide(delete_share_cli), name='delete-share')
    cmd_group.add_command(hide(list_share_permissions_cli), name='list-share-permissions')
    cmd_group.add_command(hide(update_share_permissions_cli), name='update-share-permissions')

    # Register command group.
    shares_group.add_command(create_share_cli, name='create')
    shares_group.add_command(list_shares_cli, name='list')
    shares_group.add_command(get_share_cli, name='get')
    shares_group.add_command(update_share_cli, name='update')
    shares_group.add_command(add_share_schema_cli, name='add-schema')
    shares_group.add_command(update_share_schema_cli, name='update-schema')
    shares_group.add_command(remove_share_schema_cli, name='remove-schema')
    shares_group.add_command(add_share_table_cli, name='add-table')
    shares_group.add_command(update_share_table_cli, name='update-table')
    shares_group.add_command(remove_share_table_cli, name='remove-table')
    shares_group.add_command(delete_share_cli, name='delete')
    shares_group.add_command(list_share_permissions_cli, name='list-permissions')
    shares_group.add_command(update_share_permissions_cli, name='update-permissions')
    cmd_group.add_command(shares_group, name='shares')


@click.group()
def recipients_group():  # pragma: no cover
    pass


def register_recipients_commands(cmd_group):
    # Register deprecated "verb-noun" commands for backward compatibility.
    cmd_group.add_command(hide(create_recipient_cli), name='create-recipient')
    cmd_group.add_command(hide(list_recipients_cli), name='list-recipients')
    cmd_group.add_command(hide(get_recipient_cli), name='get-recipient')
    cmd_group.add_command(hide(update_recipient_cli), name='update-recipient')
    cmd_group.add_command(hide(rotate_recipient_token_cli), name='rotate-recipient-token')
    cmd_group.add_command(hide(list_recipient_permissions_cli), name='list-recipient-permissions')
    cmd_group.add_command(hide(delete_recipient_cli), name='delete-recipient')

    # Register command group.
    recipients_group.add_command(create_recipient_cli, name='create')
    recipients_group.add_command(list_recipients_cli, name='list')
    recipients_group.add_command(get_recipient_cli, name='get')
    recipients_group.add_command(update_recipient_cli, name='update')
    recipients_group.add_command(rotate_recipient_token_cli, name='rotate-token')
    recipients_group.add_command(list_recipient_permissions_cli, name='list-permissions')
    recipients_group.add_command(delete_recipient_cli, name='delete')
    cmd_group.add_command(recipients_group, name='recipients')


@click.group()
def providers_group():  # pragma: no cover
    pass


def register_providers_commands(cmd_group):
    # Register deprecated "verb-noun" commands for backward compatibility.
    cmd_group.add_command(hide(create_provider_cli), name='create-provider')
    cmd_group.add_command(hide(list_providers_cli), name='list-providers')
    cmd_group.add_command(hide(get_provider_cli), name='get-provider')
    cmd_group.add_command(hide(update_provider_cli), name='update-provider')
    cmd_group.add_command(hide(delete_provider_cli), name='delete-provider')
    cmd_group.add_command(hide(list_provider_shares_cli), name='list-provider-shares')

    # Register command group.
    providers_group.add_command(create_provider_cli, name='create')
    providers_group.add_command(list_providers_cli, name='list')
    providers_group.add_command(get_provider_cli, name='get')
    providers_group.add_command(update_provider_cli, name='update')
    providers_group.add_command(delete_provider_cli, name='delete')
    providers_group.add_command(list_provider_shares_cli, name='list-shares')
    cmd_group.add_command(providers_group, name='providers')


def register_delta_sharing_commands(cmd_group):
    register_shares_commands(cmd_group)
    register_recipients_commands(cmd_group)
    register_providers_commands(cmd_group)
