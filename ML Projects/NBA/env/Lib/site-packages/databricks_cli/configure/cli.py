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
import io
import os
from os import path

import click
from click import ParamType

from databricks_cli.oauth.oauth import get_tokens

from databricks_cli.configure.config import profile_option, get_profile_from_context, debug_option
from databricks_cli.configure.provider import DatabricksConfig, update_and_persist_config, \
    ProfileConfigProvider
from databricks_cli.sdk.version import API_VERSION, API_VERSIONS
from databricks_cli.utils import CONTEXT_SETTINGS

PROMPT_HOST = 'Databricks Host (should begin with https://)'
PROMPT_USERNAME = 'Username'
PROMPT_PASSWORD = 'Password'  # NOQA
PROMPT_TOKEN = 'Token'  # NOQA
ENV_AAD_TOKEN = 'DATABRICKS_AAD_TOKEN'
DEFAULT_SCOPES = [
    'accounts',
    'clusters',
    'mlflow',
    'offline_access',
    'sql',
    'unity-catalog'
]


def _configure_cli_token_file(profile, token_file, host, insecure, jobs_api_version):
    if not path.exists(token_file):
        raise RuntimeError('Unable to read token from "{}"'.format(token_file))

    with io.open(token_file, encoding='utf-8') as f:
        token = f.readline().strip()

    config = ProfileConfigProvider(profile).get_config() or DatabricksConfig.empty()
    if not host:
        host = click.prompt(PROMPT_HOST, default=config.host, type=_DbfsHost())

    new_config = DatabricksConfig.from_token(host=host,
                                             token=token,
                                             refresh_token=None,
                                             insecure=insecure,
                                             jobs_api_version=jobs_api_version)
    update_and_persist_config(profile, new_config)


def _configure_cli_token(profile, insecure, host, jobs_api_version):
    config = ProfileConfigProvider(profile).get_config() or DatabricksConfig.empty()

    if not host:
        host = click.prompt(PROMPT_HOST, default=config.host, type=_DbfsHost())

    token = click.prompt(PROMPT_TOKEN, default=config.token, hide_input=True)
    new_config = DatabricksConfig.from_token(host=host,
                                             token=token,
                                             refresh_token=None,
                                             insecure=insecure,
                                             jobs_api_version=jobs_api_version)
    update_and_persist_config(profile, new_config)


def scope_format(user_input):
    user_inputs = user_input.split(',')
    choice = click.Choice(DEFAULT_SCOPES)
    return list(map(lambda x: choice(x.strip()), user_inputs))


def _configure_cli_oauth(profile, insecure, host, scope, jobs_api_version):
    config = ProfileConfigProvider(profile).get_config() or DatabricksConfig.empty()

    if not host:
        host = click.prompt(PROMPT_HOST, default=config.host, type=_DbfsHost())
    if not scope:
        scope = click.prompt(
            "Pick one or more comma-separated scopes from {scopes}".format(scopes=DEFAULT_SCOPES),
            value_proc=scope_format,
            type=click.Choice(DEFAULT_SCOPES), default=None)
    access_token, refresh_token = get_tokens(host, scope)
    new_config = DatabricksConfig.from_token(host=host,
                                             token=access_token,
                                             refresh_token=refresh_token,
                                             insecure=insecure,
                                             jobs_api_version=jobs_api_version)
    update_and_persist_config(profile, new_config)


def _configure_cli_aad_token(profile, insecure, host, jobs_api_version):
    config = ProfileConfigProvider(profile).get_config() or DatabricksConfig.empty()

    if ENV_AAD_TOKEN not in os.environ:
        click.echo('[ERROR] Set Environment Variable \'%s\' with your '
                   'AAD Token and run again.\n' % ENV_AAD_TOKEN)
        click.echo('Commands to run to get your AAD token:\n'
                   '\t az login\n'
                   '\t token_response=$(az account get-access-token '
                   '--resource 2ff814a6-3304-4ab8-85cb-cd0e6f879c1d)\n'
                   '\t export %s=$(jq .accessToken -r <<< "$token_response")\n' % ENV_AAD_TOKEN
                   )
        return

    if not host:
        host = click.prompt(PROMPT_HOST, default=config.host, type=_DbfsHost())

    aad_token = os.environ.get(ENV_AAD_TOKEN)
    new_config = DatabricksConfig.from_token(host=host,
                                             token=aad_token,
                                             refresh_token=None,
                                             insecure=insecure,
                                             jobs_api_version=jobs_api_version)
    update_and_persist_config(profile, new_config)


def _configure_cli_password(profile, insecure, host, jobs_api_version):
    config = ProfileConfigProvider(profile).get_config() or DatabricksConfig.empty()
    if config.password:
        default_password = '*' * len(config.password)
    else:
        default_password = None

    if not host:
        host = click.prompt(PROMPT_HOST, default=config.host, type=_DbfsHost())

    username = click.prompt(PROMPT_USERNAME, default=config.username)
    password = click.prompt(PROMPT_PASSWORD, default=default_password, hide_input=True,
                            confirmation_prompt=True)
    if password == default_password:
        password = config.password
    new_config = DatabricksConfig.from_password(host, username, password, insecure,
                                                jobs_api_version)
    update_and_persist_config(profile, new_config)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Configures host and authentication info for the CLI.')
@click.option('--oauth', '-o', 'oauth', show_default=True, is_flag=True, default=False,
              help='[Experimental] Use OAuth for authorization')
@click.option('--scope', '-s', 'scope', show_default=True, multiple=True,
              type=click.Choice(DEFAULT_SCOPES),
              help='[Experimental] Specify which OAuth scopes to request access for')
@click.option('--token', '-t', 'token', show_default=True, is_flag=True, default=False)
@click.option('--token-file', '-f', 'token_file', default=None,
              help='Instead of reading the token from stdin, ' +
                   'read the token from a file provided by a secret store.')
@click.option('--host', show_default=True, default=None,
              help='Host to connect to.')
@click.option('--aad-token', show_default=True, is_flag=True, default=False)
@click.option('--insecure', show_default=True, is_flag=True, default=None,
              help='DO NOT verify SSL Certificates')
@click.option('--jobs-api-version', show_default=True, default=API_VERSION,
              type=click.Choice(API_VERSIONS), help='API version to use for jobs.')
@debug_option
@profile_option
def configure_cli(token, aad_token, insecure, host, token_file, jobs_api_version, oauth, scope):
    """
    Configures host, authentication, and jobs-api version for the CLI.
    """
    profile = get_profile_from_context()
    insecure_str = str(insecure) if insecure is not None else None

    if token:
        _configure_cli_token(profile=profile, insecure=insecure_str, host=host,
                             jobs_api_version=jobs_api_version)
    elif token_file:
        _configure_cli_token_file(profile=profile, insecure=insecure_str, host=host,
                                  token_file=token_file, jobs_api_version=jobs_api_version)
    elif oauth:
        _configure_cli_oauth(profile=profile, insecure=insecure_str, host=host,
                             scope=scope, jobs_api_version=jobs_api_version)
    elif aad_token:
        _configure_cli_aad_token(profile=profile, insecure=insecure_str, host=host,
                                 jobs_api_version=jobs_api_version)
    else:
        _configure_cli_password(profile=profile, insecure=insecure_str, host=host,
                                jobs_api_version=jobs_api_version)


class _DbfsHost(ParamType):
    """
    Used to validate the configured host
    """

    def convert(self, value, param, ctx):
        if value.startswith('https://'):
            return value
        else:
            self.fail('The host does not start with https://')
