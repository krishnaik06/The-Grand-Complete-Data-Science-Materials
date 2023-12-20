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

from json import loads as json_loads

import click
from tabulate import tabulate

from databricks_cli.click_types import OutputClickType, JsonClickType, JobIdClickType
from databricks_cli.jobs.api import JobsApi
from databricks_cli.utils import eat_exceptions, CONTEXT_SETTINGS, pretty_format, json_cli_base, \
    truncate_string

from databricks_cli.configure.config import provide_api_client, profile_option, \
    get_profile_from_context, debug_option, get_config, api_version_option
from databricks_cli.configure.provider import DatabricksConfig, update_and_persist_config, \
    ProfileConfigProvider
from databricks_cli.version import print_version_callback, version as cli_version


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--json-file', default=None, type=click.Path(),
              help='File containing JSON request to POST to /api/2.*/jobs/create.')
@click.option('--json', default=None, type=JsonClickType(),
              help=JsonClickType.help('/api/2.*/jobs/create'))
@api_version_option
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def create_cli(api_client, json_file, json, version):
    """
    Creates a job.

    The specification for the json option can be found
    https://docs.databricks.com/api/latest/jobs.html#create
    """
    check_version(api_client, version)
    json_cli_base(json_file, json,
                  lambda json: JobsApi(api_client).create_job(json, version=version))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--job-id', default=None, type=JobIdClickType(), help=JobIdClickType.help)
@click.option('--json-file', default=None, type=click.Path(),
              help='File containing partial JSON request to POST to /api/2.*/jobs/reset. '
                   'For more, read full help message.')
@click.option('--json', default=None, type=JsonClickType(),
              help='Partial JSON string to POST to /api/2.*/jobs/reset. '
                   'For more, read full help message.')
@api_version_option
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def reset_cli(api_client, json_file, json, job_id, version):
    """
    Resets (edits) the definition of a job.

    The specification for the json option can be found
    https://docs.databricks.com/api/latest/jobs.html#jobsjobsettings
    """
    check_version(api_client, version)
    if not bool(json_file) ^ bool(json):
        raise RuntimeError('Either --json-file or --json should be provided')
    if json_file:
        with open(json_file, 'r') as f:
            json = f.read()
    deser_json = json_loads(json)
    # If the payload is defined using the API definition rather than the CLI
    # extract the settings data.
    new_settings = deser_json['new_settings'] if (
        'new_settings' in deser_json) else deser_json

    # If job id is not defined in the call we fall back to checking
    # the JSON for a job_id property
    if job_id is None:
        if 'job_id' in deser_json:
            job_id = deser_json['job_id']
        else:
            raise RuntimeError(
                'Either --job-id or a root-level json key "job_id" should be provided')

    request_body = {
        'job_id': job_id,
        'new_settings': new_settings
    }

    JobsApi(api_client).reset_job(request_body, version=version)


def _jobs_to_table(jobs_json):
    ret = []
    for j in jobs_json['jobs']:
        ret.append((j['job_id'], truncate_string(j['settings']['name'])))
    return sorted(ret, key=lambda t: t[1].lower())


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Lists the jobs in the Databricks Job Service.')
@click.option('--output', default=None, help=OutputClickType.help, type=OutputClickType())
@click.option('--type', 'job_type', default=None, help='The type of job to list', type=str)
@click.option('--expand-tasks', is_flag=True,
              help='Expands the tasks array (only available in API 2.1).')
@click.option('--offset', default=None, type=int,
              help='The offset to use when listing jobs (only available in API 2.1).')
@click.option('--limit', default=None, type=int,
              help='The maximum number of jobs to fetch in a single call ' +
                   '(only available in API 2.1).')
@click.option('--all', '_all', is_flag=True,
              help='Lists all jobs by executing sequential calls to the API ' +
                   '(only available in API 2.1).')
@click.option('--name', 'name', default=None, type=str,
              help='If provided, only returns jobs that match the supplied ' + 
                   'name (only available in API 2.1).')
@api_version_option
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def list_cli(api_client, output, job_type, version, expand_tasks, offset, limit, _all, name):
    """
    Lists the jobs in the Databricks Job Service.

    By default the output format will be a human readable table with the following fields

      - Job ID

      - Job name

    A JSON formatted output can also be requested by setting the --output parameter to "JSON"

    In table mode, the jobs are sorted by their name.
    """
    check_version(api_client, version)
    api_version = version or api_client.jobs_api_version
    using_features_only_in_21 = expand_tasks or offset or limit or _all or name
    if api_version != '2.1' and using_features_only_in_21:
        click.echo(click.style('ERROR', fg='red') + ': the options --expand-tasks, ' +
                   '--offset, --limit, --all, and --name are only available in API 2.1', err=True)
        return
    jobs_api = JobsApi(api_client)
    has_more = True
    jobs = []
    if _all:
        offset = 0
        limit = 20
    while has_more:
        jobs_json = jobs_api.list_jobs(job_type=job_type, expand_tasks=expand_tasks,
                                       offset=offset, limit=limit, version=version,
                                       name=name)
        jobs += jobs_json['jobs'] if 'jobs' in jobs_json else []
        has_more = jobs_json.get('has_more', False) and _all
        if has_more:
            offset = offset + \
                (len(jobs_json['jobs']) if 'jobs' in jobs_json else 20)

    out = {'jobs': jobs}
    if OutputClickType.is_json(output):
        click.echo(pretty_format(out))
    else:
        click.echo(tabulate(_jobs_to_table(out),
                   tablefmt='plain', disable_numparse=True))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Deletes the specified job.')
