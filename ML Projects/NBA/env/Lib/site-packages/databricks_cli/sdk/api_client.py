#!/usr/bin/env python

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
A common class to be used by client of different APIs
"""

import base64
import json
import warnings
import requests
import ssl
import copy
import pprint

from . import version

from requests.adapters import HTTPAdapter
from requests.utils import get_netrc_auth
from requests.auth import HTTPBasicAuth
from six.moves.urllib.parse import urlparse

try:
    from requests.packages.urllib3.poolmanager import PoolManager
    from requests.packages.urllib3 import exceptions
    from requests.packages.urllib3.util.retry import Retry
except ImportError:
    from urllib3.poolmanager import PoolManager
    from urllib3 import exceptions
    from urllib3.util.retry import Retry

from databricks_cli.sdk.version import UC_API_VERSION
from databricks_cli.version import version as databricks_cli_version

class TlsV1HttpAdapter(HTTPAdapter):
    """
    A HTTP adapter implementation that specifies the ssl version to be TLS1.
    This avoids problems with openssl versions that
    use SSL3 as a default (which is not supported by the server side).
    """

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_version=ssl.PROTOCOL_TLSv1_2)

# https://github.com/psf/requests/issues/2773#issuecomment-174312831
class FallbackNetrcAuth(requests.auth.AuthBase):
    '''Force requests to ignore the ``.netrc`` if other authentication 
    methods have been setup. Fallback to ``.netrc`` if not. 

    Use with::

        requests.get(url, auth=FallbackNetrcAuth())
        
        s = requests.Session()
        s.auth = FallbackNetrcAuth()
    '''

    def __call__(self, r):
        if "Authorization" in r.headers:
            return r
        
        netrc_tuple = get_netrc_auth(r.url)

        if netrc_tuple is None or not any(netrc_tuple):
            return r
        
        return HTTPBasicAuth(*netrc_tuple)(r)

class ApiClient(object):
    """
    A partial Python implementation of dbc rest api
    to be used by different versions of the client.
    """
    def __init__(self, user=None, password=None, host=None, token=None,
                 api_version=version.API_VERSION, default_headers={}, verify=True, command_name="", jobs_api_version=None):
        if host[-1] == "/":
            host = host[:-1]

        retries = Retry(
            total=6,
            backoff_factor=1,
            status_forcelist=[429],
            allowed_methods=set({'POST'}) | set(Retry.DEFAULT_ALLOWED_METHODS),
            respect_retry_after_header=True,
            raise_on_status=False # return original response when retries have been exhausted
        )
        self.session = requests.Session()
        self.session.auth = FallbackNetrcAuth()
        self.session.mount('https://', TlsV1HttpAdapter(max_retries=retries))

        parsed_url = urlparse(host)
        scheme = parsed_url.scheme
        hostname = parsed_url.hostname
        self.url = "%s://%s/api/" % (scheme, hostname)
        if user is not None and password is not None:
            encoded_auth = (user + ":" + password).encode()
            user_header_data = "Basic " + base64.standard_b64encode(encoded_auth).decode()
            auth = {'Authorization': user_header_data, 'Content-Type': 'text/json'}
        elif token is not None:
            auth = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'text/json'}
        else:
            auth = {}
        user_agent = {'user-agent': 'databricks-cli-{v}-{c}'.format(v=databricks_cli_version,
                                                                    c=command_name)}
        self.default_headers = {}
        self.default_headers.update(auth)
        self.default_headers.update(default_headers)
        self.default_headers.update(user_agent)
        self.verify = verify
        self.api_version = api_version
        self.jobs_api_version = jobs_api_version

    def close(self):
        """Close the client"""
        pass

    # helper functions starting here

    def perform_query(self, method, path, data = {}, headers = None, files=None, version=None):
        """set up connection and perform query"""
        if headers is None:
            headers = self.default_headers
        else:
            tmp_headers = copy.deepcopy(self.default_headers)
            tmp_headers.update(headers)
            headers = tmp_headers

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", exceptions.InsecureRequestWarning)
            if method == 'GET':
                translated_data = {k: _translate_boolean_to_query_param(data[k]) for k in data}
                resp = self.session.request(method, self.get_url(path, version=version), params = translated_data,
                                            verify = self.verify, headers = headers)
            else:
                if files is None:
                    resp = self.session.request(method, self.get_url(path, version=version), data = json.dumps(data),
                                                verify = self.verify, headers = headers)
                else:
                    # Multipart file upload
                    resp = self.session.request(method, self.get_url(path, version=version), files = files, data = data,
                                                verify = self.verify, headers = headers)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            message = e.args[0]
            try:
                reason = pprint.pformat(json.loads(resp.text), indent=2)
                message += '\n Response from server: \n {}'.format(reason)
            except ValueError:
                pass
            raise requests.exceptions.HTTPError(message, response=e.response)
        return resp.json()


    def get_url(self, path, version=None):
        if version:
            return self.url + version + path
        elif self.jobs_api_version and path and path.startswith('/jobs'):
            return self.url + self.jobs_api_version + path
        elif path and _is_uc_path(path):
            return self.url + UC_API_VERSION + path
        return self.url + self.api_version + path


def _is_uc_path(path):
    return path.startswith('/unity-catalog')


def _translate_boolean_to_query_param(value):
    assert not isinstance(value, list), 'GET parameters cannot pass list of objects'
    if isinstance(value, bool):
        if value:
            return 'true'
        else:
            return 'false'
    return value
