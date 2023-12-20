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

import click

from databricks_cli.click_types import JsonClickType, OneOfOption
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.unity_catalog.api import UnityCatalogApi
from databricks_cli.unity_catalog.utils import hide, json_file_help, json_string_help, \
    mc_pretty_format
from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS, json_cli_base


PERMISSIONS_OBJ_TYPES = [
    'metastore', 'catalog', 'schema', 'table', 'storage-credential', 'external-location'
]


def _get_perm_securable_name_and_type(metastore_id, catalog_name, schema_full_name,
                                      table_full_name, credential_name, location_name):
    if metastore_id:
        return ('metastore', metastore_id)
    elif catalog_name:
        return ('catalog', catalog_name)
    elif schema_full_name:
        return ('schema', schema_full_name)
    elif table_full_name:
        return ('table', table_full_name)
    elif credential_name:
        return ('storage-credential', credential_name)
    else:
        return ('external-location', location_name)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get permissions on a securable.')
@click.option('--metastore', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='ID of metastore of interest')
@click.option('--catalog', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='Name of catalog of interest')
@click.option('--schema', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='Full name of schema of interest')
@click.option('--table', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='Full name of table of interest')
@click.option('--storage-credential', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='Name of the storage credential of interest')
@click.option('--external-location', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='Name of the external location of interest')
@click.option('--effective', is_flag=True, default=False,
              help='Get effective permissions (including inherited privileges)')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_permissions_cli(api_client, metastore, catalog, schema, table, storage_credential,
                        external_location, effective):
    """
    Get permissions on a securable.
    """
    sec_type, sec_name = _get_perm_securable_name_and_type(metastore, catalog, schema, table,
                                                           storage_credential, external_location)

    if effective:
        perm_json = UnityCatalogApi(api_client).get_effective_permissions(sec_type, sec_name)
    else:
        perm_json = UnityCatalogApi(api_client).get_permissions(sec_type, sec_name)
    click.echo(mc_pretty_format(perm_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='update permissions on a securable.')
@click.option('--metastore', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='ID of metastore of interest')
@click.option('--catalog', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='Name of catalog of interest')
@click.option('--schema', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='Full name of schema of interest')
@click.option('--table', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='Full name of table of interest')
@click.option('--storage-credential', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='Name of the storage credential of interest')
@click.option('--external-location', cls=OneOfOption, default=None,
              one_of=PERMISSIONS_OBJ_TYPES,
              help='Name of the external location of interest')
@click.option('--json-file', default=None, type=click.Path(),
              help=json_file_help(method='PATCH', path='/permissions/{securable}/{id}'))
@click.option('--json', default=None, type=JsonClickType(),
              help=json_string_help(method='PATCH', path='/permissions/{securable}/{id}'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def update_permissions_cli(api_client, metastore, catalog, schema, table, storage_credential,
                           external_location, json_file, json):
    """
    Update permissions on a securable.

    The public specification for the JSON request is in development.
    """
    sec_type, sec_name = _get_perm_securable_name_and_type(metastore, catalog, schema, table,
                                                           storage_credential, external_location)

    json_cli_base(json_file, json,
                  lambda json: UnityCatalogApi(api_client).update_permissions(sec_type, sec_name,
                                                                              json),
                  encode_utf8=True)


@click.group()
def permissions_group():  # pragma: no cover
    pass


def register_perms_commands(cmd_group):
    # Register deprecated "verb-noun" commands for backward compatibility.
    cmd_group.add_command(hide(get_permissions_cli), name='get-permissions')
    cmd_group.add_command(hide(update_permissions_cli), name='update-permissions')

    # Register command group.
    permissions_group.add_command(get_permissions_cli, name='get')
    permissions_group.add_command(update_permissions_cli, name='update')
    cmd_group.add_command(permissions_group, name='permissions')
