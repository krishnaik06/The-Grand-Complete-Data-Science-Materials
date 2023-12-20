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

from hashlib import sha1
import os
import copy

from six.moves import urllib

from databricks_cli.sdk import DeltaPipelinesService
from databricks_cli.dbfs.api import DbfsApi
from databricks_cli.dbfs.dbfs_path import DbfsPath

BUFFER_SIZE = 1024 * 64
base_pipelines_dir = 'dbfs:/pipelines/code'


class PipelinesApi(object):
    def __init__(self, api_client):
        self.client = DeltaPipelinesService(api_client)
        self.dbfs_client = DbfsApi(api_client)

    def create(self, settings, settings_dir, allow_duplicate_names, headers=None):
        data = self._upload_libraries_and_update_settings(settings, settings_dir)
        data['allow_duplicate_names'] = allow_duplicate_names
        return self.client.client.perform_query('POST', '/pipelines', data=data,
                                                headers=headers)

    def edit(self, settings, settings_dir, allow_duplicate_names, headers=None):
        data = self._upload_libraries_and_update_settings(settings, settings_dir)
        data['allow_duplicate_names'] = allow_duplicate_names
        pipeline_id = data['id']
        self.client.client.perform_query('PUT', '/pipelines/{}'.format(pipeline_id), data=data,
                                         headers=headers)

    def delete(self, pipeline_id, headers=None):
        self.client.delete(pipeline_id, headers)

    def get(self, pipeline_id, headers=None):
        return self.client.get(pipeline_id, headers)

    def list(self, headers=None):
        def call(page_token=None, max_results=None, order_by=None):
            _data = {}
            if page_token:
                _data["page_token"] = page_token
            if max_results:
                _data["max_results"] = max_results
            if order_by:
                _data["order_by"] = order_by

            return self.client.client.perform_query(
                'GET', '/pipelines', data=_data, headers=headers)

        response = call()
        pipelines = response.get("statuses", [])

        while "next_page_token" in response:
            response = call(page_token=response["next_page_token"])
            pipelines.extend(response.get("statuses", []))
        return pipelines

    def start_update(self, pipeline_id, full_refresh=None, headers=None):
        return self.client.start_update(pipeline_id, full_refresh=full_refresh, headers=headers)

    def stop(self, pipeline_id, headers=None):
        self.client.stop(pipeline_id, headers)

    def _upload_libraries_and_update_settings(self, settings, settings_dir):
        settings = copy.deepcopy(settings)
        lib_objects = LibraryObject.from_json(settings.get('libraries', []))
        local_lib_objects, external_lib_objects = self._identify_local_libraries(lib_objects)

        settings['libraries'] = LibraryObject.to_json(
            external_lib_objects + self._upload_local_libraries(
                settings_dir, local_lib_objects))
        return settings

    @staticmethod
    def _identify_local_libraries(lib_objects):
        """
        Partitions the given set of libraries into local libraries i.e. libraries that should
        be uploaded to DBFS, and non-local libraries. Jars or whls with a file scheme or no scheme
        at all are (currently) considered local libraries.

        :param lib_objects: List[LibraryObject]
        :return: List[List[LibraryObject], List[LibraryObject]] ([Local, External])
        """
        local_lib_objects, external_lib_objects = [], []
        for lib_object in lib_objects:
            if lib_object.lib_type not in ['jar', 'whl']:
                external_lib_objects.append(lib_object)
                continue

            parsed_uri = urllib.parse.urlparse(lib_object.path)
            if parsed_uri.scheme == '':
                local_lib_objects.append(lib_object)
            elif parsed_uri.scheme.lower() == 'file':
                # exactly 1 or 3
                if parsed_uri.path.startswith('//') or parsed_uri.netloc != '':
                    raise RuntimeError('invalid file uri scheme, '
                                       'did you mean to use file:/ or file:///')
                local_lib_objects.append(LibraryObject(lib_object.lib_type, parsed_uri.path))
            else:
                external_lib_objects.append(lib_object)
        return local_lib_objects, external_lib_objects

    def _upload_local_libraries(self, settings_dir, local_lib_objects):
        relative_local_lib_objects = [
            LibraryObject(
                llo.lib_type, os.path.join(settings_dir, llo.path)) for llo in local_lib_objects]
        remote_lib_objects = [LibraryObject(rllo.lib_type, self._get_hashed_path(rllo.path))
                              for rllo in relative_local_lib_objects]
        transformed_remote_lib_objects = [LibraryObject(rlo.lib_type, DbfsPath(rlo.path))
                                          for rlo in remote_lib_objects]
        upload_files = [llo_tuple for llo_tuple in
                        zip(relative_local_lib_objects, transformed_remote_lib_objects)
                        if not self.dbfs_client.file_exists(llo_tuple[1].path)]

        for llo, rlo in upload_files:
            self.dbfs_client.put_file(llo.path, rlo.path, False)

        return remote_lib_objects

    @staticmethod
    def _get_hashed_path(path):
        """
        Finds the corresponding dbfs file path for the file located at the supplied path by
        calculating its hash using SHA1.
        :param path: Local File Path
        :return: Remote Path (pipeline_base_dir + file_hash (dot) file_extension)
        """
        hash_buffer = sha1()
        with open(path, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                hash_buffer.update(data)

        file_hash = hash_buffer.hexdigest()
        # splitext includes the period in the extension
        extension = os.path.splitext(path)[1][1:]
        if extension == 'whl':
            # Wheels need to follow the format described in the PEP, so we simply
            # pre-pend the content hash to the wheel_name
            # basename in Python returns the extension as well
            wheel_name = os.path.basename(path)
            path = '{}/{}/{}'.format(base_pipelines_dir, file_hash, wheel_name)
        else:
            path = '{}/{}.{}'.format(base_pipelines_dir, file_hash, extension)
        return path


class LibraryObject(object):
    def __init__(self, lib_type, lib_path):
        self.path = lib_path
        self.lib_type = lib_type

    @classmethod
    def from_json(cls, libraries):
        """
        Serialize Libraries into LibraryObjects
        :param libraries: List[Dictionary{String, String}]
        :return: List[LibraryObject]
        """
        lib_objects = []
        for library in libraries:
            for lib_type, path in library.items():
                lib_objects.append(LibraryObject(lib_type, path))
        return lib_objects

    @classmethod
    def to_json(cls, lib_objects):
        """
        Deserialize LibraryObjects
        :param lib_objects: List[LibraryObject]
        :return: List[Dictionary{String, String}]
        """
        libraries = []
        for lib_object in lib_objects:
            libraries.append({lib_object.lib_type: lib_object.path})
        return libraries

    def __eq__(self, other):
        if not isinstance(other, LibraryObject):
            return NotImplemented
        return self.path == other.path and self.lib_type == other.lib_type
