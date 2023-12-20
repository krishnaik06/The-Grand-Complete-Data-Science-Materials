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
from databricks_cli.sdk import ClusterService


class ClusterApi(object):
    def __init__(self, api_client):
        self.client = ClusterService(api_client)

    def create_cluster(self, json):
        return self.client.client.perform_query('POST', '/clusters/create', data=json)

    def edit_cluster(self, json):
        return self.client.client.perform_query('POST', '/clusters/edit', data=json)

    def start_cluster(self, cluster_id):
        return self.client.start_cluster(cluster_id)

    def restart_cluster(self, cluster_id):
        return self.client.restart_cluster(cluster_id)

    def resize_cluster(self, cluster_id, num_workers):
        return self.client.resize_cluster(cluster_id, num_workers=num_workers)

    def delete_cluster(self, cluster_id):
        return self.client.delete_cluster(cluster_id)

    def get_cluster(self, cluster_id):
        return self.client.get_cluster(cluster_id)

    def list_clusters(self):
        return self.client.list_clusters()

    def list_zones(self):
        return self.client.list_available_zones()

    def list_node_types(self):
        return self.client.list_node_types()

    def spark_versions(self):
        return self.client.list_spark_versions()

    def permanent_delete(self, cluster_id):
        return self.client.permanent_delete_cluster(cluster_id)

    def get_cluster_ids_by_name(self, cluster_name):
        data = self.client.list_clusters()
        return [c for c in data.get('clusters', []) if c.get('cluster_name') == cluster_name]

    def get_cluster_id_for_name(self, cluster_name):
        """
        Given a cluster name, this will return a single cluster id for that name.
        If there are multiple clusters with the same name it will raise a RuntimeError.
        If there are no clusters with the name it will raise a RuntimeError.
        """
        clusters_by_name = self.get_cluster_ids_by_name(cluster_name)
        cluster_ids = [
            cluster['cluster_id'] for cluster in clusters_by_name if
            cluster and 'cluster_id' in cluster
        ]

        if len(cluster_ids) == 0:
            raise RuntimeError('No clusters with name {} were found'.format(cluster_name))

        if len(cluster_ids) > 1:
            raise RuntimeError('More than 1 cluster was named {}, '.format(cluster_name) +
                               'please use --cluster-id.\n' +
                               'Cluster ids found: {}'.format(', '.join(cluster_ids))
                               )
        return cluster_ids[0]

    def get_cluster_by_name(self, cluster_name):
        """
        Given a cluster name, this will return the cluster config for that cluster.
        If there are multiple clusters with the same name it will raise a RuntimeError.
        If there are no clusters with the name it will raise a RuntimeError.
        """
        cluster_id = self.get_cluster_id_for_name(cluster_name)
        return self.get_cluster(cluster_id)

    def get_events(self, cluster_id, start_time, end_time, order, event_types, offset, limit):
        return self.client.get_events(cluster_id, start_time, end_time, order, event_types,
                                      offset, limit)
