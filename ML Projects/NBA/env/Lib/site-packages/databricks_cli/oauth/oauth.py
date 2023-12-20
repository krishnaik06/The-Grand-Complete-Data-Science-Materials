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


import base64
import hashlib
import json
import os
import webbrowser

from datetime import datetime, timedelta, tzinfo

import click

import jwt
from jwt import PyJWTError

import oauthlib.oauth2
from oauthlib.oauth2.rfc6749.errors import OAuth2Error

import requests
from requests.exceptions import RequestException

from databricks_cli.utils import error_and_quit

try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer


# This could use 'import secrets' in Python 3
def token_urlsafe(nbytes=32):
    tok = os.urandom(nbytes)
    return base64.urlsafe_b64encode(tok).rstrip(b'=').decode('ascii')


# This could be datetime.timezone.utc in Python 3
class UTCTimeZone(tzinfo):
    """UTC"""
    def utcoffset(self, dt):
        #pylint: disable=unused-argument
        return timedelta(0)

    def tzname(self, dt):
        #pylint: disable=unused-argument
        return "UTC"

    def dst(self, dt):
        #pylint: disable=unused-argument
        return timedelta(0)


# Some contant values
OIDC_REDIRECTOR_PATH = "oidc"
CLIENT_ID = "databricks-cli"
REDIRECT_PORT = 8020
UTC = UTCTimeZone()


def get_client(client_id=CLIENT_ID):
    return oauthlib.oauth2.WebApplicationClient(client_id)


def get_redirect_url(port=REDIRECT_PORT):
    return "http://localhost:{port}".format(port=port)


def fetch_well_known_config(idp_url):
    known_config_url = "{idp_url}/.well-known/oauth-authorization-server".format(idp_url=idp_url)
    try:
        response = requests.request(method="GET", url=known_config_url)
    except RequestException:
        error_and_quit("Unable to fetch OAuth configuration from {idp_url}.\n"
                       "Verify it is a valid workspace URL and that OAuth is "
                       "enabled on this account.".format(idp_url=idp_url))

    if response.status_code != 200:
        error_and_quit("Received status {status} OAuth configuration from "
                       "{idp_url}.\n Verify it is a valid workspace URL and "
                       "that OAuth is enabled on this account."
                       .format(status=response.status_code, idp_url=idp_url))
    try:
        return json.loads(response.text)
    except json.decoder.JSONDecodeError:
        error_and_quit("Unable to decode OAuth configuration from {idp_url}.\n"
                       "Verify it is a valid workspace URL and that OAuth is "
                       "enabled on this account.".format(idp_url=idp_url))


def get_idp_url(host):
    maybe_scheme = "https://" if not host.startswith("https://") else ""
    maybe_trailing_slash = "/" if not host.endswith("/") else ""
    return "{scheme}{host}{trailing}{path}".format(
        scheme=maybe_scheme, host=host, trailing=maybe_trailing_slash, path=OIDC_REDIRECTOR_PATH)


def get_challenge(verifier_string=token_urlsafe(32)):
    digest = hashlib.sha256(verifier_string.encode('UTF-8')).digest()
    challenge_string = base64.urlsafe_b64encode(digest).decode("UTF-8").replace('=', '')
    return verifier_string, challenge_string


# This is a janky global that is used to store the path of the single request the HTTP server
# will receive.
global_request_path = None


def set_request_path(path):
    global global_request_path
    global_request_path = path


class SingleRequestHandler(BaseHTTPRequestHandler):
    RESPONSE_BODY = """<html>
<head>
  <title>Close this Tab</title>
  <style>
    body {
      font-family: "Barlow", Helvetica, Arial, sans-serif;
      padding: 20px;
      background-color: #f3f3f3;
    }
  </style>
</head>
<body>
  <h1>Please close this tab.</h1>
  <p>
    The Databricks CLI received a response. You may close this tab.
  </p>
</body>
</html>""".encode("utf-8")

    def do_GET(self):  # nopep8
        self.send_response(200, "Success")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.RESPONSE_BODY)
        set_request_path(self.path)

    def log_message(self, format, *args):
        #pylint: disable=redefined-builtin
        #pylint: disable=unused-argument
        return


