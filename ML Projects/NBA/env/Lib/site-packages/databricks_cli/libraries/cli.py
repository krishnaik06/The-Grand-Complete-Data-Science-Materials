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

import click

from databricks_cli.click_types import ClusterIdClickType, OneOfOption, OptionalOneOfOption
from databricks_cli.clusters.api import ClusterApi
from databricks_cli.configure.config import provide_api_client, profile_option, debug_option
from databricks_cli.libraries.api import LibrariesApi
from databricks_cli.utils import CONTEXT_SETTINGS, eat_exceptions, pretty_format, CLUSTER_OPTIONS
from databricks_cli.version import print_version_callback, version


def _all_cluster_statuses(api_client):
    click.echo(pretty_format(LibrariesApi(api_client).all_cluster_statuses()))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get the status of all libraries.')
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def all_cluster_statuses_cli(api_client):
    """
    Get the status of all libraries on all clusters. A status will be available for all libraries
    installed on this cluster via the API or the libraries UI as well as libraries set to be
    installed on all clusters via the libraries UI. If a library has been set to be installed on
    all clusters, is_library_for_all_clusters will be true.
    """
    _all_cluster_statuses(api_client)


def _cluster_status(api_client, cluster_id, cluster_name):
    libraries_api = LibrariesApi(api_client)

    if not cluster_id:
        cluster_id = ClusterApi(api_client).get_cluster_id_for_name(cluster_name)

    click.echo(pretty_format(libraries_api.cluster_status(cluster_id)))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Get the status of all libraries for a specified cluster.')
@click.option('--cluster-id', cls=OneOfOption, one_of=CLUSTER_OPTIONS,
              type=ClusterIdClickType(), default=None, help=ClusterIdClickType.help)
@click.option('--cluster-name', cls=OneOfOption, one_of=CLUSTER_OPTIONS,
              type=ClusterIdClickType(), default=None, help=ClusterIdClickType.help)
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def cluster_status_cli(api_client, cluster_id, cluster_name):
    """
    Get the status of all libraries for a specified cluster. A status will be available for all
    libraries installed on this cluster via the API or the libraries UI as well as libraries set to
    be installed on all clusters via the libraries UI. If a library has been set to be installed on
    all clusters, is_library_for_all_clusters will be true.
    """
    _cluster_status(api_client, cluster_id, cluster_name)


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Shortcut to `all-cluster-statuses` or `cluster-status`.')
@click.option('--cluster-id', cls=OptionalOneOfOption, one_of=CLUSTER_OPTIONS,
              type=ClusterIdClickType(), default=None, help=ClusterIdClickType.help)
@click.option('--cluster-name', cls=OptionalOneOfOption, one_of=CLUSTER_OPTIONS,
              type=ClusterIdClickType(), default=None, help=ClusterIdClickType.help)
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def list_cli(api_client, cluster_id, cluster_name):
    """
    Get the statuses of all libraries for all clusters or for a specified cluster.
    If the option --cluster-id is provided, then all libraries on that cluster will be listed,
    (cluster-status). If the option --cluster-id is omitted, then all libraries on all clusters
    will be listed (all-cluster-statuses).
    """
    if cluster_id is not None or cluster_name is not None:
        _cluster_status(api_client, cluster_id, cluster_name)
    else:
        _all_cluster_statuses(api_client)


INSTALL_OPTIONS = ['jar', 'egg', 'whl', 'maven-coordinates', 'pypi-package', 'cran-package']
UNINSTALL_OPTIONS = ['all'] + INSTALL_OPTIONS
JAR_HELP = 'JAR on DBFS or S3 or WASB.'
EGG_HELP = 'Egg on DBFS or S3 or WASB.'
WHEEL_HELP = """
Wheel or zipped wheelhouse on DBFS or S3 or WASB. Only recommended for clusters running
Databricks Runtime 4.2 or higher.
"""
MAVEN_COORDINATES_HELP = """
Maven coordinates in the form of GroupId:ArtifactId:Version (i.e. org.jsoup:jsoup:1.7.2).
"""
MAVEN_REPO_HELP = """
Maven repository to install the Maven package from. If omitted, both Maven 
Repository and Spark Packages are searched.
"""
MAVEN_EXCLUSION_HELP = """
List of dependences to exclude. For example: --maven-exclusion "slf4j:slf4j" 
--maven-exclusion "*:hadoop-client".
"""
PYPI_PACKAGE_HELP = """
The name of the PyPI package to install. An optional exact version
specification is also supported. Examples: "simplejson" and "simplejson==3.8.0".
"""
PYPI_REPO_HELP = """
The repository where the package can be found. If not specified, the default pip index is used.
"""
CRAN_PACKAGE_HELP = """
The name of the CRAN package to install.
"""
CRAN_REPO_HELP = """
The repository where the package can be found. If not specified, the default CRAN repo is used.
"""


