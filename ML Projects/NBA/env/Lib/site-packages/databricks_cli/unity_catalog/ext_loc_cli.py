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

import click

from databricks_cli.click_types import JsonClickType
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.unity_catalog.api import UnityCatalogApi
from databricks_cli.unity_catalog.utils import del_none, hide, json_file_help, json_string_help, \
    mc_pretty_format
from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS, json_cli_base


def create_update_common_options(f):
    @click.option('--url', default=None,
                help='Path URL for the new external location')
    @click.option('--storage-credential-name', default=None,
                help='Name of storage credential to use with new external location')
    @click.option('--read-only/--no-read-only', is_flag=True, default=None,
                help='Whether the external location is read-only')
    @click.option('--comment', default=None,
                help='Free-form text description.')
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        f(*args, **kwargs)
    return wrapper


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Create External Location.')
@click.option('--name', default=None,
              help='Name of new external location')
@create_update_common_options
@click.option('--skip-validation', '-s', 'skip_val', is_flag=True, default=False,
              help='Skip the validation of location\'s storage credential before creation')
@click.option('--json-file', default=None, type=click.Path(),
              help=json_file_help(method='POST', path='/external-locations'))
@click.option('--json', default=None, type=JsonClickType(),
              help=json_string_help(method='POST', path='/external-locations'))
