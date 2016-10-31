from django.test import TestCase
from webapp.client import *
from sure import expect
import httpretty


class InstapageApiClientTestCase(TestCase):

    def setUp(self):
        self.api = InstapageApiClient("instapage.com", "http://127.0.0.1:8000/")

    def test_successful_login(self):
        """
        Successful login
        :return None:
        """
        print("START: test_successful_login")

        httpretty.enable()
        httpretty.register_uri(httpretty.POST, "http://instapage.com/ajax/services/user-login",
                               body=json.dumps({"message": "Ok",
                                                "data": {"user_id": 976617,
                                                         "plugin_hash": "75f9179460cdb14751d68390f876b3e"},
                                                "success": True,
                                                "error": False}),
                               content_type='text/json')

        user_id, plugin_h = self.api.login("login", "password")

        expect(user_id).to.equal(976617)
        expect(plugin_h).to.equal('75f9179460cdb14751d68390f876b3e')

        httpretty.disable()

        print("PASS: test_successful_login")

    def test_incorrect_password(self):
        """
        Invalid password
        :return None:
        """
        print("START: test_incorrect_password")

        httpretty.enable()
        httpretty.register_uri(httpretty.POST, "http://instapage.com/ajax/services/user-login",
                               body=json.dumps({u'error_message': u'Login failed',
                                                u'success': False,
                                                u'error': True}),
                               content_type='text/json')

        try:
            response = self.api.login("login", "password")
        except InstapageApiException as e:
            expect(e.message()).to.equal('Authentication failure: Login failed')

        httpretty.disable()

        print("PASS: test_incorrect_password")

    def test_get_user_pages(self):
        """
        Simple API call
        :return None:
        """
        print("START: test_get_user_pages")

        httpretty.enable()
        httpretty.register_uri(httpretty.POST, "http://instapage.com/ajax/services/my-pages",
                                   body=json.dumps({'message': u'Ok',
                                                    'data': {'pages': ['page1', 'page2', 'page3']},
                                                    'success': True,
                                                    'error': False}),
                                   content_type='text/json')

        response = self.api.get_user_pages(998475, "75f9179460cdb14751d68390f876b3e")
        expect(response).to.equal(['page1', 'page2', 'page3'])

        httpretty.disable()

        print("PASS: test_get_user_pages")

    def test_internal_server_error(self):
        """
        Internal Server Error
        :return:
        """
        print("START: test_internal_server_error")

        httpretty.enable()
        httpretty.register_uri(httpretty.POST, "http://instapage.com/ajax/services/my-pages",
                               status=500)
        try:
            response = self.api.api_call("my-pages")
        except InstapageApiException as e:
            expect(e.m_message).to.equal("Connection failure: Internal Server Error")

        httpretty.disable()

        print("PASS: test_internal_server_error")

    def test_not_found_page(self):
        """
        Page Not Found!
        :return:
        """
        print("START: test_not_found_page")

        httpretty.enable()
        httpretty.register_uri(httpretty.POST, "http://instapage.com/ajax/services/my-pages",
                               status=404)
        try:
            response = self.api.api_call("my-pages")
        except InstapageApiException as e:
            expect(e.m_message).to.equal("Connection failure: Not Found")

        httpretty.disable()

        print("PASS: test_not_found_page")

    def test_request_page_content(self):
        """
        Request page content
        :return None:
        """
        print("START: test_request_page_content")

        httpretty.enable()
        httpretty.register_uri(httpretty.POST, "http://instapage.com/server/view-by-id/330178",
                               body='<p>Page</p>')

        response = self.api.get_page(330178)
        expect(response).to.equal("<p>Page</p>")

        httpretty.disable()

        print("PASS: test_request_page_content")

    def test_get_page_by_id(self):
        """
        Page by ID
        :return None:
        """
        print("START: test_get_page_by_id")

        httpretty.enable()
        httpretty.register_uri(httpretty.POST, "http://instapage.com/server/view-by-id/330178")

        response = self.api.request_page("http://instapage.com/server/view-by-id/330178")
        expect(response.status).to.equal(200)

        httpretty.disable()

        print("PASS: test_get_page_by_id")

