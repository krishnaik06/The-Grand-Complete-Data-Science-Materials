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
               short_help='Create a new schema.')
@click.option('--catalog-name', required=True, help='Parent catalog of new schema.')
@click.option('--name', required=True,
              help='Name of new schema, relative to parent catalog.')
@click.option('--comment', default=None, required=False,
              help='Free-form text description.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def create_schema_cli(api_client, catalog_name, name, comment):
    """
    Create a new schema in the specified catalog.
    """
    schema_json = UnityCatalogApi(api_client).create_schema(catalog_name, name, comment)
    click.echo(mc_pretty_format(schema_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List schemas.')
@click.option('--catalog-name', required=True,
              help='Name of the parent catalog for schemas of interest.')
@click.option('--name-pattern', default=None,
              help='SQL LIKE pattern that the schema name must match to be in list.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_schemas_cli(api_client, catalog_name, name_pattern):
    """
    List schemas.
    """
    schemas_json = UnityCatalogApi(api_client).list_schemas(catalog_name, name_pattern)
    click.echo(mc_pretty_format(schemas_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get a schema.')
@click.option('--full-name', required=True,
              help='Full name (<catalog>.<schema>) of the schema to get.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_schema_cli(api_client, full_name):
    """
    Get a schema.
    """
    schema_json = UnityCatalogApi(api_client).get_schema(full_name)
    click.echo(mc_pretty_format(schema_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Update a schema.')
@click.option('--full-name', required=True,
              help='Full name (<catalog>.<schema>) of the schema to update.')
@click.option('--json-file', default=None, type=click.Path(),
              help=json_file_help(method='PATCH', path='/schemas/{name}'))
@click.option('--json', default=None, type=JsonClickType(),
              help=json_string_help(method='PATCH', path='/schemas/{name}'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def update_schema_cli(api_client, full_name, json_file, json):
    """
    Update a schema.

    The public specification for the JSON request is in development.
    """
    json_cli_base(json_file, json,
                  lambda json: UnityCatalogApi(api_client).update_schema(full_name, json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Delete a schema.')
@click.option('--full-name', required=True,
              help='Full name (<catalog>.<schema>) of the schema to delete.')
@click.option('--purge', '-p', is_flag=True, default=False,
              help='Purge all child schemas and tables of catalog.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_schema_cli(api_client, full_name, purge):
    """
    Delete a schema.
    """
    if purge:
        (catalog_name, schema_name) = full_name.split('.')
        click.echo("Purging all tables from schema %s in catalog %s" % (schema_name, catalog_name))

        tables_response = UnityCatalogApi(api_client).list_tables(catalog_name, schema_name, None)
        for t in tables_response['tables']:
            click.echo("Deleting table: %s" % (t['full_name']))
            UnityCatalogApi(api_client).delete_table(t['full_name'])

    UnityCatalogApi(api_client).delete_schema(full_name)


@click.group()
def schemas_group():  # pragma: no cover
    pass


def register_schema_commands(cmd_group):
    # Register deprecated "verb-noun" commands for backward compatibility.
    cmd_group.add_command(hide(create_schema_cli), name='create-schema')
    cmd_group.add_command(hide(list_schemas_cli), name='list-schemas')
    cmd_group.add_command(hide(get_schema_cli), name='get-schema')
    cmd_group.add_command(hide(update_schema_cli), name='update-schema')
    cmd_group.add_command(hide(delete_schema_cli), name='delete-schema')

    # Register command group.
    schemas_group.add_command(create_schema_cli, name='create')
    schemas_group.add_command(list_schemas_cli, name='list')
    schemas_group.add_command(get_schema_cli, name='get')
    schemas_group.add_command(update_schema_cli, name='update')
    schemas_group.add_command(delete_schema_cli, name='delete')
    cmd_group.add_command(schemas_group, name='schemas')
