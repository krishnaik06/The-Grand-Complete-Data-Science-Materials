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

import json
import os
import sys

import click

from databricks_cli.configure.config import profile_option, debug_option
from databricks_cli.libraries.cli import libraries_group
from databricks_cli.version import print_version_callback, version
from databricks_cli.utils import CONTEXT_SETTINGS
from databricks_cli.configure.cli import configure_cli
from databricks_cli.dbfs.cli import dbfs_group
from databricks_cli.workspace.cli import workspace_group
from databricks_cli.jobs.cli import jobs_group
from databricks_cli.clusters.cli import clusters_group
from databricks_cli.cluster_policies.cli import cluster_policies_group
from databricks_cli.runs.cli import runs_group
from databricks_cli.secrets.cli import secrets_group
from databricks_cli.stack.cli import stack_group
from databricks_cli.groups.cli import groups_group
from databricks_cli.tokens.cli import tokens_group
from databricks_cli.instance_pools.cli import instance_pools_group
from databricks_cli.pipelines.cli import pipelines_group
from databricks_cli.repos.cli import repos_group
from databricks_cli.unity_catalog.cli import unity_catalog_group


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--version', '-v', is_flag=True, callback=print_version_callback,
              expose_value=False, is_eager=True, help=version)
@debug_option
@profile_option
def cli(**_):
    pass


cli.add_command(configure_cli, name='configure')
cli.add_command(dbfs_group, name='fs')
cli.add_command(workspace_group, name='workspace')
cli.add_command(jobs_group, name='jobs')
cli.add_command(clusters_group, name='clusters')
cli.add_command(cluster_policies_group, name='cluster-policies')
cli.add_command(runs_group, name='runs')
cli.add_command(libraries_group, name='libraries')
cli.add_command(secrets_group, name='secrets')
cli.add_command(stack_group, name='stack')
cli.add_command(groups_group, name='groups')
cli.add_command(tokens_group, name='tokens')
cli.add_command(instance_pools_group, name="instance-pools")
cli.add_command(pipelines_group, name='pipelines')
cli.add_command(repos_group, name='repos')
cli.add_command(unity_catalog_group, name='unity-catalog')


def _trampoline_into_new_cli():
    trampoline_disable_env_var = 'DATABRICKS_CLI_DO_NOT_EXECUTE_NEWER_VERSION'
    if os.environ.get(trampoline_disable_env_var) is not None:
        return

    # Try to trampoline only if we're running the CLI as 'databricks'.
    if os.path.basename(sys.argv[0]) != 'databricks':
        return

    # Check to see if the new version of the CLI is in $PATH.
    paths = os.environ['PATH'].split(os.pathsep)
    self = None
    self_version = version
    candidate = None
    for path in paths:
        exec_path = os.path.join(path, 'databricks')
        if os.name == 'nt':
            exec_path = os.path.join(path, 'databricks.exe')

        if not os.path.exists(exec_path):
            continue

        # Keep a pointer to the first 'databricks' in $PATH.
        if not self:
            self = exec_path

        # The new CLI is a single binary larger than 1MB.
        # We use this as heuristic to tell if the new CLI is installed.
        # Because this version of the CLI is much smaller, we do not
        # need to dedup our own path to avoid an exec loop.
        stat = os.stat(exec_path)
        if stat.st_size < (1024 * 1024):
            continue

        candidate = exec_path
        break

    # Return if we cannot find the new CLI in $PATH.
    if candidate is None:
        return

    # Determine the version of the new CLI.
    candidate_version_json = os.popen(candidate + ' version --output json').read().strip()
    try:
        candidate_version_obj = json.loads(candidate_version_json)
        candidate_version = candidate_version_obj['Version']
    except (RuntimeError, json.JSONDecodeError):
        candidate_version = '<unknown>'

    def e(message, highlight=False, nl=False):
        style = {}
        if not highlight:
            style["fg"] = 'yellow'

        click.echo(click.style(message, **style), err=True, nl=nl)

    e("Databricks CLI ")
    e("v{}".format(candidate_version), highlight=True)
    e(" found at ")
    e(candidate, highlight=True, nl=True)

    e("Your current $PATH prefers running CLI ")
    e("v{}".format(self_version), highlight=True)
    e(" at ")
    e(self, highlight=True, nl=True)

    e("", nl=True)

    e("Because both are installed and available in $PATH, " +
      "I assume you are trying to run the newer version.", nl=True)
    e("If you want to disable this behavior you can set " +
      "{}=1.".format(trampoline_disable_env_var), nl=True)

    e("", nl=True)

    e("Executing CLI ")
    e("v{}".format(candidate_version), highlight=True)
    e("...", nl=True)
    e("-" * (len("Executing CLI v{}...".format(candidate_version))), nl=True)

    # The new CLI is at least 1MB in size. This is a good heuristic to
    # determine if the new CLI is installed.
    os.execv(candidate, sys.argv)


def main():
    try:
        _trampoline_into_new_cli()
    except Exception as e: # noqa
        # Log the error and continue; perhaps a permissions issue?
        click.echo("Failed to look for newer version of CLI: {}".format(e), err=True)

    try:
        rv = cli(standalone_mode=False)
        if isinstance(rv, int):
            sys.exit(rv)
        sys.exit(0)
    except click.ClickException as e:
        e.show()
        message = """
Warning: The version of the CLI you are using is deprecated.
To migrate to the new CLI, see https://docs.databricks.com/dev-tools/cli/migrate.html.

In the new CLI, commands and flags might be different.
The preceding migration guide provides guidance about how to adapt your commands accordingly.
"""
        click.echo(click.style(message, fg='yellow'), err=True)
        sys.exit(e.exit_code)
    except click.Abort:
        click.utils.echo("Aborted!", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
