# -*- coding: utf-8 -*-

"""
Servicenow REST API client
The REST API is active by default in all instances, starting with the Eureka release.
"""

__author__ = "Robert Wikman <rbw@vault13.org>"

import requests
import json
from requests.auth import HTTPBasicAuth


class UnexpectedResponse(Exception):
    pass


class InvalidUsage(Exception):
    pass


class Client(object):
    base = "api/now"

    def __init__(self, instance, user, password, raise_on_empty=True):
        ## Connection properties
        self.instance = instance
        self.fqdn = "%s.service-now.com" % instance
        self._user = user
        self._password = password
        self._session = self._create_session()
        self._raise_on_empty = raise_on_empty

        ## Request properties
        self.table = None

        ## Return properties
        self.return_code = None

    def _create_session(self):
        """
        Creates and returns a new session object with the user/pw combination passed to the constructor
        :return: session object
        """
        s = requests.Session()
        s.auth = HTTPBasicAuth(self._user, self._password)
        s.headers.update({'content-type': 'application/json', 'accept': 'application/json'})
        return s

    @property
    def url(self):
        ## Some tables uses a different base path
        if self.table == 'attachment':
            base = self.base
        else:
            base = "%s/%s" % (self.base, "table")

        url_str = 'https://%(fqdn)s/%(base)s/%(table)s' % (
            {
                'fqdn': self.fqdn,
                'base': base,
                'table': self.table
            }
        )

        return url_str

    def _handle_response(self, request, method):
        """
        Checks for errors in the server response. Returns serialized server response on success.
        :param request: request object
        :param method: HTTP method
        :return: ServiceNow response dict
        """
        if method == 'DELETE':
            if request.status_code != 204:
                raise UnexpectedResponse("Unexpected HTTP response code. Expected: 204, got %d" % request.status_code)
            else:
                return True

        result = request.json()

        if request.status_code == 404 and self._raise_on_empty is False:
            result['result'] = []
        elif 'error' in result:
            raise UnexpectedResponse("ServiceNow responded (%i): %s" % (request.status_code,
                                                                        result['error']['message']))

        self.return_code = request.status_code
        return result['result']

    def _format_query(self, query, fields):
        """
        The dict-to-string conversion used here was inspired by: https://github.com/locaweb/python-servicenow
        :param query: query of type dict or string
        :param fields: Comma-separated field names to return in the response
        :return: servicenow query string
        """

        if isinstance(query, dict):  # Dict-type query
            try:
                items = query.iteritems()  # Python 2
            except AttributeError:
                items = query.items()  # Python 3

            query_str = '^'.join(['%s=%s' % (field, value) for field, value in items])
        elif isinstance(query, str):  # String-type query
            query_str = query
        else:
            raise InvalidUsage("You must pass a query using either a dictionary or string (for advanced queries)")

        result = {'sysparm_query': query_str}
        if fields is not None:
            if isinstance(fields, list):
                result.update({'sysparm_fields': ",".join(fields)})
            else:
                raise InvalidUsage("You must pass the fields as a list")

        return result

    def _request(self, method, query, fields, payload=None, sysid=None):
        """
        Request wrapper. Makes sure table property is set and performs the appropriate method call.
        :param method: http verb str
        :param query: query dict
        :param payload: query payload for inserts
        :param sysid: the sysid to operate on
        :param fields: Comma-separated field names to return in the response
        :return: server response
        """
        if not self.table:
            raise InvalidUsage("You must specify a table to query ServiceNow")

        if sysid:
            url = "%s/%s" % (self.url, sysid)
        else:
            url = self.url

        if method == 'GET':
            request = self._session.get(
                url,
                params=self._format_query(query, fields)
            )
        elif method == 'POST':
            request = self._session.post(
                url,
                data=json.dumps(payload)
            )
        elif method == 'PUT':
            request = self._session.put(
                url,
                data=json.dumps(payload)
            )
        elif method == 'DELETE':
            request = self._session.delete(
                url,
                data=json.dumps(payload)
            )

        return self._handle_response(request, method)

    def get(self, query, fields=None):
        return self._request('GET', query, fields)

    def update(self, payload, sysid):
        return self._request('PUT', None, None, payload, sysid)

    def insert(self, payload):
        return self._request('POST', None, None, payload)

    def delete(self, sysid):
        return self._request('DELETE', None, None, None, sysid)

