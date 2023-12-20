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

from base64 import b64encode, b64decode

import os
import shutil
import tempfile

import re
import click

from requests.exceptions import HTTPError

from databricks_cli.sdk import DbfsService
from databricks_cli.utils import error_and_quit
from databricks_cli.dbfs.dbfs_path import DbfsPath
from databricks_cli.dbfs.exceptions import LocalFileExistsException

BUFFER_SIZE_BYTES = 2**20


class ParseException(Exception):
    pass


class FileInfo(object):
    def __init__(self, dbfs_path, is_dir, file_size, modification_time):
        self.dbfs_path = dbfs_path
        self.is_dir = is_dir
        self.file_size = file_size
        self.modification_time = modification_time

    def to_row(self, is_long_form, is_absolute):
        path = self.dbfs_path.absolute_path if is_absolute else self.dbfs_path.basename
        stylized_path = click.style(path, 'cyan') if self.is_dir else path
        if is_long_form:
            filetype = 'dir' if self.is_dir else 'file'
            row = [filetype, self.file_size, stylized_path]
            # Add modification time if it is available.
            if self.modification_time is not None:
                row.append(self.modification_time)
            return row
        return [stylized_path]

    @classmethod
    def from_json(cls, json):
        dbfs_path = DbfsPath.from_api_path(json['path'])
        # If JSON doesn't include modification_time data, replace it with None.
        modification_time = json['modification_time'] if 'modification_time' in json else None
        return cls(dbfs_path, json['is_dir'], json['file_size'], modification_time)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.dbfs_path == other.dbfs_path and \
                self.is_dir == other.is_dir and \
                self.file_size == other.file_size and \
                self.modification_time == other.modification_time
        return False


class DbfsErrorCodes(object):
    RESOURCE_DOES_NOT_EXIST = 'RESOURCE_DOES_NOT_EXIST'
    RESOURCE_ALREADY_EXISTS = 'RESOURCE_ALREADY_EXISTS'
    PARTIAL_DELETE = 'PARTIAL_DELETE'


