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

import math
import random
import sys
import traceback
from json import dumps as json_dumps, loads as json_loads

import click
import six
from requests.exceptions import HTTPError

from databricks_cli.click_types import ContextObject

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
CLUSTER_OPTIONS = ['cluster-id', 'cluster-name']
DEBUG_MODE = False


def eat_exceptions(function):
    @six.wraps(function)
    def decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except HTTPError as exception:
            if exception.response.status_code == 401:
                error_and_quit('Your authentication information may be incorrect. Please '
                               'reconfigure with ``dbfs configure``')
            elif exception.response.status_code == 403:
                error_and_quit('Authorization failed. Your token may be expired or '
                               'lack the valid scope')
            else:
                error_and_quit(exception.response.content)
        except Exception as exception:  # noqa
            if not DEBUG_MODE:
                error_and_quit('{}: {}'.format(type(exception).__name__, str(exception)))

    decorator.__doc__ = function.__doc__
    return decorator


def pipelines_exception_eater(function):
    """
    Formats error messages from the pipelines API while keeping the existing
    behavior of eat_exception
    """

    @six.wraps(function)
    def decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except HTTPError as exception:  # noqa
            if exception.response.status_code == 401:
                error_and_quit('Your authentication information may be incorrect. Please '
                               + 'reconfigure with ``dbfs configure``')
            else:
                try:
                    exp_context = json_loads(exception.response.content.decode('utf-8'))
                    message = exception.response.content
                    if 'error_code' in exp_context and 'message' in exp_context:
                        message = exp_context['error_code'] + '\n' + exp_context['message']
                    error_and_quit(message)
                except Exception:  # noqa
                    error_and_quit(exception.response.content)
        except Exception as exception:  # noqa
            if not DEBUG_MODE:
                error_and_quit('{}: {}'.format(type(exception).__name__, str(exception)))

    decorator.__doc__ = function.__doc__
    return decorator


def error_and_quit(message):
    ctx = click.get_current_context()
    context_object = ctx.ensure_object(ContextObject)
    if context_object.debug_mode:
        traceback.print_exc()
    click.echo(u'Error: {}'.format(message))
    sys.exit(1)


INTERVAL_MAX = 30
INTERVAL_BASE = 5
MAX_EXPONENT = 10


def backoff_with_jitter(attempt):
    """
    Creates a growing but randomized wait time based on the number of attempts already made.
    """
    exponent = min(attempt, MAX_EXPONENT)
    sleep_time = min(INTERVAL_MAX, INTERVAL_BASE * 2 ** exponent)
    return random.randrange(math.floor(sleep_time * 0.5), sleep_time)


def pretty_format(json, encode_utf8=False):
    if encode_utf8:
        return json_dumps(json, indent=2, ensure_ascii=False)
    return json_dumps(json, indent=2)


def json_cli_base(json_file, json, api, error_msg='', print_response=True, encode_utf8=False):
    """
    Takes json_file or json string and calls an function "api" with the json
    deserialized
    """
    if not (json_file is None) ^ (json is None):
        if not error_msg:
            error_msg = 'Either --json-file or --json should be provided'
        raise RuntimeError(error_msg)
    if json_file:
        with open(json_file, 'r') as f:
            json = f.read()
    res = api(json_loads(json))
    if print_response:
        click.echo(pretty_format(res, encode_utf8))


def truncate_string(s, length=100):
    if len(s) <= length:
        return s
    return s[:length] + '...'


def to_graph(dict_obj, graph_name="Graph"):
    entries = ["\"{}\" -> {};".format(key, ','.join(
        '"{}"'.format(item) for item in dict_obj.get(key))) for key in dict_obj]
    return "digraph \"{}\" ".format(graph_name) + "{\n\t" + "\n\t".join(entries) + "\n}"


class InvalidConfigurationError(RuntimeError):
    @staticmethod
    def for_profile(profile):
        if profile is None:
            return InvalidConfigurationError(
                'You haven\'t configured the CLI yet! '
                'Please configure by entering `{} configure`'.format(sys.argv[0]))
        return InvalidConfigurationError(
            ('You haven\'t configured the CLI yet for the profile {profile}! '
             'Please configure by entering '
             '`{argv} configure --profile {profile}`').format(
                profile=profile, argv=sys.argv[0]))


def merge_dicts_shallow(*dicts):
    """
    Merges dicts through shallow copy.
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result
    