def _get_library_from_options(jar, egg, whl, maven_coordinates, maven_repo, maven_exclusion,  # noqa
                              pypi_package, pypi_repo, cran_package, cran_repo):
    maven_exclusion = list(maven_exclusion)
    if jar is not None:
        return {'jar': jar}
    elif egg is not None:
        return {'egg': egg}
    elif whl is not None:
        return {'whl': whl}
    elif maven_coordinates is not None:
        maven_library = {'maven': {'coordinates': maven_coordinates}}
        if maven_repo is not None:
            maven_library['maven']['repo'] = maven_repo
        if len(maven_exclusion) > 0:
            maven_library['maven']['exclusions'] = maven_exclusion
        return maven_library
    elif pypi_package is not None:
        pypi_library = {'pypi': {'package': pypi_package}}
        if pypi_repo is not None:
            pypi_library['pypi']['repo'] = pypi_repo
        return pypi_library
    elif cran_package is not None:
        cran_library = {'cran': {'package': cran_package}}
        if cran_repo is not None:
            cran_library['cran']['repo'] = cran_repo
        return cran_library
    raise AssertionError('Code not reached.')  # pragma: no cover


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Install a library on a cluster.')
@click.option('--cluster-id', required=True, type=ClusterIdClickType(),
              help=ClusterIdClickType.help)
@click.option('--jar', cls=OneOfOption, one_of=INSTALL_OPTIONS, help=JAR_HELP)
@click.option('--egg', cls=OneOfOption, one_of=INSTALL_OPTIONS, help=EGG_HELP)
@click.option('--whl', cls=OneOfOption, one_of=INSTALL_OPTIONS, help=WHEEL_HELP)
@click.option('--maven-coordinates', cls=OneOfOption, one_of=INSTALL_OPTIONS,
              help=MAVEN_COORDINATES_HELP)
@click.option('--maven-repo', help=MAVEN_REPO_HELP)
@click.option('--maven-exclusion', multiple=True, help=MAVEN_EXCLUSION_HELP)
@click.option('--pypi-package', cls=OneOfOption, one_of=INSTALL_OPTIONS, help=PYPI_PACKAGE_HELP)
@click.option('--pypi-repo', help=PYPI_REPO_HELP)
@click.option('--cran-package', cls=OneOfOption, one_of=INSTALL_OPTIONS, help=CRAN_PACKAGE_HELP)
@click.option('--cran-repo', help=CRAN_REPO_HELP)
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def install_cli(api_client, cluster_id, jar, egg, whl, maven_coordinates, maven_repo,  # noqa
                maven_exclusion, pypi_package, pypi_repo, cran_package, cran_repo):
    """
    Install a library on a cluster. Libraries must be first uploaded to dbfs or s3
    (see `dbfs cp -h`). Unlike the API, only one library can be installed for each execution of
    `databricks libraries install`.

    Users should only provide one of
    [--jar, --egg, --whl, --maven-coordinates, --pypi-package, --cran-package].

    Installing a whl library on clusters running Databricks Runtime 4.2 or higher effectively runs
    the pip command against the wheel file directly on driver and executors.The library must satisfy
    the wheel file name convention.
    To install multiple wheel files, use the .wheelhouse.zip file that includes all the wheel files
    with the --whl option.

    Installing a wheel library on clusters running Databricks Runtime lower than 4.2 just adds the
    file to the PYTHONPATH variable, without installing the dependencies.
    More information is available here:
    https://docs.databricks.com/api/latest/libraries.html#managedlibrariesmanagedlibraryserviceinstalllibraries
    """
    library = _get_library_from_options(jar, egg, whl, maven_coordinates, maven_repo,
                                        maven_exclusion, pypi_package, pypi_repo, cran_package,
                                        cran_repo)
    LibrariesApi(api_client).install_libraries(cluster_id, [library])