def get_authorization_code(client, auth_url, redirect_url, scope, state, challenge, port):
    #pylint: disable=unused-variable
    (auth_req_uri, headers, body) = client.prepare_authorization_request(
        authorization_url=auth_url,
        redirect_url=redirect_url,
        scope=scope,
        state=state,
        code_challenge=challenge,
        code_challenge_method="S256")
    click.echo("Opening {uri}".format(uri=auth_req_uri))

    with HTTPServer(("", port), SingleRequestHandler) as httpd:
        webbrowser.open_new(auth_req_uri)
        click.echo("Listening for OAuth authorization callback at {uri}"
                   .format(uri=redirect_url))
        httpd.handle_request()

    if not global_request_path:
        error_and_quit("No path parameters were returned to the callback at {uri}"
                       .format(uri=redirect_url))
    # This is a kludge because the parsing library expects https callbacks
    # We should probably set it up using https
    full_redirect_url = "https://localhost:{port}/{path}".format(
        port=port, path=global_request_path)
    try:
        authorization_code_response = \
            client.parse_request_uri_response(full_redirect_url, state=state)
    except OAuth2Error as err:
        error_and_quit("OAuth Token Request error {error}".format(error=err.description))
    return authorization_code_response


def send_auth_code_token_request(client, token_request_url, redirect_url, code, verifier):
    token_request_body = client.prepare_request_body(code=code, redirect_uri=redirect_url)
    data = "{body}&code_verifier={verifier}".format(body=token_request_body, verifier=verifier)
    return send_token_request(token_request_url, data)


def send_token_request(token_request_url, data):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.request(method="POST", url=token_request_url, data=data, headers=headers)
    oauth_response = json.loads(response.text)
    return oauth_response


def send_refresh_token_request(hostname, refresh_token):
    idp_url = get_idp_url(hostname)
    oauth_config = fetch_well_known_config(idp_url)
    token_request_url = oauth_config['token_endpoint']
    client = get_client()
    token_request_body = client.prepare_refresh_body(
        refresh_token=refresh_token, client_id=client.client_id)
    return send_token_request(token_request_url, token_request_body)


def get_tokens_from_response(oauth_response):
    access_token = oauth_response['access_token']
    refresh_token = oauth_response['refresh_token'] if 'refresh_token' in oauth_response else None
    return access_token, refresh_token


def check_and_refresh_access_token(hostname, access_token, refresh_token):
    now = datetime.now(tz=UTC)
    # If we can't decode an expiration time, this will be expired by default.
    expiration_time = now
    try:
        # This token has already been verified and we are just parsing it.
        # If it has been tampered with, it will be rejected on the server side.
        # This avoids having to fetch the public key from the issuer and perform
        # an unnecessary signature verification.
        decoded = jwt.decode(access_token, options={"verify_signature": False})
        expiration_time = datetime.fromtimestamp(decoded['exp'], tz=UTC)
    except PyJWTError as err:
        error_and_quit(err)

    if expiration_time > now:
        # The access token is fine. Just return it.
        return access_token, refresh_token, False

    if not refresh_token:
        error_and_quit("OAuth access token expired on {expiration_time}."
                       .format(expiration_time=expiration_time))

    # Try to refresh using the refresh token
    click.echo("Attempting to refresh OAuth access token that expired on {expiration_time}"
               .format(expiration_time=expiration_time))
    oauth_response = send_refresh_token_request(hostname, refresh_token)
    fresh_access_token, fresh_refresh_token = get_tokens_from_response(oauth_response)
    return fresh_access_token, fresh_refresh_token, True


def get_tokens(hostname, scope=None):
    idp_url = get_idp_url(hostname)
    oauth_config = fetch_well_known_config(idp_url)
    # We are going to override oauth_config["authorization_endpoint"] use the
    # /oidc redirector on the hostname, which may inject additional parameters.
    auth_url = "{}/v1/authorize".format(get_idp_url(hostname))
    state = token_urlsafe(16)
    (verifier, challenge) = get_challenge()
    client = get_client()
    redirect_url = get_redirect_url()
    try:
        auth_response = get_authorization_code(
            client,
            auth_url,
            redirect_url,
            scope,
            state,
            challenge,
            REDIRECT_PORT)
    except OAuth2Error as err:
        error_and_quit("OAuth Authorization Error: {error}".format(error=err.description))

    token_request_url = oauth_config["token_endpoint"]
    code = auth_response['code']
    oauth_response = \
        send_auth_code_token_request(client, token_request_url, redirect_url, code, verifier)
    return get_tokens_from_response(oauth_response)
