# Databricks CLI
# Copyright 2018 Databricks, Inc.
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
import os
import json

import click

from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS
from databricks_cli.version import print_version_callback, version
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.stack.api import StackApi

DEBUG_MODE = True


def _generate_stack_status_path(stack_path):
    """
    Given a path to the stack configuration template JSON file, generates a path to where the
    deployment status JSON will be stored after successful deployment of the stack.

    :param stack_path: Path to the stack config template JSON file
    :return: The path to the stack status file.

    >>> self._generate_stack_status_path('./stack.json')
    './stack.deployed.json'
    """
    stack_status_insert = 'deployed'
    stack_path_split = stack_path.split('.')
    stack_path_split.insert(-1, stack_status_insert)
    return '.'.join(stack_path_split)


def _load_json(path):
    """
    Parse a json file to a readable dict format.
    Returns an empty dictionary if the path doesn't exist.

    :param path: File path of the JSON stack configuration template.
    :return: dict of parsed JSON stack config template.
    """
    stack_conf = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            stack_conf = json.load(f)
    return stack_conf


def _save_json(path, data):
    """
    Writes data to a JSON file.

    :param path: Path of JSON file.
    :param data: dict- data that wants to by written to JSON file
    :return: None
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Deploy a stack given a JSON configuration of the stack')
@click.argument('config_path', type=click.Path(exists=True), required=True)
@click.option('--overwrite', '-o', is_flag=True, default=False, show_default=True,
              help='Include to overwrite existing workspace notebooks and dbfs files')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def deploy(api_client, config_path, **kwargs):
    """
    Deploy a stack to the databricks workspace given a JSON stack configuration template.

    After deployment, a stack status will be saves at <config_file_name>.deployed.json. Please
    do not edit or move the file as it is generated through the CLI and is used for future
    deployments of the stack. If you run into errors with the stack status at deployment,
    please delete the stack status file and try the deployment again. If the problem persists,
    please raise a Github issue on the Databricks CLI repository at
    https://www.github.com/databricks/databricks-cli/issues
    """
    click.echo('#' * 80)
    click.echo('Deploying stack at: {} with options: {}'.format(config_path, kwargs))
    stack_config = _load_json(config_path)
    status_path = _generate_stack_status_path(config_path)
    stack_status = _load_json(status_path)
    config_dir = os.path.dirname(os.path.abspath(config_path))
    cli_dir = os.getcwd()
    os.chdir(config_dir)  # Switch current working directory to where json config is stored
    new_stack_status = StackApi(api_client).deploy(stack_config, stack_status, **kwargs)
    click.echo('#' * 80)
    os.chdir(cli_dir)
    click.echo("Saving stack status to {}".format(status_path))
    _save_json(status_path, new_stack_status)
    click.echo('Note: The stack status file is an automatically generated file that is'
               ' depended on for the databricks stack CLI to function correctly.'
               ' Please do not edit the file.')
    click.echo('#' * 80)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Download stack notebooks given a JSON configuration of the stack')
@click.argument('config_path', type=click.Path(exists=True), required=True)
@click.option('--overwrite', '-o', is_flag=True, help='Include to overwrite existing'
                                                      ' notebooks in the local filesystem.')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def download(api_client, config_path, **kwargs):
    """
    Download workspace notebooks of a stack to the local filesystem given a JSON stack
    configuration template.
    """
    click.echo('#' * 80)
    click.echo('Downloading stack at: {} with options: {}'.format(config_path, kwargs))
    stack_config = _load_json(config_path)
    config_dir = os.path.dirname(os.path.abspath(config_path))
    cli_dir = os.getcwd()
    os.chdir(config_dir)  # Switch current working directory to where json config is stored
    StackApi(api_client).download(stack_config, **kwargs)
    os.chdir(cli_dir)
    click.echo('#' * 80)


@click.group(context_settings=CONTEXT_SETTINGS,
             short_help='[Beta] Utility to deploy and download Databricks resource stacks.')
@click.option('--version', '-v', is_flag=True, callback=print_version_callback,
              expose_value=False, is_eager=True, help=version)
@debug_option
@profile_option
def stack_group():  # pragma: no cover
    """
    [Beta] Utility to deploy and download Databricks resource stacks.
    """
    pass


stack_group.add_command(deploy, name='deploy')
stack_group.add_command(download, name='download')