@debug_option
@profile_option
# UC's createExternalLocation returns a 401 when the validation of the external location's
# storage credential fails; that translates to a misleading error when eat_exceptions is enabled:
#   Your authentication information may be incorrect. Please reconfigure with ``dbfs configure``
# Until that is fixed (should return a 400), show full error trace.
#@eat_exceptions
@provide_api_client
def create_location_cli(api_client, name, url, storage_credential_name,
                        read_only, comment, skip_val, json_file, json):
    """
    Create new external location.

    The public specification for the JSON request is in development.
    """
    if ((name is not None) or (url is not None) or (storage_credential_name is not None) or
        (read_only is not None) or (comment is not None)):
        if (json_file is not None) or (json is not None):
            raise ValueError('Cannot specify JSON if any other creation flags are specified')
        data = {
            'name': name,
            'url': url,
            'credential_name': storage_credential_name,
            'read_only': read_only,
            'comment': comment
        }
        loc_json = UnityCatalogApi(api_client).create_external_location(data, skip_val)
        click.echo(mc_pretty_format(loc_json))
    elif (json is None) and (json_file is None):
        raise ValueError('Must provide name, url and storage-credential-name' +
                         ' or use JSON specification')
    else:
        json_cli_base(json_file, json,
                      lambda json:
                      UnityCatalogApi(api_client).create_external_location(json, skip_val),
                      encode_utf8=True)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List external locations.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_locations_cli(api_client, ):
    """
    List external locations.
    """
    locs_json = UnityCatalogApi(api_client).list_external_locations()
    click.echo(mc_pretty_format(locs_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get an external location.')
@click.option('--name', required=True,
              help='Name of the external location to get.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_location_cli(api_client, name):
    """
    Get an external location.
    """
    loc_json = UnityCatalogApi(api_client).get_external_location(name)
    click.echo(mc_pretty_format(loc_json))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Update an external location.')
@click.option('--name', required=True,
              help='Name of the external location to update.')
@click.option('--new-name', default=None, help='New name of the external location.')
@create_update_common_options
@click.option('--owner', default=None,
              help='Owner of the external location.')
@click.option('--force', '-f', is_flag=True, default=False,
              help='Force update even if location has dependent tables/mounts')
@click.option('--skip-validation', '-s', 'skip_val', is_flag=True, default=False,
              help='Skip the validation of location\'s storage credential')
@click.option('--json-file', default=None, type=click.Path(),
              help=json_file_help(method='PATCH', path='/external-locations/{name}'))
@click.option('--json', default=None, type=JsonClickType(),
              help=json_string_help(method='PATCH', path='/external-locations/{name}'))
@debug_option
@profile_option
# See comment for create_location_cli
#@eat_exceptions
@provide_api_client
def update_location_cli(api_client, name, new_name, url, storage_credential_name, read_only,
                        comment, owner, force, skip_val, json_file, json):
    """
    Update an external location.

    The public specification for the JSON request is in development.
    """
    if ((new_name is not None) or (storage_credential_name is not None) or
        (read_only is not None) or (comment is not None)):
        if (json_file is not None) or (json is not None):
            raise ValueError('Cannot specify JSON if any other update flags are specified')
        data = {
            'name': new_name,
            'url': url,
            'credential_name': storage_credential_name,
            'read_only': read_only,
            'comment': comment,
            'owner': owner
        }
        loc_json = UnityCatalogApi(api_client).update_external_location(
            name, data, force, skip_val)
        click.echo(mc_pretty_format(loc_json))
    else:
        json_cli_base(json_file, json,
                      lambda json: UnityCatalogApi(api_client).update_external_location(name, json,
                                                                                        force,
                                                                                        skip_val),
                      encode_utf8=True)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Delete an external location.')
@click.option('--name', required=True,
              help='Name of the external location to delete.')
@click.option('--force', '-f', is_flag=True, default=False,
              help='Force deletion even if location has dependent tables/mounts')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_location_cli(api_client, name, force):
    """
    Delete an external location.
    """
    UnityCatalogApi(api_client).delete_external_location(name, force)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Validate a external location/credential pair')
@click.option('--name', default=None,
              help='Name of the external location to validate.')
@click.option('--url', default=None,
              help='A storage URL to validate.')
@click.option('--cred-name', default=None,
              help='Name of the storage credential to use for validation.')
@click.option('--cred-aws-iam-role', default=None,
              help='An aws role to validate')
@click.option('--cred-az-directory-id', default=None,
              help='An Azure Service Principal directory id to validate')
@click.option('--cred-az-application-id', default=None,
              help='An Azure Service Principal application id to validate')
@click.option('--cred-az-client-secret', default=None,
              help='An Azure Service Principal directory id to validate')
@click.option('--cred-az-mi-access-connector-id', default=None,
              help='An Azure Managed Identity access connector id to validate')
@click.option('--cred-az-mi-id', default=None,
              help='An Azure Managed Identity id to validate')
@click.option('--cred-gcp-sak-email', default=None,
              help='A GCP Service Account Key email to validate')
@click.option('--cred-gcp-sak-private-key-id', default=None,
              help='A GCP Service Account Key private key ID to validate')
@click.option('--cred-gcp-sak-private-key', default=None,
              help='A GCP Service Account Key private key to validate')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def validate_location_cli(api_client, name, url, cred_name, cred_aws_iam_role, cred_az_directory_id,
                          cred_az_application_id, cred_az_client_secret,
                          cred_az_mi_access_connector_id,
                          cred_az_mi_id, cred_gcp_sak_email, cred_gcp_sak_private_key_id,
                          cred_gcp_sak_private_key):
    """
    Validate an external location/credential combination.

    This call will attempt to read/list/write/delete with the given credentials and
    external location.

    One of name/url must be provided. If both are specified, the given credential
    name will be excluded from path overlap checks (used to validate a potential
    update of that credential).

    One of cred-name, or cloud provider specific credential parameters must be
    provided.
    """
    validation_spec = {
        'external_location_name': name,
        'url': url,
        'storage_credential_name': cred_name,
    }
    if cred_aws_iam_role is not None:
        validation_spec['aws_iam_role'] = {
            'role_arn': cred_aws_iam_role
        }

    if ((cred_az_directory_id is not None) or (cred_az_application_id is not None) or
        (cred_az_client_secret is not None)):
        validation_spec['azure_service_principal'] = {
            'directory_id': cred_az_directory_id,
            'application_id': cred_az_application_id,
            'client_secret': cred_az_client_secret
        }

    if (cred_az_mi_access_connector_id is not None) or (cred_az_mi_id is not None):
        validation_spec['azure_managed_identity'] = {
            'access_connector_id': cred_az_mi_access_connector_id,
            'managed_identity_id': cred_az_mi_id
        }

    if ((cred_gcp_sak_email is not None) or (cred_gcp_sak_private_key_id is not None) or
        (cred_gcp_sak_private_key is not None)):
        validation_spec['gcp_service_account_key'] = {
            'email': cred_gcp_sak_email,
            'private_key_id': cred_gcp_sak_private_key_id,
            'private_key': cred_gcp_sak_private_key
        }

    del_none(validation_spec)
    validation_json = UnityCatalogApi(api_client).validate_external_location(validation_spec)
    click.echo(mc_pretty_format(validation_json))


@click.group()
def external_locations_group():  # pragma: no cover
    pass


def register_ext_loc_commands(cmd_group):
    # Register deprecated "verb-noun" commands for backward compatibility.
    cmd_group.add_command(hide(create_location_cli), name='create-external-location')
    cmd_group.add_command(hide(list_locations_cli), name='list-external-locations')
    cmd_group.add_command(hide(get_location_cli), name='get-external-location')
    cmd_group.add_command(hide(update_location_cli), name='update-external-location')
    cmd_group.add_command(hide(delete_location_cli), name='delete-external-location')
    cmd_group.add_command(hide(validate_location_cli), name='validate-external-location')

    # Register command group.
    external_locations_group.add_command(create_location_cli, name='create')
    external_locations_group.add_command(list_locations_cli, name='list')
    external_locations_group.add_command(get_location_cli, name='get')
    external_locations_group.add_command(update_location_cli, name='update')
    external_locations_group.add_command(delete_location_cli, name='delete')
    external_locations_group.add_command(validate_location_cli, name='validate')
    cmd_group.add_command(external_locations_group, name='external-locations')
