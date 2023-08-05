"""
ElasticBox Confidential
Copyright (c) 2014 All Right Reserved, ElasticBox Inc.

NOTICE:  All information contained herein is, and remains the property
of ElasticBox. The intellectual and technical concepts contained herein are
proprietary and may be covered by U.S. and Foreign Patents, patents in process,
and are protected by trade secret or copyright law. Dissemination of this
information or reproduction of this material is strictly forbidden unless prior
written permission is obtained from ElasticBox
"""


from __future__ import absolute_import

import urlparse
import requests

ELASTICBOX_TOKEN_HEADER = 'ElasticBox-Token'
ELASTICBOX_RELEASE_HEADER = 'ElasticBox-Release'
ELASTICBOX_RELEASE = '4.0'

requests.packages.urllib3.disable_warnings()


class AuthenticatedSession(object):

    def __init__(self, args):
        parsed_url = urlparse.urlparse(args.url)
        if not parsed_url.scheme:
            self._url = 'https://{0}'.format(parsed_url.geturl())
        else:
            self._url = parsed_url.geturl()

        self._session = requests.Session()
        self._session.headers.update({ELASTICBOX_TOKEN_HEADER: args.token})
        self._session.headers.update({ELASTICBOX_RELEASE_HEADER: ELASTICBOX_RELEASE})

    def get(self, url_path, *args):
        return self._session.get(self._url + url_path.format(*args), verify=False)

    def delete(self, url_path, *args):
        return self._session.delete(self._url + url_path.format(*args), verify=False)

    def put(self, url_path, *args, **kwargs):
        return self._session.put(self._url + url_path.format(*args), verify=False, **kwargs)

    def post(self, url_path, *args, **kwargs):
        return self._session.post(self._url + url_path.format(*args), verify=False, **kwargs)
