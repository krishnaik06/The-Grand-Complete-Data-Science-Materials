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

import uuid
import click
import six

from databricks_cli.click_types import ContextObject
from databricks_cli.configure.provider import get_config, \
    update_and_persist_config, ProfileConfigProvider
from databricks_cli.oauth.oauth import check_and_refresh_access_token
from databricks_cli.utils import InvalidConfigurationError
from databricks_cli.sdk import ApiClient
from databricks_cli.sdk.version import API_VERSIONS


def provide_api_client(function):
    """
    Injects the api_client keyword argument to the wrapped function.
    All callbacks wrapped by provide_api_client expect the argument ``profile`` to be passed in.
    """
    @six.wraps(function)
    def decorator(*args, **kwargs):
        ctx = click.get_current_context()
        command_name = "-".join(ctx.command_path.split(" ")[1:])
        command_name += "-" + str(uuid.uuid1())
        profile = get_profile_from_context()
        if profile:
            # If we request a specific profile, only get credentials from there.
            config = ProfileConfigProvider(profile).get_config()
        else:
            # If unspecified, use the default provider, or allow for user overrides.
            config = get_config()
        if not config or not config.is_valid:
            raise InvalidConfigurationError.for_profile(profile)

        # This checks if an OAuth access token has expired and will attempt to refresh it if
        # a refresh token is present
        if config.host and config.token and config.refresh_token:
            config.token, config.refresh_token, updated = \
                check_and_refresh_access_token(config.host, config.token, config.refresh_token)
            if updated:
                update_and_persist_config(profile, config)

        kwargs['api_client'] = _get_api_client(config, command_name)

        return function(*args, **kwargs)
    decorator.__doc__ = function.__doc__
    return decorator


def get_profile_from_context():
    ctx = click.get_current_context()
    context_object = ctx.ensure_object(ContextObject)
    return context_object.get_profile()


def debug_option(f):
    def callback(ctx, param, value):  # NOQA
        context_object = ctx.ensure_object(ContextObject)
        context_object.set_debug(value)
    return click.option('--debug', is_flag=True, callback=callback,
                        expose_value=False, help="Debug Mode. Shows full stack trace on error.")(f)


def profile_option(f):
    def callback(ctx, param, value):  # NOQA
        if value is not None:
            context_object = ctx.ensure_object(ContextObject)
            context_object.set_profile(value)
    return click.option('--profile', required=False, default=None, callback=callback,
                        expose_value=False,
                        help='CLI connection profile to use. The default profile is "DEFAULT".')(f)


def api_version_option(f):
    return click.option('--version', required=False, default=None, type=click.Choice(API_VERSIONS),
                        help='Override the API version used to call databricks.')(f)


def _get_api_client(config, command_name=""):
    verify = config.insecure is None
    if config.is_valid_with_token:
        return ApiClient(host=config.host, token=config.token, verify=verify,
                         command_name=command_name, jobs_api_version=config.jobs_api_version)
    return ApiClient(user=config.username, password=config.password,
                     host=config.host, verify=verify, command_name=command_name,
                     jobs_api_version=config.jobs_api_version)
