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

from databricks_cli.click_types import MetastoreIdClickType, WorkspaceIdClickType, JsonClickType
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.unity_catalog.utils import hide, json_file_help, json_string_help, \
    mc_pretty_format
from databricks_cli.unity_catalog.api import UnityCatalogApi
from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS, json_cli_base


#################  Metastore Commands  #####################


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Create a metastore.')
@click.option('--name', required=True, help='Name of the new metastore.')
@click.option('--storage-root', required=True,
              help='Storage root URL for the new metastore.')
@click.option('--region', required=False,
              help='Region for the new metastore. ' +
                   'Only workspaces located in the same region can be assigned to this metastore.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def create_metastore_cli(api_client, name, storage_root, region):
    """
    Create new metastore.
    """
    metastore_json = UnityCatalogApi(api_client).create_metastore(name, storage_root, region)
    click.echo(mc_pretty_format(metastore_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List metastores.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_metastores_cli(api_client):
    """
    List metastores.
    """
    metastores_json = UnityCatalogApi(api_client).list_metastores()
    click.echo(mc_pretty_format(metastores_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get a metastore.')
@click.option('--id', 'metastore_id', required=True, type=MetastoreIdClickType(),
              help='Unique identifier of the metastore to get.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_metastore_cli(api_client, metastore_id):
    """
    Get a metastore.
    """
    metastore_json = UnityCatalogApi(api_client).get_metastore(metastore_id)
    click.echo(mc_pretty_format(metastore_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Update a metastore.')
@click.option('--id', 'metastore_id', required=True, type=MetastoreIdClickType(),
              help='Unique identifier of the metastore to update.')
@click.option('--new-name', default=None, help='New name of the metastore.')
@click.option('--storage-root-credential-id', default=None,
              help='Storage Credential ID to access storage root.')
@click.option('--delta-sharing-scope', default=None,
              help='Delta sharing scope. Can be INTERNAL or INTERNAL_AND_EXTERNAL.')
@click.option('--delta-sharing-recipient-token-lifetime-in-seconds', default=None, type=int,
              help=(
                'The token lifetime determines how long a generated Delta Sharing token is '
                'valid for. 0 for no expiration.'))
@click.option('--delta-sharing-organization-name', default=None,
              help=(
                'The organization name of a Delta Sharing entity. '
                'The name will be used in Databricks-to-Databricks Delta Sharing as the official '
                'name.'))
@click.option('--owner', default=None, help='Owner of the metastore.')
@click.option('--json-file', default=None, type=click.Path(),
              help=json_file_help(method='PATCH', path='/metastores/{id}'))
@click.option('--json', default=None, type=JsonClickType(),
              help=json_string_help(method='PATCH', path='/metastores/{id}'))
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def update_metastore_cli(api_client, metastore_id, new_name,
                         storage_root_credential_id,
                         delta_sharing_scope, delta_sharing_recipient_token_lifetime_in_seconds,
                         delta_sharing_organization_name, owner, json_file, json):
    """
    Update a metastore.

    The public specification for the JSON request is in development.
    """
    has_delta_sharing_flag = (
        (delta_sharing_scope is not None) or
        (delta_sharing_recipient_token_lifetime_in_seconds is not None) or
        (delta_sharing_organization_name is not None))
    if ((new_name is not None) or
        (storage_root_credential_id is not None) or has_delta_sharing_flag or (owner is not None)):
        if (json_file is not None) or (json is not None):
            raise ValueError('Cannot specify JSON if any other update flags are specified')
        data = {
            'name': new_name,
            'storage_root_credential_id': storage_root_credential_id,
            'delta_sharing_scope': delta_sharing_scope,
            'delta_sharing_recipient_token_lifetime_in_seconds':
            delta_sharing_recipient_token_lifetime_in_seconds,
            'delta_sharing_organization_name': delta_sharing_organization_name,
            'owner': owner
        }
        metastore_json = UnityCatalogApi(api_client).update_metastore(metastore_id, data)
        click.echo(mc_pretty_format(metastore_json))
    else:
        json_cli_base(json_file, json,
                  lambda json: UnityCatalogApi(api_client).update_metastore(metastore_id, json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Delete a metastore.')
@click.option('--id', 'metastore_id', required=True, type=MetastoreIdClickType(),
              help='Unique identifier of the metastore to delete.')
@click.option('--force', '-f', is_flag=True, default=False)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_metastore_cli(api_client, metastore_id, force):
    """
    Delete a metastore.
    """
    UnityCatalogApi(api_client).delete_metastore(metastore_id, force)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get summary info of current metastore.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def metastore_summary_cli(api_client):
    """
    Get metastore summary.
    """
    summary_json = UnityCatalogApi(api_client).get_metastore_summary()
    click.echo(mc_pretty_format(summary_json))

@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get metastore assignment for workspace.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_metastore_assignment_cli(api_client):
    """
    Get current metastore assignment for workspace.
    """
    assign_json = UnityCatalogApi(api_client).get_current_metastore_assignment()
    click.echo(mc_pretty_format(assign_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Assign a metastore to a workspace.')
@click.option('--workspace-id', 'workspace_id', required=True, type=WorkspaceIdClickType(),
              help='Unique identifier of the workspace for the metastore assignment.')
@click.option('--metastore-id', 'metastore_id', required=True, type=MetastoreIdClickType(),
              help='Unique identifier of the metastore to assign to the workspace.')
@click.option('--default-catalog-name', 'default_catalog_name', required=False,
              default='hive_metastore',
              help='Name of the default catalog to use with the metastore ' +
                   '(default: "hive_metastore").')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def assign_metastore_cli(api_client, workspace_id, metastore_id, default_catalog_name):
    """
    Assign a metastore to a specified workspace.

    If the workspace already has a metastore assigned, it is updated.
    """
    resp = UnityCatalogApi(api_client).create_metastore_assignment(workspace_id, metastore_id,
                                                                   default_catalog_name)
    # resp will just be an empty object ('{}') but it's good to print *something*
    click.echo(mc_pretty_format(resp))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Unassigns a metastore from a workspace.')
@click.option('--workspace-id', 'workspace_id', required=True, type=WorkspaceIdClickType(),
              help='Unique identifier of the workspace.')
@click.option('--metastore-id', 'metastore_id', required=True, type=MetastoreIdClickType(),
              help='Unique identifier of the metastore to unassign from the workspace.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def unassign_metastore_cli(api_client, workspace_id, metastore_id):
    """
    Unassign a metastore from a workspace.
    """
    resp = UnityCatalogApi(api_client).delete_metastore_assignment(workspace_id, metastore_id)
    # resp will just be an empty object ('{}') but it's good to print *something*
    click.echo(mc_pretty_format(resp))


@click.group()
def metastores_group():  # pragma: no cover
    pass


def register_metastore_commands(cmd_group):
    # Register deprecated "verb-noun" commands for backward compatibility.
    cmd_group.add_command(hide(create_metastore_cli), name='create-metastore')
    cmd_group.add_command(hide(list_metastores_cli), name='list-metastores')
    cmd_group.add_command(hide(get_metastore_cli), name='get-metastore')
    cmd_group.add_command(hide(update_metastore_cli), name='update-metastore')
    cmd_group.add_command(hide(delete_metastore_cli), name='delete-metastore')
    cmd_group.add_command(hide(metastore_summary_cli), name='metastore-summary')
    cmd_group.add_command(hide(assign_metastore_cli), name='assign-metastore')
    cmd_group.add_command(hide(unassign_metastore_cli), name='unassign-metastore')
    cmd_group.add_command(hide(get_metastore_assignment_cli),
                          name='get-metastore-assignment')

    # Register command group.
    metastores_group.add_command(create_metastore_cli, name='create')
    metastores_group.add_command(list_metastores_cli, name='list')
    metastores_group.add_command(get_metastore_cli, name='get')
    metastores_group.add_command(update_metastore_cli, name='update')
    metastores_group.add_command(delete_metastore_cli, name='delete')
    metastores_group.add_command(metastore_summary_cli, name='get-summary')
    metastores_group.add_command(assign_metastore_cli, name='assign')
    metastores_group.add_command(unassign_metastore_cli, name='unassign')
    metastores_group.add_command(get_metastore_assignment_cli, name='get-assignment')
    cmd_group.add_command(metastores_group, name='metastores')
