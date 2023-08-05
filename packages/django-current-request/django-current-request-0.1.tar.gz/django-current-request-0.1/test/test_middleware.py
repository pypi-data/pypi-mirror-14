from django.conf import settings
from django.test import TestCase, RequestFactory
from django.test.client import Client

import json

from djangocurrentrequest.middleware import get_current_request

class MiddlewareTest(TestCase):
    def test_middleware_prepend(self):
        with self.modify_settings(MIDDLEWARE_CLASSES={
            'prepend': 'djangocurrentrequest.middleware.RequestMiddleware',
            }):
            response = self.client.get('/')
            data = json.loads(response.content.decode("utf-8"))
            self.assertEqual(data['path'], '/')

    def test_middleware_append(self):
        with self.modify_settings(MIDDLEWARE_CLASSES={
            'append': 'djangocurrentrequest.middleware.RequestMiddleware',
            }):
            response = self.client.get('/')
            data = json.loads(response.content.decode("utf-8"))
            self.assertEqual(data['path'], '/')

