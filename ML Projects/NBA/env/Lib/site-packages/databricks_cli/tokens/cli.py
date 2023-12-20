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

from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.tokens.api import TokensApi
from databricks_cli.utils import CONTEXT_SETTINGS, eat_exceptions, pretty_format
from databricks_cli.version import print_version_callback, version


TOKEN_LIFETIME_SEC = 60 * 60 * 24 * 90


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Create a token.')
@click.option('--lifetime-seconds', required=False, default=TOKEN_LIFETIME_SEC,
              help="Number of seconds for the token to live for. The default is %d seconds or "
                   "%d days." % (TOKEN_LIFETIME_SEC, TOKEN_LIFETIME_SEC / 60 / 60 / 24))
@click.option('--comment', required=True,
              help="String describing what the token is for.")
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def create_token_cli(api_client, lifetime_seconds, comment):
    """
    Create and return a token.
    This call returns the error QUOTA_EXCEEDED if the caller exceeds the token quota, which is 600.
    """
    content = TokensApi(api_client).create(lifetime_seconds, comment)
    click.echo(pretty_format(content))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List tokens for the calling user.')
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def list_cli(api_client):
    """
    List all the valid tokens for a user-workspace pair.
    """
    content = TokensApi(api_client).list()
    click.echo(pretty_format(content))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Revoke an access token.')
@click.option('--token-id', required=True,
              help="Token id to revoke")
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def revoke_cli(api_client, token_id):
    """
    Revoke an access token.

    This call returns the error RESOURCE_DOES_NOT_EXIST
    if a token with the specified ID is not valid.
    """
    content = TokensApi(api_client).revoke(token_id)
    click.echo(pretty_format(content))


@click.group(context_settings=CONTEXT_SETTINGS,
             short_help="Utility to interact with Databricks tokens.")
@click.option("--version", "-v", is_flag=True, callback=print_version_callback,
              expose_value=False, is_eager=True, help=version)
@debug_option
@profile_option
@eat_exceptions
def tokens_group():  # pragma: no cover
    """Utility to interact with Databricks tokens."""
    pass


tokens_group.add_command(create_token_cli, name='create')
tokens_group.add_command(list_cli, name='list')
tokens_group.add_command(revoke_cli, name='revoke')
