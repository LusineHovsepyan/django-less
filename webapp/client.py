# Python packages
import httplib
import urllib
import base64
import json


class InstapageApiException(Exception):
    """ Exception for failures during communication with Instapage private API
    """
    def __init__(self, message):
        self.m_message = message

    def message(self):
        return self.m_message


class InstapageApiClient(object):
    """ Client for Instapage private APIs. Client acts as a Wordpress plugin.
    """

    def __init__(self, instapage_host, app_host):
        """ Class constructor. Sets configurable host for Instapage API.

        :param instapage_host: string hostname (domain) for Instapage API
        :param app_host: string hostname (domain) for Django App
        """
        self.host = instapage_host
        self.service = app_host

    def login(self, email, password):
        """ Logs into Instapage private API as a Wordpress plugin

        :param email: string user email
        :param password: string plaintext password
        :return: tuple user ID and hash generated for plugin
        """
        data = self.api_call('user-login',
                             user_id='',
                             email=base64.b64encode(email),
                             password=base64.b64encode(password)
                             )
        return data['data']['user_id'], data['data']['plugin_hash']

    def get_user_pages(self, user_id, plugin_hash):
        """ Gets the list of pages crated by user on the Instapage side

        :param user_id: int unique ID if the user retrieved when logged in
        :param plugin_hash: string hash generated for a plugin communication
        :return: list of dictionaries. Each page as a dict
        """
        data = self.api_call('my-pages',
                             user_id=user_id,
                             plugin_hash=plugin_hash
                             )
        return data['data']['pages']

    def get_page(self, page_id):
        """ Retrieves the HTML content for a page identified by its ID

        :param page_id: int unique ID for the page retrieved along with user pages
        :return: string HTML source of the page
        """
        response = self.request_page("/server/view-by-id/{}".format(page_id))
        return response.read()

    def request_page(self, url, **kwargs):
        """ Requests a public page from the Instapage API

        :param url: string request URL
        :param kwargs: dict of query params to be sent
        :return: httplib HTTPResponse instance
        """
        conn = httplib.HTTPConnection(self.host)
        headers = self.get_base_headers()
        conn.request("POST", url, urllib.urlencode(kwargs), headers)
        return conn.getresponse()

    def api_call(self, service, **kwargs):
        """ Calls a specific service within Instapage private API

        :param service: string service name
        :param kwargs: dict of query params to be sent
        :return: httplib HTTPResponse instance
        """
        conn = httplib.HTTPConnection(self.host)
        headers = self.get_base_headers()
        params = self.get_base_params()
        for param, value in kwargs.iteritems():
            key = "data[{}]".format(param)
            params[key] = value
        url = "/ajax/services/" + service
        conn.request("POST", url, urllib.urlencode(params), headers)
        return self.deserialize_response(conn.getresponse())

    def deserialize_response(self, response):
        """ Deserializes JSON encoded response and hanldles faulty responses

        :param response: httplib.HTTPResponse instance
        :return: dict deserialized data
        """
        if 200 != response.status:
            message = 'Connection failure: {}'.format(response.reason)
            raise InstapageApiException(message)
        data = json.loads(response.read())
        if data['error']:
            message = 'Authentication failure: {}'.format(
                data['error_message'])
            raise InstapageApiException(message)
        elif not data['success']:
            message = 'API call failure: {}'.format(data['message'])
            raise InstapageApiException(message)
        return data

    def get_base_headers(self):
        """ Get the basic set of headers to be sent with all requests
        """
        return {
            'Accept-Encoding': 'deflate;q=1.0, compress;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    def get_base_params(self):
        """ Get the basic set of params to be sent with API calls
        """
        return {
            'service-type': 'Wordpress',
            'service': self.service,
            'version': '2.21',
        }