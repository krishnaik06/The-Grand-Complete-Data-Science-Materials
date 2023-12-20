"""Provide the API methods for GROUPs Databricks REST endpoint."""
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
from databricks_cli.groups.api import GroupsApi
from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS, pretty_format
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.version import print_version_callback, version


MEMBER_OPTIONS = ['user-name', 'group-name']


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help="Add an existing principal to another existing group.")
@click.option("--parent-name", required=True,
              help=("Name of the parent group to which the new member will be "
                    " added. This field is required."))
@click.option("--user-name", cls=OneOfOption, default=None, one_of=MEMBER_OPTIONS,
              help="The user name which will be added to the parent group.")
@click.option("--group-name", cls=OneOfOption, default=None, one_of=MEMBER_OPTIONS,
              help="If group name which will be added to the parent group.")
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def add_member_cli(api_client, parent_name, user_name, group_name):
    """Add a user or group to a group."""
    GroupsApi(api_client).add_member(parent_name=parent_name,
                                     user_name=user_name,
                                     group_name=group_name)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help="Create a new group with the given name.")
@click.option("--group-name", required=True)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def create_cli(api_client, group_name):
    """Create a new group with the given name."""
    content = GroupsApi(api_client).create(group_name)
    click.echo(pretty_format(content))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help="Return all of the members of a particular group.")
@click.option("--group-name", required=True)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_members_cli(api_client, group_name):
    """Return all of the members of a particular group."""
    content = GroupsApi(api_client).list_members(group_name)
    click.echo(pretty_format(content))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help="Return all of the groups in a workspace.")
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_all_cli(api_client):
    """Return all of the groups in an organization."""
    content = GroupsApi(api_client).list_all()
    click.echo(pretty_format(content))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help="Retrieve all groups in which a given user or group is a member.")
@click.option("--user-name", cls=OneOfOption, default=None, one_of=MEMBER_OPTIONS)
@click.option("--group-name", cls=OneOfOption, default=None, one_of=MEMBER_OPTIONS)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_parents_cli(api_client, user_name, group_name):
    """Retrieve all groups in which a given user or group is a member."""
    content = GroupsApi(api_client).list_parents(user_name=user_name,
                                                 group_name=group_name)
    click.echo(pretty_format(content))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help="Removes a user or group from a group.")
@click.option("--parent-name", required=True,
              help=("Name of the parent group to which the new member will be "
                    " removed. This field is required."))
@click.option("--user-name", cls=OneOfOption, default=None, one_of=MEMBER_OPTIONS,
              help="The user name which will be removed from the parent group.")
@click.option("--group-name", cls=OneOfOption, default=None, one_of=MEMBER_OPTIONS,
              help="If group name which will be removed from the parent group.")
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def remove_member_cli(api_client, parent_name, user_name, group_name):
    GroupsApi(api_client).remove_member(parent_name=parent_name,
                                        user_name=user_name,
                                        group_name=group_name)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help="Remove a group from this organization.")
@click.option("--group-name", required=False)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_cli(api_client, group_name):
    """Remove a group from this organization."""
    content = GroupsApi(api_client).delete(group_name)
    click.echo(pretty_format(content))


@click.group(context_settings=CONTEXT_SETTINGS,
             short_help="Utility to interact with Databricks groups.")
@click.option("--version", "-v", is_flag=True, callback=print_version_callback,
              expose_value=False, is_eager=True, help=version)
@debug_option
@profile_option
@eat_exceptions
def groups_group():  # pragma: no cover
    """Provide utility to interact with Databricks groups."""
    pass


groups_group.add_command(add_member_cli, name="add-member")
groups_group.add_command(create_cli, name="create")
groups_group.add_command(list_members_cli, name="list-members")
groups_group.add_command(list_all_cli, name="list")
groups_group.add_command(list_parents_cli, name="list-parents")
groups_group.add_command(remove_member_cli, name="remove-member")
groups_group.add_command(delete_cli, name="delete")
