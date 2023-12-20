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

from databricks_cli.sdk import JobsService


class RunsApi(object):
    def __init__(self, api_client):
        self.client = JobsService(api_client)

    def submit_run(self, json, version=None):
        return self.client.client.perform_query('POST', '/jobs/runs/submit', data=json,
                                                version=version)

    def list_runs(self, job_id, active_only, completed_only, offset, limit, version=None):
        return self.client.list_runs(job_id, active_only, completed_only, offset, limit,
                                     version=version)

    def get_run(self, run_id, version=None):
        return self.client.get_run(run_id, version=version)

    def cancel_run(self, run_id, version=None):
        return self.client.cancel_run(run_id, version=version)

    def get_run_output(self, run_id, version=None):
        return self.client.get_run_output(run_id, version=version)
