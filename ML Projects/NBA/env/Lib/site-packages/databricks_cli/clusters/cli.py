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
import time
from datetime import datetime
from json import loads as json_loads

import click
from tabulate import tabulate

from databricks_cli.click_types import OutputClickType, JsonClickType, ClusterIdClickType, \
    OneOfOption
from databricks_cli.clusters.api import ClusterApi
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS, pretty_format, json_cli_base, \
    truncate_string, CLUSTER_OPTIONS
from databricks_cli.version import print_version_callback, version


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--json-file', default=None, type=click.Path(),
              help='File containing JSON request to POST to /api/2.0/clusters/create.')
@click.option('--json', default=None, type=JsonClickType(),
              help=JsonClickType.help('/api/2.0/clusters/create'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def create_cli(api_client, json_file, json):
    """
    Creates a Databricks cluster.

    The specification for the request json can be found at
    https://docs.databricks.com/api/latest/clusters.html#create
    """
    json_cli_base(json_file, json, lambda json: ClusterApi(api_client).create_cluster(json))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--json-file', default=None, type=click.Path(),
              help='File containing JSON request to POST to /api/2.0/clusters/edit.')
@click.option('--json', default=None, type=JsonClickType(),
              help=JsonClickType.help('/api/2.0/clusters/edit'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def edit_cli(api_client, json_file, json):
    """
    Edits a Databricks cluster.

    The specification for the request json can be found at
    https://docs.databricks.com/api/latest/clusters.html#edit
    """
    if not bool(json_file) ^ bool(json):
        raise RuntimeError('Either --json-file or --json should be provided')
    if json_file:
        with open(json_file, 'r') as f:
            json = f.read()
    deser_json = json_loads(json)
    ClusterApi(api_client).edit_cluster(deser_json)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Starts a terminated Databricks cluster given its ID.')
@click.option('--cluster-id', required=True, type=ClusterIdClickType(),
              help=ClusterIdClickType.help)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def start_cli(api_client, cluster_id):
    """
    Starts a terminated Databricks cluster given its ID.

    If the cluster is not currently in a TERMINATED state, nothing will happen.

    """
    ClusterApi(api_client).start_cluster(cluster_id)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--cluster-id', required=True, type=ClusterIdClickType(),
              help=ClusterIdClickType.help)
@debug_option
@profile_option
@provide_api_client
@eat_exceptions
def restart_cli(api_client, cluster_id):
    """
    Restarts a Databricks cluster given its ID.

    If the cluster is not currently in a RUNNING state, nothing will happen
    """
    ClusterApi(api_client).restart_cluster(cluster_id)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--cluster-id', required=True, type=ClusterIdClickType(),
              help=ClusterIdClickType.help)
@click.option('--num-workers', required=True, type=click.INT,
              help='Number of workers')
@debug_option
@profile_option
@provide_api_client
@eat_exceptions
def resize_cli(api_client, cluster_id, num_workers):
    """Resizes a Databricks cluster given its ID.

    Provide a `--num-workers` parameter to indicate the new cluster size.

    If the cluster is not currently in a RUNNING state, this will cause an
    error to occur.
    """
    ClusterApi(api_client).resize_cluster(cluster_id, num_workers)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--cluster-id', required=True, type=ClusterIdClickType(),
              help=ClusterIdClickType.help)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_cli(api_client, cluster_id):
    """
    Removes a Databricks cluster given its ID.

    The cluster is removed asynchronously. Once the deletion has completed,
    the cluster will be in a TERMINATED state. If the cluster is already in
    a TERMINATING or TERMINATED state, nothing will happen.

    Use ``databricks clusters get --cluster-id CLUSTER_ID`` to check termination states.
    """
    ClusterApi(api_client).delete_cluster(cluster_id)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--cluster-id', cls=OneOfOption, one_of=CLUSTER_OPTIONS,
              type=ClusterIdClickType(), default=None, help=ClusterIdClickType.help)
@click.option('--cluster-name', cls=OneOfOption, one_of=CLUSTER_OPTIONS,
              type=ClusterIdClickType(), default=None, help=ClusterIdClickType.help)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_cli(api_client, cluster_id, cluster_name):
    """
    Retrieves metadata about a cluster.
    """
    if cluster_id:
        cluster = ClusterApi(api_client).get_cluster(cluster_id)
    elif cluster_name:
        cluster = ClusterApi(api_client).get_cluster_by_name(cluster_name)
    else:
        raise RuntimeError('cluster_name and cluster_id were empty?')

    click.echo(pretty_format(cluster))


def _clusters_to_table(clusters_json):
    ret = []
    for c in clusters_json.get('clusters', []):
        ret.append((c['cluster_id'], truncate_string(c['cluster_name']), c['state']))
    return ret