def _uninstall_cli_exit_help(cluster_id):
    click.echo(click.style('WARNING: Uninstalling libraries requires a cluster restart.', fg='red'))
    click.echo('databricks clusters restart --cluster-id {}'.format(cluster_id))


@click.command(context_settings=CONTEXT_SETTINGS,
               short_help='Uninstall a library on a cluster.')
@click.option('--cluster-id', required=True, type=ClusterIdClickType(),
              help=ClusterIdClickType.help)
@click.option('--all', is_flag=True, cls=OneOfOption, one_of=UNINSTALL_OPTIONS, default=False,
              help='If set, uninstall all libraries.')
@click.option('--jar', cls=OneOfOption, one_of=UNINSTALL_OPTIONS, help=JAR_HELP)
@click.option('--egg', cls=OneOfOption, one_of=UNINSTALL_OPTIONS, help=EGG_HELP)
@click.option('--whl', cls=OneOfOption, one_of=UNINSTALL_OPTIONS, help=WHEEL_HELP)
@click.option('--maven-coordinates', cls=OneOfOption, one_of=UNINSTALL_OPTIONS,
              help=MAVEN_COORDINATES_HELP)
@click.option('--maven-repo', help=MAVEN_REPO_HELP)
@click.option('--maven-exclusion', multiple=True, help=MAVEN_EXCLUSION_HELP)
@click.option('--pypi-package', cls=OneOfOption, one_of=UNINSTALL_OPTIONS,
              help=PYPI_PACKAGE_HELP)
@click.option('--pypi-repo', help=PYPI_REPO_HELP)
@click.option('--cran-package', cls=OneOfOption, one_of=UNINSTALL_OPTIONS, help=CRAN_PACKAGE_HELP)
@click.option('--cran-repo', help=CRAN_REPO_HELP)
@debug_option
@profile_option
@eat_exceptions  # noqa
@provide_api_client
def uninstall_cli(api_client, cluster_id, all, jar, egg, whl, maven_coordinates, maven_repo,  # noqa
                  maven_exclusion, pypi_package, pypi_repo, cran_package, cran_repo):
    """
    Mark libraries on a cluster to be uninstalled. Libraries which are marked to be uninstalled
    will stay attached until the cluster is restarted. (see `databricks clusters restart -h`).
    """
    if all:
        libraries_api = LibrariesApi(api_client)
        library_statuses = libraries_api.cluster_status(cluster_id).get('library_statuses', [])
        libraries = [l_status['library'] for l_status in library_statuses]
        if len(libraries) == 0:
            return
        libraries_api.uninstall_libraries(cluster_id, libraries)
        _uninstall_cli_exit_help(cluster_id)
        return
    library = _get_library_from_options(jar, egg, whl, maven_coordinates, maven_repo,
                                        maven_exclusion, pypi_package, pypi_repo, cran_package,
                                        cran_repo)
    LibrariesApi(api_client).uninstall_libraries(cluster_id, [library])
    _uninstall_cli_exit_help(cluster_id)


@click.group(context_settings=CONTEXT_SETTINGS,
             short_help='Utility to interact with libraries.')
@click.option('--version', '-v', is_flag=True, callback=print_version_callback,
              expose_value=False, is_eager=True, help=version)
@debug_option
@profile_option
@eat_exceptions
def libraries_group():  # pragma: no cover
    """
    Utility to interact with libraries.

    This is a wrapper around the libraries API
    (https://docs.databricks.com/api/latest/libraries.html).
    """
    pass


libraries_group.add_command(list_cli, name='list')
libraries_group.add_command(all_cluster_statuses_cli, name='all-cluster-statuses')
libraries_group.add_command(cluster_status_cli, name='cluster-status')
libraries_group.add_command(install_cli, name='install')
libraries_group.add_command(uninstall_cli, name='uninstall')
