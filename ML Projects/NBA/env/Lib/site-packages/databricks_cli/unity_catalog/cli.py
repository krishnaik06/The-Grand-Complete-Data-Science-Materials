# Databricks CLI
# Copyright 2021 Databricks, Inc.
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

import click

from databricks_cli.utils import CONTEXT_SETTINGS
from databricks_cli.version import print_version_callback, version

from databricks_cli.unity_catalog.metastore_cli import register_metastore_commands
from databricks_cli.unity_catalog.catalog_cli import register_catalog_commands
from databricks_cli.unity_catalog.schema_cli import register_schema_commands
from databricks_cli.unity_catalog.table_cli import register_table_commands
from databricks_cli.unity_catalog.ext_loc_cli import register_ext_loc_commands
from databricks_cli.unity_catalog.cred_cli import register_cred_commands
from databricks_cli.unity_catalog.delta_sharing_cli import register_delta_sharing_commands
from databricks_cli.unity_catalog.perms_cli import register_perms_commands
from databricks_cli.unity_catalog.lineage_cli import register_lineage_commands


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--version', '-v', is_flag=True, callback=print_version_callback,
              expose_value=False, is_eager=True, help=version)
def unity_catalog_group():  # pragma: no cover
    """
    Utility to interact with Databricks Unity Catalog.
    """
    pass


register_metastore_commands(unity_catalog_group)
register_ext_loc_commands(unity_catalog_group)
register_cred_commands(unity_catalog_group)
register_catalog_commands(unity_catalog_group)
register_schema_commands(unity_catalog_group)
register_table_commands(unity_catalog_group)
register_delta_sharing_commands(unity_catalog_group)
register_perms_commands(unity_catalog_group)
register_lineage_commands(unity_catalog_group)
