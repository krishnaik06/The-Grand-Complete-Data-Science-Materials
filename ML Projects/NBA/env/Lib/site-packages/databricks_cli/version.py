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

import re


version = '0.18.0' #  NOQA


def print_version_callback(ctx, param, value): #  NOQA
    import click
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version {}'.format(version))
    ctx.exit()


def _match_version(value):
    # Expect version to be of the form: `X.Y.Z(.suffix)?`
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)(\.\w+)?$', value)
    if match is None:
        raise ValueError("Non-compliant version string: " + value)
    return match


def is_release_version(value=None):
    """
    Returns whether the current version of databricks-cli is a release version or not.
    """
    if value is None:
        value = version

    # The 4th group is the optional `.devZZZ` suffix.
    # If it is non-empty, this is not a release version.
    match = _match_version(value)
    if match.group(4) is not None:
        return False

    return True


def next_development_version(value=None):
    """
    Returns the hypothetical next development version of databricks-cli.
    """
    if value is None:
        value = version

    match = _match_version(value)
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))
    return "{}.{}.{}.dev0".format(major, minor, patch + 1)
