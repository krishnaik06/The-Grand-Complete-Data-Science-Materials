# Databricks CLI
# Copyright 2022 Databricks, Inc.
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
#

from databricks_cli.unity_catalog.utils import mc_pretty_format


class UnityCatalogService(object):
    def __init__(self, client):
        self.client = client

    # Metastore Operations

    def create_metastore(self, name, storage_root, region, headers=None):
        _data = {
            'name': name,
            'storage_root': storage_root,
        }
        if region is not None:
            _data['region'] = region
        return self.client.perform_query('POST', '/unity-catalog/metastores', data=_data,
                                         headers=headers)

    def list_metastores(self, headers=None):
        _data = {}
        return self.client.perform_query('GET', '/unity-catalog/metastores', data=_data,
                                         headers=headers)

    def get_metastore(self, metastore_id, headers=None):
        _data = {}
        return self.client.perform_query('GET', '/unity-catalog/metastores/%s' % (metastore_id),
                                         data=_data, headers=headers)

    def get_metastore_summary(self, headers=None):
        _data = {}
        return self.client.perform_query('GET', '/unity-catalog/metastore_summary', data=_data,
                                         headers=headers)

    def update_metastore(self, metastore_id, metastore_spec, headers=None):
        return self.client.perform_query('PATCH', '/unity-catalog/metastores/%s' % (metastore_id),
                                         data=metastore_spec, headers=headers)

    def delete_metastore(self, metastore_id, force=None, headers=None):
        _data = {}
        if force is not None:
            _data['force'] = force

        return self.client.perform_query('DELETE', '/unity-catalog/metastores/%s' % (metastore_id),
                                         data=_data, headers=headers)

    def create_metastore_assignment(self, workspace_id, metastore_id, default_catalog_name=None,
                                    headers=None):
        _data = {
            'metastore_id': metastore_id
        }
        if default_catalog_name is not None:
            _data['default_catalog_name'] = default_catalog_name
        url = '/unity-catalog/workspaces/%s/metastore' % (workspace_id)
        return self.client.perform_query('PUT', url, data=_data, headers=headers)

    def update_metastore_assignment(self, workspace_id, metastore_id, default_catalog_name,
                                    headers=None):
        _data = {
            'metastore_id': metastore_id,
            'default_catalog_name': default_catalog_name
        }
        url = '/unity-catalog/workspaces/%s/metastore' % (workspace_id)
        return self.client.perform_query('PATCH', url, data=_data, headers=headers)

    def delete_metastore_assignment(self, workspace_id, metastore_id, headers=None):
        _data = {
            'metastore_id': metastore_id
        }
        url = '/unity-catalog/workspaces/%s/metastore' % (workspace_id)
        return self.client.perform_query('DELETE', url, data=_data, headers=headers)

    def get_current_metastore_assignment(self, headers=None):
        _data = {}
        return self.client.perform_query('GET', '/unity-catalog/current-metastore-assignment',
                                         data=_data, headers=headers)

    # External Location Operations

    def create_external_location(self, loc_spec, skip_validation, headers=None):
        # Merge the skip_validation arg, since it's not a query arg and the
        # ExternalLocationInfo spec is 'inline'
        if skip_validation:
            loc_spec['skip_validation'] = skip_validation
        url = '/unity-catalog/external-locations'
        return self.client.perform_query('POST', url, data=loc_spec, headers=headers)

    def list_external_locations(self, headers=None):
        _data = {}
        return self.client.perform_query('GET', '/unity-catalog/external-locations', data=_data,
                                         headers=headers)

    def get_external_location(self, name, headers=None):
        _data = {}
        return self.client.perform_query('GET', '/unity-catalog/external-locations/%s' % (name),
                                         data=_data, headers=headers)

    def update_external_location(self, name, loc_spec, force, skip_validation, headers=None):
        _data = loc_spec
        # Merge the skip_validation arg, since it's not a query arg and the
        # ExternalLocationInfo spec is 'inline'
        if skip_validation:
            _data['skip_validation'] = skip_validation
        # Same for the 'force' field.
        if force:
            _data["force"] = True

        return self.client.perform_query('PATCH', '/unity-catalog/external-locations/%s' % (name),
                                         data=_data, headers=headers)

    def delete_external_location(self, name, force, headers=None):
        _data = {
            "force": force
        }
        return self.client.perform_query('DELETE', '/unity-catalog/external-locations/%s' % (name),
                                         data=_data, headers=headers)

    def validate_external_location(self, validation_spec, headers=None):
        return self.client.perform_query('POST', '/unity-catalog/validate-storage-credentials',
                                         data=validation_spec, headers=headers)

    # Data Access Configuration Operations

    def create_dac(self, metastore_id, dac_spec, skip_validation, headers=None):
        if skip_validation:
            dac_spec['skip_validation'] = skip_validation
        url = '/unity-catalog/metastores/%s/data-access-configurations' % (metastore_id)
        return self.client.perform_query('POST', url, data=dac_spec, headers=headers)

    def list_dacs(self, metastore_id, headers=None):
        _data = {}
        url = '/unity-catalog/metastores/%s/data-access-configurations' % (metastore_id)
        return self.client.perform_query('GET', url, data=_data, headers=headers)

    def get_dac(self, metastore_id, dac_id, headers=None):
        url = '/unity-catalog/metastores/%s/data-access-configurations/%s' % (metastore_id, dac_id)
        return self.client.perform_query('GET', url, headers=headers)

    def delete_dac(self, metastore_id, dac_id, headers=None):
        url = '/unity-catalog/metastores/%s/data-access-configurations/%s' % (metastore_id, dac_id)
        return self.client.perform_query('DELETE', url, headers=headers)

    # Storage Credential Operations

    def create_storage_credential(self, cred_spec, skip_validation, headers=None):
        # Merge the skip_validation arg, since it's not a query arg and the
        # StorageCredentialInfo spec is 'inline'
        if skip_validation:
            cred_spec['skip_validation'] = skip_validation
        url = '/unity-catalog/storage-credentials'
        return self.client.perform_query('POST', url, data=cred_spec, headers=headers)

    def list_storage_credentials(self, name_pattern=None, headers=None):
        _data = {}
        if name_pattern is not None:
            _data['name_pattern'] = name_pattern

        return self.client.perform_query('GET', '/unity-catalog/storage-credentials',
                                         data=_data, headers=headers)

    def get_storage_credential(self, name, headers=None):
        _data = {}

        return self.client.perform_query('GET', '/unity-catalog/storage-credentials/%s' % (name),
                                         data=_data, headers=headers)

    def update_storage_credential(self, name, cred_spec, skip_validation, headers=None):
        # Merge the skip_validation arg, since it's not a query arg and the
        # StorageCredentialInfo spec is 'inline'
        if skip_validation:
            cred_spec['skip_validation'] = skip_validation
        return self.client.perform_query('PATCH', '/unity-catalog/storage-credentials/%s' % (name),
                                         data=cred_spec, headers=headers)

    def delete_storage_credential(self, name, force, headers=None):
        _data = {}
        if force:
            _data["force"] = True

        return self.client.perform_query('DELETE', '/unity-catalog/storage-credentials/%s' % (name),
                                         data=_data, headers=headers)

    # Catalog Operations

    def create_catalog(self, name, comment=None, provider=None, share=None, headers=None):
        _data = {
            'name': name,
        }
        if comment is not None:
            _data['comment'] = comment
        if provider is not None:
            _data['provider_name'] = provider
        if share is not None:
            _data['share_name'] = share
        return self.client.perform_query('POST', '/unity-catalog/catalogs', data=_data,
                                         headers=headers)

    def list_catalogs(self, headers=None):
        _data = {}

        return self.client.perform_query('GET', '/unity-catalog/catalogs', data=_data,
                                         headers=headers)

    def get_catalog(self, name, headers=None):
        _data = {}
        return self.client.perform_query('GET', '/unity-catalog/catalogs/%s' % (name),
                                         data=_data, headers=headers)

    def update_catalog(self, name, catalog_spec, headers=None):
        return self.client.perform_query('PATCH', '/unity-catalog/catalogs/%s' % (name),
                                         data=catalog_spec, headers=headers)

    def delete_catalog(self, name, headers=None):
        _data = {}
        return self.client.perform_query('DELETE', '/unity-catalog/catalogs/%s' % (name),
                                         data=_data, headers=headers)

    def get_catalog_bindings(self, name, headers=None):
        _data = {}
        return self.client.perform_query('GET',
                                         '/unity-catalog/workspace-bindings/catalogs/%s' % (name),
                                         data=_data, headers=headers)

    def update_catalog_bindings(self, name, workspace_bindings_spec, headers=None):
        return self.client.perform_query('PATCH',
                                         '/unity-catalog/workspace-bindings/catalogs/%s' % (name),
                                         data=workspace_bindings_spec, headers=headers)

    # Schema Operations

    def create_schema(self, catalog_name, new_schema_name, comment=None, headers=None):
        _data = {
            'catalog_name': catalog_name,
            'name': new_schema_name,
        }
        if comment is not None:
            _data['comment'] = comment
        return self.client.perform_query('POST', '/unity-catalog/schemas', data=_data,
                                         headers=headers)

    def list_schemas(self, catalog_name=None, name_regex=None, headers=None):
        _data = {}
        if catalog_name is not None:
            _data['catalog_name'] = catalog_name
        if name_regex is not None:
            _data['schema_name_regex'] = name_regex

        return self.client.perform_query('GET', '/unity-catalog/schemas', data=_data,
                                         headers=headers)

    def list_lineages_by_table(self, table_name=None, headers=None):
        """
        List table lineage by table name
        """
        _data = {}
        if table_name is not None:
            _data['table_name'] = table_name

        return self.client.perform_query('GET', '/lineage-tracking/table-lineage/get', data=_data,
                                         headers=headers)

    def list_lineages_by_column(self, table_name=None, column_name=None, headers=None):
        """
        List column lineage by table name and comlumn name
        """
        _data = {}
        if table_name is not None:
            _data['table_name'] = table_name
        if column_name is not None:
            _data['column_name'] = column_name

        return self.client.perform_query('GET', '/lineage-tracking/column-lineage/get', data=_data,
                                         headers=headers)

    def get_schema(self, full_name, headers=None):
        _data = {}
        return self.client.perform_query('GET', '/unity-catalog/schemas/%s' % (full_name),
                                         data=_data, headers=headers)

    def update_schema(self, full_name, schema_spec, headers=None):
        return self.client.perform_query('PATCH', '/unity-catalog/schemas/%s' % (full_name),
                                         data=schema_spec, headers=headers)

    def delete_schema(self, full_name, headers=None):
        _data = {}
        return self.client.perform_query('DELETE', '/unity-catalog/schemas/%s' % (full_name),
                                         data=_data, headers=headers)

    # Table Operations

    def create_table(self, table_spec, headers=None):
        return self.client.perform_query('POST', '/unity-catalog/tables', data=table_spec,
                                         headers=headers)

    def list_tables(self, catalog_name, schema_name=None, name_regex=None, headers=None):
        _data = {
            'catalog_name': catalog_name
        }
        if schema_name is not None:
            _data['schema_name'] = schema_name
        if name_regex is not None:
            _data['table_name_regex'] = name_regex

        return self.client.perform_query('GET', '/unity-catalog/tables', data=_data,
                                         headers=headers)

    def list_table_summaries(self, catalog_name, headers=None):
        _data = {
            'catalog_name': catalog_name
        }
        return self.client.perform_query('GET', '/unity-catalog/table-summaries', data=_data,
                                         headers=headers)

    def get_table(self, full_name, headers=None):
        _data = {}
        return self.client.perform_query('GET', '/unity-catalog/tables/%s' % (full_name),
                                         data=_data, headers=headers)

    def update_table(self, full_name, table_spec, headers=None):
        return self.client.perform_query('PATCH', '/unity-catalog/tables/%s' % (full_name),
                                         data=table_spec, headers=headers)

    def delete_table(self, full_name, headers=None):
        _data = {}
        return self.client.perform_query('DELETE', '/unity-catalog/tables/%s' % (full_name),
                                         data=_data, headers=headers)

    # Share Operations

    def create_share(self, name, headers=None):
        _data = {
            'name': name
        }
        return self.client.perform_query('POST', '/unity-catalog/shares', data=_data,
                                         headers=headers)

    def list_shares(self, headers=None):
        _data = {}
        return self.client.perform_query('GET', '/unity-catalog/shares', data=_data,
                                         headers=headers)

    def get_share(self, name, include_shared_data, headers=None):
        _data = {'include_shared_data': include_shared_data}

        return self.client.perform_query('GET', '/unity-catalog/shares/%s' % (name),
                                         data=_data, headers=headers)

    def update_share(self, name, share_spec, headers=None):
        return self.client.perform_query('PATCH', '/unity-catalog/shares/%s' % (name),
                                         data=share_spec, headers=headers)

    def delete_share(self, name, headers=None):
        _data = {}
        return self.client.perform_query('DELETE', '/unity-catalog/shares/%s' % (name),
                                         data=_data, headers=headers)

    def list_share_permissions(self, name, headers=None):
        _data = {}
        return self.client.perform_query('GET', '/unity-catalog/shares/%s/permissions' % (name),
                                         data=_data, headers=headers)

    def update_share_permissions(self, name, perm_spec, headers=None):
        return self.client.perform_query('PATCH', '/unity-catalog/shares/%s/permissions' % (name),
                                         data=perm_spec, headers=headers)

    # Recipient Operations

    def create_recipient(self, name, comment=None, sharing_id=None,
                         allowed_ip_addresses=None, custom_properties=None, headers=None):
        _data = {
            'name': name,
        }
        if comment is not None:
            _data['comment'] = comment
        if sharing_id is not None:
            _data['data_recipient_global_metastore_id'] = sharing_id
            _data['authentication_type'] = 'DATABRICKS'
        else:
            _data['authentication_type'] = 'TOKEN'
        if allowed_ip_addresses is not None:
            _data['ip_access_list'] = {
                'allowed_ip_addresses': allowed_ip_addresses,
            }
        if custom_properties is not None:
            _data['properties_kvpairs'] = {
                'properties': custom_properties
            }

        return self.client.perform_query('POST', '/unity-catalog/recipients', data=_data,
                                         headers=headers)

    def list_recipients(self, headers=None):
        _data = {}

        return self.client.perform_query('GET', '/unity-catalog/recipients', data=_data,
                                         headers=headers)

    def get_recipient(self, name, headers=None):
        _data = {}

        return self.client.perform_query('GET', '/unity-catalog/recipients/%s' % (name),
                                         data=_data, headers=headers)

    def update_recipient(self, name, recipient_spec, headers=None):
        return self.client.perform_query('PATCH', '/unity-catalog/recipients/%s' % (name),
                                         data=recipient_spec, headers=headers)

    def rotate_recipient_token(self, name, existing_token_expire_in_seconds=None, headers=None):
        _data = {
            'name': name,
        }
        if existing_token_expire_in_seconds is not None:
            _data['existing_token_expire_in_seconds'] = existing_token_expire_in_seconds
        return self.client.perform_query('POST', '/unity-catalog/recipients/%s/rotate-token' %
                                         (name), data=_data, headers=headers)

    def get_recipient_share_permissions(self, name, headers=None):
        _data = {}

        return self.client.perform_query('GET', '/unity-catalog/recipients/%s/share-permissions'
                                         % (name), data=_data, headers=headers)

    def delete_recipient(self, name, headers=None):
        _data = {}

        return self.client.perform_query('DELETE', '/unity-catalog/recipients/%s' % (name),
                                         data=_data, headers=headers)

    # Provider Operations

    def create_provider(self, name, comment, recipient_profile=None, headers=None):
        _data = {
            'name': name,
        }
        if comment is not None:
            _data['comment'] = comment
        if recipient_profile is not None:
            _data['recipient_profile_str'] = mc_pretty_format(recipient_profile)
            _data['authentication_type'] = 'TOKEN'
        else:
            _data['authentication_type'] = 'DATABRICKS'
        return self.client.perform_query('POST', '/unity-catalog/providers/',
                                         data=_data, headers=headers)

    def list_providers(self, headers=None):
        return self.client.perform_query('GET', '/unity-catalog/providers', data={},
                                         headers=headers)

    def get_provider(self, name, headers=None):
        return self.client.perform_query('GET', '/unity-catalog/providers/%s' % (name),
                                         data={}, headers=headers)

    def update_provider(self, name, provider_spec, headers=None):
        return self.client.perform_query('PATCH', '/unity-catalog/providers/%s' % (name),
                                         data=provider_spec, headers=headers)

    def delete_provider(self, name, headers=None):
        return self.client.perform_query('DELETE', '/unity-catalog/providers/%s' % (name),
                                         data={}, headers=headers)

    def list_provider_shares(self, name, headers=None):
        return self.client.perform_query('GET', '/unity-catalog/providers/%s/shares' % (name),
                                         data={}, headers=headers)

    # Permissions Operations

    def _permissions_url(self, sec_type, sec_name, effective=False):
        if effective:
            return '/unity-catalog/effective-permissions/%s/%s' % (sec_type, sec_name)
        else:
            return '/unity-catalog/permissions/%s/%s' % (sec_type, sec_name)

    def get_permissions(self, sec_type, sec_name, headers=None):
        _data = {}
        return self.client.perform_query('GET', self._permissions_url(sec_type, sec_name),
                                         data=_data, headers=headers)

    def get_effective_permissions(self, sec_type, sec_name, headers=None):
        _data = {}
        return self.client.perform_query('GET', self._permissions_url(sec_type, sec_name,
                                                                      effective=True),
                                         data=_data, headers=headers)

    def update_permissions(self, sec_type, sec_name, perm_diff_spec, headers=None):
        _data = perm_diff_spec
        return self.client.perform_query('PATCH', self._permissions_url(sec_type, sec_name),
                                         data=_data, headers=headers)

    def replace_permissions(self, sec_type, sec_name, perm_spec, headers=None):
        _data = perm_spec
        return self.client.perform_query('PUT', self._permissions_url(sec_type, sec_name),
                                         data=_data, headers=headers)
