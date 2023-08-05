# -*- coding: utf-8 -*-
from __future__ import absolute_import
from future.standard_library import install_aliases
from past.builtins import basestring, unicode
install_aliases()

import datetime
import json
import os
import requests
import warnings
from urllib.parse import quote

from tzlocal import get_localzone

from kyper.util.api import errors, credential_management
from . import _config
from ._version import __version__

def _parse_response(response, version):
    '''
        Parses response into Python dict and checks for exceptions
    '''
    js = response.json()

    if js.get('status') == "ok":
        if js.get('version').split(".")[0] == version.split(".")[0]: # match major version
            if js.get('deprecated'):
                warnings.warn(
                    "Version {} is deprecated and will be removed soon. \
                    Please upgrade your kyper.data library to the latest version.".format(js.get('version')),
                    PendingDeprecationWarning
                )
            return js
        else: 
            raise errors.VersionMismatchException(version, js.get('version'))
    elif js.get('status') == "error":
        raise errors.make_exception_from_code_and_message(js.get('code'),
                                                          js.get('message'))
    else:
        raise errors.MalformedResponseException(js)


def _friendlify_type(param):
    if isinstance(param, datetime.datetime): # datetime
        if param.tzinfo is None:
            local_tz = get_localzone()
            return quote(local_tz.localize(param).isoformat())
        else:
            return quote(param.isoformat())
    elif isinstance(param, datetime.date): # date
        return quote(param.isoformat())
    elif isinstance(param, basestring): # string
        return quote(unicode(param))
    elif hasattr(param, '__iter__'): # iterable
        return ','.join(map(_friendlify_type, param))
    else:
        return quote(json.dumps(param))


def get_data(service, version, method, **kwargs):
    '''
        Makes a data service API call, validates the response, and returns the contents of the 'data' field 
    '''
    API_ENDPOINT = _config.API_ENDPOINT

    keys_to_keep = []
    for k, v in kwargs.items():
        if v is not None:
            keys_to_keep.append(k)

    # make types friendly for API passing and remove Nones
    params = {}
    for k in keys_to_keep:
        params[str(quote(k))] = _friendlify_type(kwargs[k])

    def make_request(email, auth_token):
        params.update({"email": email})

        paramstring = "&".join(["{}={}".format(k, v) for k, v in sorted(params.items(), key=lambda t: t[0])])
        urlstring = "{}/{}/{}/{}".format(API_ENDPOINT, service, version, method) + ("?" + paramstring if paramstring else "")
        return _parse_response(
                    requests.get(
                        urlstring, headers={
                            'Authorization': 'Token {}'.format(auth_token),
                            'User-Agent': "Kyper Python Library {}".format(__version__)
                        }
                    ), version
                ).get('data')

    try:
        AUTH_TOKEN = credential_management.get_auth_token()
        EMAIL = credential_management.get_username()
        return make_request(EMAIL, AUTH_TOKEN)
    except (errors.InvalidCredentialsException, credential_management.AuthDBDoesNotExist):
        try:
            credential_management.refresh_credentials()
            AUTH_TOKEN = credential_management.get_auth_token()
            EMAIL = credential_management.get_username()
        except (errors.InvalidCredentialsException, credential_management.AuthDBDoesNotExist, credential_management.InvalidRefreshToken):
            credential_management.get_new_credentials()
            AUTH_TOKEN = credential_management.get_auth_token()
            EMAIL = credential_management.get_username()
        
        return make_request(EMAIL, AUTH_TOKEN)