@click.option('--job-id', required=True, type=JobIdClickType(), help=JobIdClickType.help)
@api_version_option
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def delete_cli(api_client, job_id, version):
    """
    Deletes the specified job.
    """
    check_version(api_client, version)
    JobsApi(api_client).delete_job(job_id, version=version)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--job-id', required=True, type=JobIdClickType(), help=JobIdClickType.help)
@api_version_option
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def get_cli(api_client, job_id, version):
    """
    Describes the metadata for a job.
    """
    check_version(api_client, version)
    click.echo(pretty_format(
        JobsApi(api_client).get_job(job_id, version=version)))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--job-id', required=True, type=JobIdClickType(), help=JobIdClickType.help)
@click.option('--jar-params', default=None, type=JsonClickType(),
              help='JSON string specifying an array of parameters. i.e. ["param1", "param2"]')
@click.option('--notebook-params', default=None, type=JsonClickType(),
              help='JSON string specifying a map of key-value pairs. '
                   'i.e. {"name": "john doe", "age": 35}')
@click.option('--python-params', default=None, type=JsonClickType(),
              help='JSON string specifying an array of parameters. i.e. ["param1", "param2"]')
@click.option('--python-named-params', default=None, type=JsonClickType(),
              help='JSON string specifying a map of key-value pairs. '
                   'i.e. {"name": "john doe", "age": 35}')
@click.option('--spark-submit-params', default=None, type=JsonClickType(),
              help='JSON string specifying an array of parameters. i.e. '
                   '["--class", "org.apache.spark.examples.SparkPi"]')
@click.option('--idempotency-token', default=None,
              help='If an active run with the provided token already exists, ' +
              'the request does not create a new run, ' +
              'but returns the ID of the existing run instead.')
@api_version_option
@debug_option
@profile_option
@eat_exceptions
@provide_api_client
def run_now_cli(api_client, job_id, jar_params, notebook_params, python_params,
                python_named_params, spark_submit_params, idempotency_token, version):
    """
    Runs a job with optional per-run parameters.

    Parameter options are specified in json and the format is documented in
    https://docs.databricks.com/api/latest/jobs.html#jobsrunnow.
    """
    check_version(api_client, version)
    jar_params_json = json_loads(jar_params) if jar_params else None
    notebook_params_json = json_loads(
        notebook_params) if notebook_params else None
    python_params = json_loads(python_params) if python_params else None
    python_named_params = json_loads(
        python_named_params) if python_named_params else None
    spark_submit_params = json_loads(
        spark_submit_params) if spark_submit_params else None
    res = JobsApi(api_client).run_now(
        job_id, jar_params_json, notebook_params_json, python_params,
        spark_submit_params, python_named_params, idempotency_token, version=version)
    click.echo(pretty_format(res))


@click.command(context_settings=CONTEXT_SETTINGS)
@api_version_option
@debug_option
@profile_option
def configure(version):
    profile = get_profile_from_context()
    config = ProfileConfigProvider(
        profile).get_config() if profile else get_config()
    new_config = config or DatabricksConfig.empty()
    new_config.jobs_api_version = version
    update_and_persist_config(profile, new_config)


@click.group(context_settings=CONTEXT_SETTINGS,
             short_help='Utility to interact with jobs.')
@click.option('--version', '-v', is_flag=True, callback=print_version_callback,
              expose_value=False, is_eager=True, help=cli_version)
@debug_option
@profile_option
@eat_exceptions
def jobs_group():  # pragma: no cover
    """
    Utility to interact with jobs.

    This is a wrapper around the jobs API (https://docs.databricks.com/api/latest/jobs.html).
    Job runs are handled by ``databricks runs``.
    """
    pass


jobs_group.add_command(create_cli, name='create')
jobs_group.add_command(list_cli, name='list')
jobs_group.add_command(delete_cli, name='delete')
jobs_group.add_command(get_cli, name='get')
jobs_group.add_command(reset_cli, name='reset')
jobs_group.add_command(run_now_cli, name='run-now')
jobs_group.add_command(configure, name='configure')


def check_version(api_client, version):
    if version is not None:
        # If the user explicitly passed --version=2.x for this invocation it means
        # they really really want that version, let's not show any warnings
        return

    if api_client.jobs_api_version == '2.1':
        # If the user is globally configured to use 2.1 we don't show the warning
        return

    click.echo(click.style('WARN', fg='yellow') + ': Your CLI is configured ' +
               'to use Jobs API 2.0. In order to use the latest Jobs features ' +
               'please upgrade to 2.1: \'databricks jobs configure --version=2.1\'. ' +
               'Future versions of this CLI will default to the new Jobs API. ' +
               'Learn more at https://docs.databricks.com/dev-tools/cli/jobs-cli.html',
               err=True
               )
