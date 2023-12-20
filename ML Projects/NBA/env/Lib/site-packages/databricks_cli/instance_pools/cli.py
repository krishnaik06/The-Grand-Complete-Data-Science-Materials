# Databricks CLI
# Copyright 2017 Databricks, Inc.
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
from tabulate import tabulate

from databricks_cli.click_types import OutputClickType, JsonClickType, InstancePoolIdClickType
from databricks_cli.instance_pools.api import InstancePoolsApi
from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS, pretty_format, json_cli_base, \
    truncate_string
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.version import print_version_callback, version


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--json-file', default=None, type=click.Path(),
              help='File containing JSON request to POST to /api/2.0/instance-pools/create.')
@click.option('--json', default=None, type=JsonClickType(),
              help=JsonClickType.help('/api/2.0/instance-pools/create'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def create_cli(api_client, json_file, json):
    """
    Creates a Databricks instance pool.

    The specification for the request json can be found at
    https://docs.databricks.com/api/latest/instance-pools.html#create
    """
    json_cli_base(json_file, json,
                  lambda json: InstancePoolsApi(api_client).create_instance_pool(json))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--json-file', default=None, type=click.Path(),
              help='File containing JSON request to POST to /api/2.0/instance-pools/edit.')
@click.option('--json', default=None, type=JsonClickType(),
              help=JsonClickType.help('/api/2.0/instance-pools/edit'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def edit_cli(api_client, json_file, json):
    """
    Edits a Databricks instance pool.

    The specification for the request json can be found at
    https://docs.databricks.com/api/latest/instance-pools.html#edit
    """
    if not bool(json_file) ^ bool(json):
        raise RuntimeError('Either --json-file or --json should be provided')
    json_cli_base(json_file, json,
                  lambda json: InstancePoolsApi(api_client).edit_instance_pool(json),
                  print_response=False)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--instance-pool-id', required=True, type=InstancePoolIdClickType(),
              help=InstancePoolIdClickType.help)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_cli(api_client, instance_pool_id):
    """
    Deletes a Databricks instance pool given its ID.

    This permanently deletes the instance pool. The idle instances in the pool are terminated
    asynchronously. New clusters cannot attach to the pool. Running clusters attached to the pool
    continue to run but cannot auto-scale up. Terminated clusters attached to the pool will fail to
    start until they are edited to no longer use the pool.
    """
    InstancePoolsApi(api_client).delete_instance_pool(instance_pool_id)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--instance-pool-id', required=True, type=InstancePoolIdClickType(),
              help=InstancePoolIdClickType.help)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_cli(api_client, instance_pool_id):
    """
    Retrieves metadata about an instance pool.
    """
    click.echo(pretty_format(InstancePoolsApi(api_client).get_instance_pool(instance_pool_id)))


def _instance_pools_to_table(instance_pools_json):
    ret = []
    stats_headers = ['idle_count', 'used_count', 'pending_idle_count', 'pending_used_count']
    for c in instance_pools_json.get('instance_pools', []):
        pool_stats = []
        pool_stats.append(c['instance_pool_id'])
        pool_stats.append(truncate_string(c['instance_pool_name']))
        for header in stats_headers:
            pool_stats.append(c['stats'][header])
        # clone the content in the pool_stats. Pool_stats will be re-used in next iteration.
        ret.append(pool_stats[:])
    return ret


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Lists active and recently terminated instance pools.')
@click.option('--output', default=None, help=OutputClickType.help, type=OutputClickType())
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_cli(api_client, output):
    """
    Lists active instance pools with the stats of the pools.
    """
    instance_pools_json = InstancePoolsApi(api_client).list_instance_pools()
    if OutputClickType.is_json(output):
        click.echo(pretty_format(instance_pools_json))
    else:
        headers = ['ID', 'NAME', 'IDLE INSTANCES', 'USED INSTANCES', 'PENDING IDLE INSTANCES',
                   'PENDING USED INSTANCES']
        click.echo(tabulate(_instance_pools_to_table(instance_pools_json), headers=headers,
                            tablefmt='plain', numalign='left'))


@click.group(context_settings=CONTEXT_SETTINGS,
             short_help='Utility to interact with Databricks instance pools.')
@click.option('--version', '-v', is_flag=True, callback=print_version_callback,
              expose_value=False, is_eager=True, help=version)
@debug_option
@profile_option
@eat_exceptions
def instance_pools_group():  # pragma: no cover
    """
    Utility to interact with Databricks instance pools.
    """
    pass


instance_pools_group.add_command(create_cli, name='create')
instance_pools_group.add_command(edit_cli, name='edit')
instance_pools_group.add_command(delete_cli, name='delete')
instance_pools_group.add_command(get_cli, name='get')
instance_pools_group.add_command(list_cli, name='list')
