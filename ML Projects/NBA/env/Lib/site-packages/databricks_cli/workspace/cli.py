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

import os
import click
from tabulate import tabulate

from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS
from databricks_cli.version import print_version_callback, version
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.workspace.api import WorkspaceApi
from databricks_cli.workspace.types import LanguageClickType, FormatClickType, WorkspaceFormat, \
    WorkspaceLanguage


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='List objects in the Databricks Workspace. ls and list are synonyms.')
@click.option('--absolute', is_flag=True, default=False,
              help='Displays absolute paths.')
@click.option('-l', '--long', 'is_long_form', is_flag=True, default=False,
              help='Displays full information including ObjectType, Path, Language')
@click.option('-i', '--id', 'with_object_id', is_flag=True, default=False,
              help='Displays ObjectId')
@click.argument('workspace_path', type=str, nargs=-1)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def ls_cli(api_client, is_long_form, with_object_id, absolute, workspace_path): # noqa
    """
    List objects in the Databricks Workspace.
    """
    if len(workspace_path) == 0:
        workspace_path = '/'
    else:
        workspace_path = workspace_path[0]
    objects = WorkspaceApi(api_client).list_objects(workspace_path)
    objects_table = [
        obj.to_row(is_long_form=is_long_form, is_absolute=absolute, with_object_id=with_object_id)
        for obj in objects
    ]
    table = tabulate(objects_table, tablefmt='plain')
    click.echo(table)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Make directories in the Databricks Workspace.')
@click.argument('workspace_path')
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def mkdirs_cli(api_client, workspace_path):
    """
    Make directories in the Databricks Workspace.

    Mkdirs will create directories along the path to the argument directory.
    """
    WorkspaceApi(api_client).mkdirs(workspace_path)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Imports a file from local to the Databricks workspace.')
@click.argument('source_path')
@click.argument('target_path')
@click.option('--language', '-l', required=True, type=LanguageClickType(),
              help=', '.join(WorkspaceLanguage.ALL))
@click.option('--format', '-f', default=WorkspaceFormat.SOURCE, type=FormatClickType())
@click.option('--overwrite', '-o', is_flag=True, default=False)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def import_workspace_cli(api_client, source_path, target_path, language, format, overwrite): # NOQA
    """
    Imports a file from local to the Databricks workspace.

    The format is by default SOURCE. Possible formats are SOURCE, HTML, JUPYTER, and DBC. Each
    format is documented at
    https://docs.databricks.com/api/latest/workspace.html#notebookexportformat.
    """
    WorkspaceApi(api_client).import_workspace(source_path, target_path, language, format, overwrite) # NOQA


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Exports a file from the Databricks workspace.')
@click.argument('source_path')
@click.argument('target_path')
@click.option('--format', '-f', default=WorkspaceFormat.SOURCE, type=FormatClickType())
@click.option('--overwrite', '-o', is_flag=True, default=False)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def export_workspace_cli(api_client, source_path, target_path, format, overwrite): # NOQA
    """
    Exports a notebook from the Databricks workspace.

    The format is by default SOURCE. Possible formats are SOURCE, HTML, JUPYTER, and DBC. Each
    format is documented at
    https://docs.databricks.com/api/latest/workspace.html#notebookexportformat.
    """
    if os.path.isdir(target_path):
        file_info = WorkspaceApi(api_client).get_status(source_path)
        if not file_info.is_notebook:
            raise RuntimeError('Export can only be called on a notebook.')
        extension = WorkspaceLanguage.to_extension(file_info.language)
        target_path = os.path.join(target_path, file_info.basename + extension)
    WorkspaceApi(api_client).export_workspace(source_path, target_path, format, overwrite) # NOQA


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Deletes objects from the Databricks workspace. '
                          'rm and delete are synonyms.')
@click.argument('workspace_path')
@click.option('--recursive', '-r', is_flag=True, default=False)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_cli(api_client, workspace_path, recursive):
    """
    Deletes objects from the Databricks workspace.

    To delete a folder add the recursive flag.
    """
    WorkspaceApi(api_client).delete(workspace_path, recursive)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Recursively exports a directory from the Databricks workspace.')
@click.argument('source_path')
@click.argument('target_path')
@click.option('--overwrite', '-o', is_flag=True, default=False)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def export_dir_cli(api_client, source_path, target_path, overwrite):
    """
    Recursively exports a directory from the Databricks workspace.

    Only directories and notebooks are exported. Notebooks are always exported in the SOURCE
    format. Notebooks will also have the extension of .scala, .py, .sql, or .r appended
    depending on the language type.
    """
    workspace_api = WorkspaceApi(api_client)
    assert workspace_api.get_status(source_path).is_dir, 'The source path must be a directory. {}' \
        .format(source_path)
    workspace_api.export_workspace_dir(source_path, target_path, overwrite)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Recursively imports a directory to the Databricks workspace.')
@click.argument('source_path')
@click.argument('target_path')
@click.option('--overwrite', '-o', is_flag=True, default=False)
@click.option('--exclude-hidden-files', '-e', is_flag=True, default=False)
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def import_dir_cli(api_client, source_path, target_path, overwrite, exclude_hidden_files):
    """
    Recursively imports a directory from local to the Databricks workspace.

    Only directories and files with the extensions .scala, .py, .sql, .r, .R, .ipynb are imported.
    When imported, these extensions will be stripped off the name of the notebook.
    """
    WorkspaceApi(api_client).import_workspace_dir(source_path, target_path, overwrite,
                                                  exclude_hidden_files)


@click.group(context_settings=CONTEXT_SETTINGS,
             short_help='Utility to interact with the Databricks workspace.')
@click.option('--version', '-v', is_flag=True, callback=print_version_callback,
              expose_value=False, is_eager=True, help=version)
@debug_option
@profile_option
def workspace_group():  # pragma: no cover
    """
    Utility to interact with the Databricks workspace.
    Workspace paths must be absolute and be prefixed with `/`.
    """
    pass


workspace_group.add_command(ls_cli, name='ls')
workspace_group.add_command(ls_cli, name='list')
workspace_group.add_command(mkdirs_cli, name='mkdirs')
workspace_group.add_command(import_workspace_cli, name='import')
workspace_group.add_command(export_workspace_cli, name='export')
workspace_group.add_command(delete_cli, name='delete')
workspace_group.add_command(delete_cli, name='rm')
workspace_group.add_command(export_dir_cli, name='export_dir')
workspace_group.add_command(import_dir_cli, name='import_dir')