def _cluster_events_to_table(events_json):
    ret = []
    for event in events_json.get('events', []):
        timestamp = event['timestamp'] / 1000
        timezone = time.tzname[time.localtime(timestamp).tm_isdst]
        formatted_time = "%s %s" % (
            datetime.fromtimestamp(event['timestamp'] / 1000.).strftime('%Y-%m-%d %H:%M:%S'),
            timezone)
        ret.append((formatted_time, event['type'], event['details']))
    return ret


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Lists active and recently terminated clusters.')
@click.option('--output', default=None, help=OutputClickType.help, type=OutputClickType())
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_cli(api_client, output):
    """
    Lists active and recently terminated clusters.

    Returns information about all currently active clusters, and up
    to 100 most recently terminated clusters in the past 7 days.

    By default the output format will be a human readable table with the following fields

      - Cluster ID

      - Cluster name

      - Cluster state
    """
    clusters_json = ClusterApi(api_client).list_clusters()
    if OutputClickType.is_json(output):
        click.echo(pretty_format(clusters_json))
    else:
        click.echo(tabulate(_clusters_to_table(clusters_json), tablefmt='plain'))


@click.command(context_settings=CONTEXT_SETTINGS)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_zones_cli(api_client):
    """
    Lists zones where clusters can be created.

    The output format is specified in
    https://docs.databricks.com/api/latest/clusters.html#list-zones
    """
    click.echo(pretty_format(ClusterApi(api_client).list_zones()))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Lists possible node types for a cluster.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_node_types_cli(api_client):
    """
    Lists possible node types for a cluster.

    The output format is specified in
    https://docs.databricks.com/api/latest/clusters.html#list-node-types
    """
    click.echo(pretty_format(ClusterApi(api_client).list_node_types()))


@click.command(context_settings=CONTEXT_SETTINGS)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def spark_versions_cli(api_client):
    """
    Lists possible Databricks Runtime versions for a cluster.

    The output format is specified in
    https://docs.databricks.com/api/latest/clusters.html#spark-versions
    """
    click.echo(pretty_format(ClusterApi(api_client).spark_versions()))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--cluster-id', required=True, type=ClusterIdClickType(),
              help=ClusterIdClickType.help)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def permanent_delete_cli(api_client, cluster_id):
    """
    Permanently deletes a Spark cluster.

    If the cluster is running, it is terminated and its resources are asynchronously removed.
    If the cluster is terminated, then it is immediately removed.
    """
    ClusterApi(api_client).permanent_delete(cluster_id)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--cluster-id', required=True, type=ClusterIdClickType(),
              help=ClusterIdClickType.help)
@click.option('--start-time', required=False, default=None,
              help="The start time in epoch milliseconds. If unprovided, returns events starting "
                   "from the beginning of time.")
@click.option('--end-time', required=False, default=None,
              help="The end time in epoch milliseconds. If unprovided, returns events up to the "
                   "current time")
@click.option('--order', required=False, default=None,
              help="The order to list events in; either ASC or DESC. Defaults to DESC "
                   "(most recent first).")
@click.option('--event-type', required=False, default=None,
              help="An event types to filter on (specify multiple event types by passing "
                   "the --event-type option multiple times). If empty, all event types "
                   "are returned.", multiple=True)
@click.option('--offset', required=False, default=None,
              help="The offset in the result set. Defaults to 0 (no offset). When an offset is "
                   "specified and the results are requested in descending order, the end_time "
                   "field is required.")
@click.option('--limit', required=False, default=None,
              help="The maximum number of events to include in a page of events. Defaults to 50, "
                   "and maximum allowed value is 500.")
@click.option('--output', default=None, help=OutputClickType.help, type=OutputClickType())
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def cluster_events_cli(api_client, cluster_id, start_time, end_time, order, event_type, offset,
                       limit, output):
    """
    Gets events for a Spark cluster.
    """
    events_json = ClusterApi(api_client).get_events(
        cluster_id=cluster_id, start_time=start_time, end_time=end_time, order=order,
        event_types=event_type, offset=offset, limit=limit)
    if OutputClickType.is_json(output):
        click.echo(pretty_format(events_json))
    else:
        click.echo(tabulate(_cluster_events_to_table(events_json), tablefmt='plain'))


@click.group(context_settings=CONTEXT_SETTINGS,
             short_help='Utility to interact with Databricks clusters.')
@click.option('--version', '-v', is_flag=True, callback=print_version_callback,
              expose_value=False, is_eager=True, help=version)
@debug_option
@profile_option
@eat_exceptions
def clusters_group():  # pragma: no cover
    """
    Utility to interact with Databricks clusters.
    """
    pass


clusters_group.add_command(create_cli, name='create')
clusters_group.add_command(edit_cli, name='edit')
clusters_group.add_command(start_cli, name='start')
clusters_group.add_command(restart_cli, name='restart')
clusters_group.add_command(resize_cli, name='resize')
clusters_group.add_command(delete_cli, name='delete')
clusters_group.add_command(get_cli, name='get')
clusters_group.add_command(list_cli, name='list')
clusters_group.add_command(list_zones_cli, name='list-zones')
clusters_group.add_command(list_node_types_cli, name='list-node-types')
clusters_group.add_command(spark_versions_cli, name='spark-versions')
clusters_group.add_command(permanent_delete_cli, name='permanent-delete')
clusters_group.add_command(cluster_events_cli, name='events')
