from django.test import TestCase


class InstapageApiClientTestCase(TestCase):

    def setUp(self):
        self.api = InstapageApiClient("api.example.com", "wp.test.com")