class DbfsApi(object):
    MULTIPART_UPLOAD_LIMIT = 2147483648

    def __init__(self, api_client):
        self.client = DbfsService(api_client)

    def list_files(self, dbfs_path, headers=None):
        list_response = self.client.list(dbfs_path.absolute_path, headers=headers)
        if 'files' in list_response:
            return [FileInfo.from_json(f) for f in list_response['files']]
        else:
            return []

    def file_exists(self, dbfs_path, headers=None):
        try:
            self.get_status(dbfs_path, headers=headers)
        except HTTPError as e:
            try:
                if e.response.json()['error_code'] == DbfsErrorCodes.RESOURCE_DOES_NOT_EXIST:
                    return False
            except ValueError:
                pass

            raise e
        return True

    def get_status(self, dbfs_path, headers=None):
        json = self.client.get_status(dbfs_path.absolute_path, headers=headers)
        return FileInfo.from_json(json)

    # Method makes multipart/form-data file upload for files <2GB.
    # Otherwise uses create, add-block, close methods for streaming upload.
    def put_file(self, src_path, dbfs_path, overwrite, headers=None):
        # If file size is >2Gb use streaming upload.
        if os.path.getsize(src_path) < self.MULTIPART_UPLOAD_LIMIT:
            self.client.put(dbfs_path.absolute_path, src_path=src_path,
                            overwrite=overwrite, headers=headers)
        else:
            handle = self.client.create(dbfs_path.absolute_path, overwrite,
                                        headers=headers)['handle']
            with open(src_path, 'rb') as local_file:
                while True:
                    contents = local_file.read(BUFFER_SIZE_BYTES)
                    if len(contents) == 0:
                        break
                    # add_block should not take a bytes object.
                    self.client.add_block(handle, b64encode(contents).decode(), headers=headers)
                self.client.close(handle, headers=headers)

    def get_file(self, dbfs_path, dst_path, overwrite, headers=None):
        if os.path.exists(dst_path) and not overwrite:
            raise LocalFileExistsException('{} exists already.'.format(dst_path))
        file_info = self.get_status(dbfs_path, headers=headers)
        if file_info.is_dir:
            error_and_quit(('The dbfs file {} is a directory.').format(repr(dbfs_path)))
        length = file_info.file_size
        offset = 0
        with open(dst_path, 'wb') as local_file:
            while offset < length:
                response = self.client.read(dbfs_path.absolute_path, offset, BUFFER_SIZE_BYTES,
                                            headers=headers)
                bytes_read = response['bytes_read']
                data = response['data']
                offset += bytes_read
                local_file.write(b64decode(data))

    @staticmethod
    def get_num_files_deleted(partial_delete_error):
        try:
            message = partial_delete_error.response.json()['message']
        except (AttributeError, KeyError):
            raise ParseException("Unable to retrieve the number of deleted files.")
        m = re.compile(r".*operation has deleted (\d+) files.*").match(message)
        if not m:
            raise ParseException(
                "Unable to retrieve the number of deleted files from the error message: {}".format(
                    message))
        return int(m.group(1))

    def delete(self, dbfs_path, recursive, headers=None):
        num_files_deleted = 0
        while True:
            try:
                self.client.delete(dbfs_path.absolute_path, recursive=recursive, headers=headers)
            except HTTPError as e:
                if e.response.status_code == 503:
                    try:
                        error_code = e.response.json()['error_code']
                    except (AttributeError, KeyError):
                        error_code = None
                    # Handle partial delete exceptions: retry until all the files have been deleted
                    if error_code == DbfsErrorCodes.PARTIAL_DELETE:
                        try:
                            num_files_deleted += DbfsApi.get_num_files_deleted(e)
                            click.echo("\rDeleted {} files. Delete in progress...\033[K".format(
                                num_files_deleted), nl=False)
                        except ParseException:
                            click.echo("\rDelete in progress...\033[K", nl=False)
                        continue
                click.echo("\rDeleted at least {} files but interrupted by error.\033[K".format(
                    num_files_deleted))
                raise e
            break
        click.echo("\rDelete finished successfully.\033[K")

    def mkdirs(self, dbfs_path, headers=None):
        self.client.mkdirs(dbfs_path.absolute_path, headers=headers)

    def move(self, dbfs_src, dbfs_dst, headers=None):
        self.client.move(dbfs_src.absolute_path, dbfs_dst.absolute_path, headers=headers)

    def _copy_to_dbfs_non_recursive(self, src, dbfs_path_dst, overwrite, headers=None):
        # Munge dst path in case dbfs_path_dst is a dir
        try:
            if self.get_status(dbfs_path_dst, headers=headers).is_dir:
                dbfs_path_dst = dbfs_path_dst.join(os.path.basename(src))
        except HTTPError as e:
            if e.response.json()['error_code'] == DbfsErrorCodes.RESOURCE_DOES_NOT_EXIST:
                pass
            else:
                raise e
        self.put_file(src, dbfs_path_dst, overwrite, headers=headers)

    def _copy_from_dbfs_non_recursive(self, dbfs_path_src, dst, overwrite, headers=None):
        # Munge dst path in case dst is a dir
        if os.path.isdir(dst):
            dst = os.path.join(dst, dbfs_path_src.basename)
        self.get_file(dbfs_path_src, dst, overwrite, headers=headers)

    def _copy_to_dbfs_recursive(self, src, dbfs_path_dst, overwrite, headers=None):
        try:
            self.mkdirs(dbfs_path_dst, headers=headers)
        except HTTPError as e:
            if e.response.json()['error_code'] == DbfsErrorCodes.RESOURCE_ALREADY_EXISTS:
                click.echo(e.response.json())
                return
        for filename in os.listdir(src):
            cur_src = os.path.join(src, filename)
            cur_dbfs_dst = dbfs_path_dst.join(filename)
            if os.path.isdir(cur_src):
                self._copy_to_dbfs_recursive(cur_src, cur_dbfs_dst, overwrite, headers=headers)
            elif os.path.isfile(cur_src):
                try:
                    self.put_file(cur_src, cur_dbfs_dst, overwrite, headers=headers)
                    click.echo('{} -> {}'.format(cur_src, cur_dbfs_dst))
                except HTTPError as e:
                    if e.response.json()['error_code'] == DbfsErrorCodes.RESOURCE_ALREADY_EXISTS:
                        click.echo('{} already exists. Skip.'.format(cur_dbfs_dst))
                    else:
                        raise e

    def _copy_from_dbfs_recursive(self, dbfs_path_src, dst, overwrite, headers=None):
        if os.path.isfile(dst):
            click.echo(
                '{} exists as a file. Skipping this subtree {}'.format(dst, repr(dbfs_path_src)))
            return
        elif not os.path.isdir(dst):
            os.makedirs(dst)

        for dbfs_src_file_info in self.list_files(dbfs_path_src, headers=headers):
            cur_dbfs_src = dbfs_src_file_info.dbfs_path
            cur_dst = os.path.join(dst, cur_dbfs_src.basename)
            if dbfs_src_file_info.is_dir:
                self._copy_from_dbfs_recursive(cur_dbfs_src, cur_dst, overwrite, headers=headers)
            else:
                try:
                    self.get_file(cur_dbfs_src, cur_dst, overwrite, headers=headers)
                    click.echo('{} -> {}'.format(cur_dbfs_src, cur_dst))
                except LocalFileExistsException:
                    click.echo(('{} already exists locally as {}. Skip. To overwrite, you ' +
                                'should provide the --overwrite flag.').format(cur_dbfs_src,
                                                                               cur_dst))

    def cp(self, recursive, overwrite, src, dst, headers=None):
        if not DbfsPath.is_valid(src) and DbfsPath.is_valid(dst):
            if not os.path.exists(src):
                error_and_quit('The local file {} does not exist.'.format(src))
            if not recursive:
                if os.path.isdir(src):
                    error_and_quit(
                        ('The local file {} is a directory. You must provide --recursive')
                        .format(src))
                self._copy_to_dbfs_non_recursive(src, DbfsPath(dst), overwrite, headers=headers)
            else:
                if not os.path.isdir(src):
                    self._copy_to_dbfs_non_recursive(src, DbfsPath(dst), overwrite, headers=headers)
                    return
                self._copy_to_dbfs_recursive(src, DbfsPath(dst), overwrite, headers=headers)
        # Copy from DBFS in this case
        elif DbfsPath.is_valid(src) and not DbfsPath.is_valid(dst):
            if not recursive:
                self._copy_from_dbfs_non_recursive(DbfsPath(src), dst, overwrite, headers=headers)
            else:
                dbfs_path_src = DbfsPath(src)
                if not self.get_status(dbfs_path_src, headers=headers).is_dir:
                    self._copy_from_dbfs_non_recursive(dbfs_path_src, dst, overwrite,
                                                       headers=headers)
                self._copy_from_dbfs_recursive(dbfs_path_src, dst, overwrite, headers=headers)
        elif not DbfsPath.is_valid(src) and not DbfsPath.is_valid(dst):
            error_and_quit('Both paths provided are from your local filesystem. '
                           'To use this utility, one of the src or dst must be prefixed '
                           'with dbfs:/')
        elif DbfsPath.is_valid(src) and DbfsPath.is_valid(dst):
            with TempDir() as temp_dir:
                # Always copy to <temp_dir>/temp since this will work no matter if it's a
                # recursive or a non-recursive copy.
                temp_path = temp_dir.path('temp')
                self.cp(recursive, True, src, temp_path)
                self.cp(recursive, overwrite, temp_path, dst)
        else:
            assert False, 'not reached'

    def cat(self, src):
        with TempDir() as temp_dir:
            temp_path = temp_dir.path('temp')
            self.cp(False, True, src, temp_path)
            with open(temp_path) as f:
                click.echo(f.read(), nl=False)


class TempDir(object):
    def __init__(self, remove_on_exit=True):
        self._dir = None
        self._path = None
        self._remove = remove_on_exit

    def __enter__(self):
        self._path = os.path.abspath(tempfile.mkdtemp())
        assert os.path.exists(self._path)
        return self

    def __exit__(self, tp, val, traceback):
        if self._remove and os.path.exists(self._path):
            shutil.rmtree(self._path)

        assert not self._remove or not os.path.exists(self._path)
        assert os.path.exists(os.getcwd())

    def path(self, *path):
        return os.path.join(self._path, *path)
