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
from base64 import b64encode, b64decode

import click

from databricks_cli.dbfs.exceptions import LocalFileExistsException
from databricks_cli.sdk import WorkspaceService
from databricks_cli.workspace.types import WorkspaceFormat, WorkspaceLanguage

DIRECTORY = 'DIRECTORY'
NOTEBOOK = 'NOTEBOOK'
LIBRARY = 'LIBRARY'
REPO = 'REPO'


class WorkspaceFileInfo(object):
    def __init__(self, path, object_type, object_id, language=None, **kwargs): # noqa
        self.path = path
        self.object_type = object_type
        self.language = language
        self.object_id = object_id

    def to_row(self, is_long_form, is_absolute, with_object_id=False):
        path = self.path if is_absolute else self.basename
        if self.is_dir:
            stylized_path = click.style(path, 'cyan')
        elif self.is_library:
            stylized_path = click.style(path, 'green')
        else:
            stylized_path = path

        result = [stylized_path]

        if is_long_form:
            result = [self.object_type, stylized_path, self.language]

        if with_object_id:
            result.append(self.object_id)

        return result

    @property
    def is_dir(self):
        return self.object_type == DIRECTORY

    @property
    def is_notebook(self):
        return self.object_type == NOTEBOOK

    @property
    def is_library(self):
        return self.object_type == LIBRARY

    @property
    def basename(self):
        return os.path.basename(self.path)

    @classmethod
    def from_json(cls, deserialized_json):
        return cls(**deserialized_json)


class WorkspaceApi(object):
    def __init__(self, api_client):
        self.client = WorkspaceService(api_client)

    def get_status(self, workspace_path, headers=None):
        return WorkspaceFileInfo.from_json(self.client.get_status(workspace_path, headers=headers))

    def list_objects(self, workspace_path, headers=None):
        response = self.client.list(workspace_path, headers=headers)
        # This case is necessary when we list an empty dir in the workspace.
        # TODO(andrewmchen): We should make our API respond with a json with 'objects' field even
        # in this case.
        if 'objects' not in response:
            return []
        objects = response['objects']
        return [WorkspaceFileInfo.from_json(f) for f in objects]

    def mkdirs(self, workspace_path, headers=None):
        self.client.mkdirs(workspace_path, headers=headers)

    def import_workspace(self, source_path, target_path, language, fmt, is_overwrite, headers=None):
        with open(source_path, 'rb') as f:
            # import_workspace must take content that is typed str.
            content = b64encode(f.read()).decode()
            self.client.import_workspace(
                target_path,
                fmt,
                language,
                content,
                is_overwrite,
                headers=headers)

    def export_workspace(self, source_path, target_path, fmt, is_overwrite, headers=None):
        """
        Faithfully exports the source_path to the target_path. Does not
        attempt to do any munging of the target_path if it is a directory.
        """
        if os.path.exists(target_path) and not is_overwrite:
            raise LocalFileExistsException('Target {} already exists.'.format(target_path))
        output = self.client.export_workspace(source_path, fmt, headers=headers)
        content = output['content']
        # Will overwrite target_path.
        with open(target_path, 'wb') as f:
            decoded = b64decode(content)
            f.write(decoded)

    def delete(self, workspace_path, is_recursive, headers=None):
        self.client.delete(workspace_path, is_recursive, headers=headers)

    def import_workspace_dir(self, source_path, target_path, overwrite, exclude_hidden_files,
                             headers=None):
        # pylint: disable=too-many-locals
        filenames = os.listdir(source_path)
        if exclude_hidden_files:
            # for now, just exclude hidden files or directories based on starting '.'
            filenames = [f for f in filenames if not f.startswith('.')]
        self.mkdirs(target_path, headers=headers)
        for filename in filenames:
            cur_src = os.path.join(source_path, filename)
            # don't use os.path.join here since it will set \ on Windows
            cur_dst = target_path.rstrip('/') + '/' + filename
            if os.path.isdir(cur_src):
                self.import_workspace_dir(cur_src, cur_dst, overwrite, exclude_hidden_files,
                                          headers=headers)
            elif os.path.isfile(cur_src):
                ext = WorkspaceLanguage.get_extension(cur_src)
                if ext != '':
                    cur_dst = cur_dst[:-len(ext)]
                    (language, file_format) = WorkspaceLanguage.to_language_and_format(cur_src)
                    self.import_workspace(cur_src, cur_dst, language, file_format, overwrite,
                                          headers=headers)
                    click.echo('{} -> {}'.format(cur_src, cur_dst))
                else:
                    extensions = ', '.join(WorkspaceLanguage.EXTENSIONS)
                    click.echo(('{} does not have a valid extension of {}. Skip this file and ' +
                                'continue.').format(cur_src, extensions))

    def export_workspace_dir(self, source_path, target_path, overwrite, headers=None):
        if os.path.isfile(target_path):
            click.echo('{} exists as a file. Skipping this subtree {}'
                       .format(target_path, source_path))
            return
        if not os.path.isdir(target_path):
            os.makedirs(target_path)
        for obj in self.list_objects(source_path, headers=headers):
            cur_src = obj.path
            cur_dst = os.path.join(target_path, obj.basename)
            if obj.is_dir:
                self.export_workspace_dir(cur_src, cur_dst, overwrite, headers=headers)
            elif obj.is_notebook:
                cur_dst = cur_dst + WorkspaceLanguage.to_extension(obj.language)
                try:
                    self.export_workspace(cur_src, cur_dst, WorkspaceFormat.SOURCE, overwrite,
                                          headers=headers)
                    click.echo('{} -> {}'.format(cur_src, cur_dst))
                except LocalFileExistsException:
                    click.echo('{} already exists locally as {}. Skip.'.format(cur_src, cur_dst))
            else:
                click.echo('{} is neither a dir or a notebook. Skip.'.format(cur_src))
