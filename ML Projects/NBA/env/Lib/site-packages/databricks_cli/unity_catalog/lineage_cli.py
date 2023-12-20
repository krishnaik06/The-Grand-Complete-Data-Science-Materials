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

from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.unity_catalog.api import UnityCatalogApi
from databricks_cli.unity_catalog.utils import mc_pretty_format, hide
from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS, to_graph


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List table lineage.')
@click.option('--table-name', required=True,
              help='Name of the table with 3L namespace')
@click.option('--level', required=False, type=int, default=1,
              help='level of lineage to retrieve')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_table_lineages_cli(api_client, table_name, level):
    """
    List table lineage by table name.
    :table_name str: name of the table with 3L format. E.g catalog.schema.table

    example response:

    digraph "lineage graph of main.lineage.user_account" {
        "main.lineage.user_account" -> "main.lineage.user_transaction";
        "main.lineage.dinner_price" -> "main.lineage.price_entry","main.lineage.user_account";
    }

    Returns the specified levels of downstream/upstream

    """
    node_to_downstream = list_table_lineages_recursive_cli(api_client, table_name, level)
    click.echo(to_graph(node_to_downstream, "lineage graph of {}".format(table_name)))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List column lineage.')
@click.option('--table-name', required=True,
              help='Name of the table with 3L namespace')
@click.option('--column-name', required=True,
              help='Name of the column for lineage analysis')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_column_lineages_cli(api_client, table_name, column_name):
    """
    List column lineage by table name and column name.
    :table_name str: name of the table with 3L format. E.g catalog.schema.table
    :column_name str: name of the column

    example response:
    {
      "downstream_cols": [
        {
          "workspace_id": 6051921418418893,
          "table_type": "TABLE",
          "catalog_name": "main",
          "table_name": "dinner_price",
          "schema_name": "lineage",
          "name": "full_menu"
        }
      ],
      "upstream_cols": [
        {
          "workspace_id": 6051921418418893,
          "table_type": "TABLE",
          "catalog_name": "main",
          "table_name": "menu",
          "schema_name": "lineage",
          "name": "app"
        },
        {
          "workspace_id": 6051921418418893,
          "table_type": "TABLE",
          "catalog_name": "main",
          "table_name": "menu",
          "schema_name": "lineage",
          "name": "desert"
        },
        {
          "workspace_id": 6051921418418893,
          "table_type": "TABLE",
          "catalog_name": "main",
          "table_name": "menu",
          "schema_name": "lineage",
          "name": "main"
        }
      ]
    }

    Returns the downstream/upstream of a given column
    """

    schemas_json = UnityCatalogApi(api_client).list_lineages_by_column(table_name, column_name)
    click.echo(mc_pretty_format(schemas_json))


@click.group()
def lineage_group():  # pragma: no cover
    pass


def register_lineage_commands(cmd_group):
    # Register deprecated "verb-noun" commands for backward compatibility.
    cmd_group.add_command(hide(list_table_lineages_cli), name='list-table-lineages')
    cmd_group.add_command(hide(list_column_lineages_cli), name='list-column-lineages')

    # Register command group.
    # Note: we deviate from the "noun-verb" pattern here because it would be awkward to have to
    # spell out "list" or "list-for". Table and column lineage is read only by definition.
    lineage_group.add_command(list_table_lineages_cli, name='table')
    lineage_group.add_command(list_column_lineages_cli, name='column')
    cmd_group.add_command(lineage_group, name='lineage')


def get_table_name(table_node):
    return "{}.{}.{}".format(
        table_node['catalog_name'],
        table_node['schema_name'],
        table_node['name']
    )


def list_table_lineages_recursive_cli(api_client, table_name, level):
    node_to_downstream = {}
    level_count = 0
    current_level = [table_name]
    next_level = []
    initial_upstream = []
    # go downstream
    while level_count < level:
        for current_table in current_level:
            if current_table in node_to_downstream:
                # skip if the table is visited before
                continue
            lineage_json = UnityCatalogApi(api_client).list_lineages_by_table(current_table)
            if level == 0:
                initial_upstream = [
                    get_table_name(
                        table_node
                    ) for table_node in lineage_json['upstream_tables']
                ] if 'upstream_tables' in lineage_json else []
            cur_downstream = [
                get_table_name(
                    table_node
                ) for table_node in lineage_json['downstream_tables']
            ] if 'downstream_tables' in lineage_json else []
            next_level.extend(cur_downstream)
            if len(cur_downstream) > 0:
                node_to_downstream[current_table] = cur_downstream
        level_count = level_count + 1
        current_level = next_level
        next_level = []
    # go upstream
    level_count = 1
    current_level = initial_upstream
    connect_upstream_tables(initial_upstream, table_name, node_to_downstream)
    next_level = []
    while level_count <= level:
        for current_table in current_level:
            lineage_json = UnityCatalogApi(api_client).list_lineages_by_table(current_table)
            upstream_of_current = [
                get_table_name(
                    table_node
                ) for table_node in lineage_json['upstream_tables']
            ] if 'upstream_tables' in lineage_json else []
            next_level.extend(upstream_of_current)
            cur_downstream = [
                get_table_name(
                    table_node
                ) for table_node in lineage_json['downstream_tables']
            ] if 'downstream_tables' in lineage_json else []
            if len(cur_downstream) > 0:
                if current_table in node_to_downstream:
                    node_to_downstream[current_table] = cur_downstream
        level_count = level_count + 1
        current_level = next_level
        next_level = []
    return node_to_downstream


def connect_upstream_tables(upstream_tables, current_table, node_to_downstream):
    """
    fill node_to_downstream dict based with give upstreams and current table
    """
    if len(upstream_tables) > 0:
        if upstream_tables not in node_to_downstream:
            node_to_downstream[upstream_tables] = [current_table]
