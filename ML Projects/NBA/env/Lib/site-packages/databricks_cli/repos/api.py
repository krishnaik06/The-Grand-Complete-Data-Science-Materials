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
import requests
from databricks_cli.sdk import ReposService, WorkspaceService


class ReposApi(object):
    def __init__(self, api_client):
        self.client = ReposService(api_client)
        self.ws_client = WorkspaceService(api_client)

    def get_repo_id(self, path):
        if not path.startswith("/Repos/"):
            raise ValueError("Path must start with /Repos/ !")

        if not len([x for x in path.split("/") if x]) == 3:
            raise ValueError("Repos paths must be in /Repos/{folder}/{repo} format!")

        try:
            status = self.ws_client.get_status(path)
            if status['object_type'] == 'REPO':
                return status['object_id']
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code != 404:
                jsn = ex.response.json()
                if 'message' in jsn:
                    msg = jsn['message']
                else:
                    msg = ex.response.reason
                raise RuntimeError(
                    "Error fetching repo ID for {path}: HTTP code: {code}, {ex}".format(
                        path=path, code=ex.response.status_code, ex=msg))

        raise RuntimeError("Can't find repo ID for {path}".format(path=path))

    def list(self, path_prefix, next_page_token):
        """
        List repos that the caller has Manage permissions on. Results are
        paginated with each page containing twenty repos.
        """
        return self.client.list_repos(path_prefix, next_page_token)

    def create(self, url, provider, path):
        """
        Creates a repo object and links it to the remote Git repo specified.
        """
        return self.client.create_repo(url, provider, path)

    def get(self, repo_id):
        """
        Gets the repo with the given ID.
        """
        return self.client.get_repo(repo_id)

    def update(self, repo_id, branch, tag):
        """
        Checks out the repo to the given branch or tag. Only one of ``branch``
        or ``tag`` should be provided.
        """
        assert bool(branch is not None) ^ bool(tag is not None)
        return self.client.update_repo(repo_id, branch, tag)

    def delete(self, repo_id):
        """
        Deletes the repo with the given ID.
        """
        return self.client.delete_repo(repo_id)
