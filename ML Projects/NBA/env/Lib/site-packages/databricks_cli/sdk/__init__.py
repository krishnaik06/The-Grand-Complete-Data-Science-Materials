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

"""
Databricks Python REST Client 2.0 for interacting with various services.

Currently supports services including clusters, clusters policies and jobs.

Requires Python 3.7 or above.

To get started, below is an example usage of the Python API client.

  # Import databricks package:
  from databricks import *

  # Create a client:
  userName = "user@company.com"
  password = "MySecretPassword"
  client = ApiClient(userName, password, host = "https://dbc-12345678-9101.cloud.databricks.com")

  # List jobs:
  jobs = JobsService(client)
  print jobs.list_jobs()

  # For help:
  help(databricks)

  # To examine available services:
  help(databricks.service)

  # To examine the jobs API:
  help(JobsService)
"""
from .service import *
from .api_client import ApiClient
