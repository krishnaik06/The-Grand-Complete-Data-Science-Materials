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

from click import ParamType

from databricks_cli.utils import error_and_quit


class DbfsPath(object):
    def __init__(self, absolute_path, validate=True):
        self.absolute_path = absolute_path
        if validate:
            self.validate()

    @classmethod
    def from_api_path(cls, path):
        return cls('dbfs:' + path)

    @classmethod
    def is_valid(cls, path):
        return cls(path, validate=False).is_absolute_path

    def validate(self):
        """
        Checks that the path is a proper DbfsPath. it must have a prefix of
        "dbfs:" and must be an absolute path.
        """
        if self.absolute_path.startswith('dbfs://'):
            error_and_quit(('The path {} cannot start with dbfs://. '
                           'It must start with dbfs:/').format(repr(self)))
        if not self.is_absolute_path:
            error_and_quit('The path {} must start with "{}"'.format(
                repr(self), repr(DbfsPath('dbfs:/'))))

    def join(self, file_name):
        """
        Returns a new extended DBFS path with a file_name.
        :param: file_name
        :type: str
        :rtype: DbfsPath
        """
        stripped_dbfs_path = self._strip_trailing_slash()
        if stripped_dbfs_path.is_root:
            absolute_path = stripped_dbfs_path.absolute_path + file_name
        else:
            absolute_path = stripped_dbfs_path.absolute_path + '/' + file_name
        return DbfsPath(absolute_path)

    def relpath(self, dbfs_path_prefix):
        """
        Strips the prefix of this DbfsPath. Behaves very similar to os.path.relpath
        """
        return os.path.relpath(self.absolute_path, dbfs_path_prefix.absolute_path)

    @property
    def basename(self):
        """
        This function is like the basename utility and is unlike os.path.basename.
        >>> assert DbfsPath('dbfs:/').basename == ''
        >>> assert DbfsPath('dbfs:/test').basename == 'test'
        >>> assert DbfsPath('dbfs:/test/').basename == 'test'
        """
        if self.is_root:
            return ''
        elif self.absolute_path[-1] == '/':
            return self.absolute_path.split('/')[-2]
        else:
            return self.absolute_path.split('/')[-1]

    @property
    def is_absolute_path(self):
        return self.absolute_path.startswith('dbfs:/')

    @property
    def is_root(self):
        return self.absolute_path == 'dbfs:/'

    def _strip_trailing_slash(self):
        if self.is_root:
            return DbfsPath('dbfs:/')
        elif self.absolute_path[-1] == '/':
            return DbfsPath(self.absolute_path[0:-1])
        else:
            return DbfsPath(self.absolute_path)

    def __repr__(self):
        return click.style(self.absolute_path, underline=True)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.absolute_path == other.absolute_path
        return False


class DbfsPathClickType(ParamType):
    name = 'Path'

    def convert(self, value, param, ctx):
        return DbfsPath(value)
