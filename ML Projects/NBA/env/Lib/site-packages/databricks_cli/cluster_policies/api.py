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
from json import dumps as json_dumps

from databricks_cli.sdk import PolicyService


class ClusterPolicyApi(object):
    def __init__(self, api_client):
        self.client = PolicyService(api_client)

    @staticmethod
    def format_policy_for_api(policy):
        if isinstance(policy.get("definition"), dict):
            policy["definition"] = json_dumps(policy["definition"])
        return policy

    def create_cluster_policy(self, json):
        return self.client.client.perform_query(
            "POST",
            "/policies/clusters/create",
            data=ClusterPolicyApi.format_policy_for_api(json),
        )

    def edit_cluster_policy(self, json):
        return self.client.client.perform_query(
            "POST",
            "/policies/clusters/edit",
            data=ClusterPolicyApi.format_policy_for_api(json),
        )

    def delete_cluster_policy(self, policy_id):
        return self.client.delete_policy(policy_id)

    def get_cluster_policy(self, policy_id):
        return self.client.get_policy(policy_id)

    def list_cluster_policies(self):
        return self.client.list_policies()
