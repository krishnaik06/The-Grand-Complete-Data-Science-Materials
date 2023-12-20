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

from databricks_cli.click_types import JsonClickType
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.unity_catalog.api import UnityCatalogApi
from databricks_cli.unity_catalog.utils import hide, json_file_help, json_string_help, \
    mc_pretty_format
from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS, json_cli_base


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Create a table. [DO NOT USE]',
               hidden=True)
@click.option('--json-file', default=None, type=click.Path(),
              help=json_file_help(method='POST', path='/tables'))
@click.option('--json', default=None, type=JsonClickType(),
              help=json_string_help(method='POST', path='/tables'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def create_table_cli(api_client, json_file, json):
    """
    Create new table specified by the JSON input.

    WARNING: Creating table metadata via the UC API may create a table
    that is unusable in DBR. Instead, use SQL commands (CREATE TABLE) in DBR.

    The public specification for the JSON request is in development.
    """
    json_cli_base(json_file, json,
                  lambda json: UnityCatalogApi(api_client).create_table(json),
                  encode_utf8=True)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List tables.')
@click.option('--catalog-name', required=True,
              help='Name of the parent catalog for tables of interest.')
@click.option('--schema-name', required=True,
              help='Name of the parent schema for tables of interest.')
@click.option('--name-pattern', default=None,
              help='SQL LIKE pattern that the table name must match to be in list.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_tables_cli(api_client, catalog_name, schema_name, name_pattern):
    """
    List tables.
    """
    tables_json = UnityCatalogApi(api_client).list_tables(catalog_name, schema_name, name_pattern)
    click.echo(mc_pretty_format(tables_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List table summaries.')
@click.option('--catalog-name', required=True,
              help='Name of the parent catalog for tables of interest.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_table_summaries_cli(api_client, catalog_name):
    """
    List table summaries (in bulk).
    """
    tables_json = UnityCatalogApi(api_client).list_table_summaries(catalog_name)
    click.echo(mc_pretty_format(tables_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get a table.')
@click.option('--full-name', required=True,
              help='Full name (<catalog>.<schema>.<table>) of the table to get.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_table_cli(api_client, full_name):
    """
    Get a table.
    """
    table_json = UnityCatalogApi(api_client).get_table(full_name)
    click.echo(mc_pretty_format(table_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Update a table. [DO NOT USE]',
               hidden=True)
@click.option('--full-name', required=True,
              help='Full name (<catalog>.<schema>.<table>) of the table to update.')
@click.option('--json-file', default=None, type=click.Path(),
              help=json_file_help(method='PATCH', path='/tables/{name}'))
@click.option('--json', default=None, type=JsonClickType(),
              help=json_string_help(method='PATCH', path='/tables/{name}'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def update_table_cli(api_client, full_name, json_file, json):
    """
    Update a table.

    WARNING: Altering table metadata via the UC API may cause the table
    to be unusable in DBR. Instead, use SQL commands (ALTER TABLE) in DBR.

    The public specification for the JSON request is in development.
    """
    json_cli_base(json_file, json,
                  lambda json: UnityCatalogApi(api_client).update_table(full_name, json),
                  encode_utf8=True)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Delete a table.')
@click.option('--full-name', required=True,
              help='Full name (<catalog>.<schema>.<table>) of the table to delete.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_table_cli(api_client, full_name):
    """
    Delete a table.
    """
    UnityCatalogApi(api_client).delete_table(full_name)


@click.group(context_settings=CONTEXT_SETTINGS,
             short_help=' ',
             help='Note:\n' +
                  'To create or update tables, use SQL commands\n' +
                  '(CREATE TABLE or ALTER TABLE) on a cluster or SQL warehouse.')
def tables_group():  # pragma: no cover
    pass


def register_table_commands(cmd_group):
    # Register deprecated "verb-noun" commands for backward compatibility.
    cmd_group.add_command(hide(create_table_cli), name='create-table')
    cmd_group.add_command(hide(list_tables_cli), name='list-tables')
    cmd_group.add_command(hide(list_table_summaries_cli), name='list-table-summaries')
    cmd_group.add_command(hide(get_table_cli), name='get-table')
    cmd_group.add_command(hide(update_table_cli), name='update-table')
    cmd_group.add_command(hide(delete_table_cli), name='delete-table')

    # Register command group.
    tables_group.add_command(create_table_cli, name='create')
    tables_group.add_command(list_tables_cli, name='list')
    tables_group.add_command(list_table_summaries_cli, name='list-summaries')
    tables_group.add_command(get_table_cli, name='get')
    tables_group.add_command(update_table_cli, name='update')
    tables_group.add_command(delete_table_cli, name='delete')
    cmd_group.add_command(tables_group, name='tables')
