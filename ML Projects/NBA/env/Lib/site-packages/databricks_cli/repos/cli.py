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

from databricks_cli.click_types import OneOfOption
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.repos.api import ReposApi
from databricks_cli.utils import CONTEXT_SETTINGS, eat_exceptions, pretty_format
from databricks_cli.version import print_version_callback, version

UPDATE_OPTIONS = ['branch', 'tag']
ID_OPTIONS = ['repo-id', 'path']


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List repos that user has Manage permissions on')
@click.option('--path-prefix', help="Path prefix to filter results by")
@click.option('--next-page-token', help="Token used to fetch the next page of results")
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def list_repos_cli(api_client, path_prefix, next_page_token):
    """
    List repos that the user has Manage permissions on.
    """
    content = ReposApi(api_client).list(path_prefix, next_page_token)
    click.echo(pretty_format(content))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Create a repo and link it to the given remote Git repo')
@click.option('--url', required=True, help="URL of the remote Git repo")
@click.option('--provider',
              help="Git provider (case insensitive). Required if it couldn't be detected from "
                   "host name")
@click.option('--path', help="Desired workspace path of the repo object")
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def create_repo_cli(api_client, url, provider, path):
    """
    Creates a repo object and links it to the remote Git repo specified.
    """
    content = ReposApi(api_client).create(url, provider, path)
    click.echo(pretty_format(content))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get repo based on ID or path')
@click.option('--repo-id', cls=OneOfOption, default=None, one_of=ID_OPTIONS, help="Repo ID")
@click.option('--path', cls=OneOfOption, default=None, one_of=ID_OPTIONS, 
              help="Workspace path of the repo object")
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def get_repo_cli(api_client, repo_id, path):
    """
    Gets the repo.
    """
    id_from_param_or_path = (repo_id if repo_id is not None
                             else ReposApi(api_client).get_repo_id(path))
    content = ReposApi(api_client).get(id_from_param_or_path)
    click.echo(pretty_format(content))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Checkout the repo to the given branch or tag')
@click.option('--repo-id', cls=OneOfOption, default=None, one_of=ID_OPTIONS, help="Repo ID")
@click.option('--path', cls=OneOfOption, default=None, one_of=ID_OPTIONS,
              help="Workspace path of the repo object")
@click.option('--branch', cls=OneOfOption, default=None, one_of=UPDATE_OPTIONS, help="Branch name")
@click.option('--tag', cls=OneOfOption, default=None, one_of=UPDATE_OPTIONS, help="Tag name")
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def update_repo_cli(api_client, repo_id, branch, tag, path):
    """
    Checks out the repo to the given branch or tag. This call returns an error if the branch 
    or tag doesn't exist.
    """
    id_from_param_or_path = (repo_id if repo_id is not None
                             else ReposApi(api_client).get_repo_id(path))
    content = ReposApi(api_client).update(id_from_param_or_path, branch, tag)
    click.echo(pretty_format(content))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Delete the repo based on ID or path')
@click.option('--repo-id', cls=OneOfOption, default=None, one_of=ID_OPTIONS, help="Repo ID")
@click.option('--path', cls=OneOfOption, default=None, one_of=ID_OPTIONS,
              help="Workspace path of the repo object")
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def delete_repo_cli(api_client, repo_id, path):
    """
    Deletes the repo.
    """
    id_from_param_or_path = (repo_id if repo_id is not None
                             else ReposApi(api_client).get_repo_id(path))
    content = ReposApi(api_client).delete(id_from_param_or_path)
    click.echo(pretty_format(content))


@click.group(context_settings=CONTEXT_SETTINGS,
             short_help="Utility to interact with Repos.")
@click.option("--version", "-v", is_flag=True, callback=print_version_callback,
              expose_value=False, is_eager=True, help=version)
@debug_option
@profile_option
@eat_exceptions
def repos_group():  # pragma: no cover
    """Utility to interact with Repos."""
    pass


repos_group.add_command(list_repos_cli, name='list')
repos_group.add_command(get_repo_cli, name='get')
repos_group.add_command(create_repo_cli, name='create')
repos_group.add_command(update_repo_cli, name='update')
repos_group.add_command(delete_repo_cli, name='delete')
