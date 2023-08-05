"""Tests for MethodView."""
#
# Copyright 2012 keyes.ie
#
# License: http://jkeyes.mit-license.org/
#

import os

from django.http import HttpResponse
from methodview import AuthorizationError
from methodview import MethodView
from mock import Mock
from unittest import TestCase

os.environ['DJANGO_SETTINGS_MODULE'] = 'unit.test_view'
SECRET_KEY = 'xxx'


def create_request(method, get={}):
    """Creare a Mock HTTP Request."""
    request = Mock(META={}, POST={}, GET=get, method=method)
    return request


class BasicMethodTest(TestCase):
    """Test for method/verb support."""

    class TestView(MethodView):
        """A Test view."""

        def get(self, request):
            """Return GOT."""
            return 'GOT'

        def post(self, request):
            """Return POSTED."""
            return 'POSTED'

    def test(self):
        """Test GET and POST."""
        view = BasicMethodTest.TestView()

        request = create_request('GET')
        res = view(request)
        self.assertEqual('GOT', res)

        request = create_request('POST')
        res = view(request)
        self.assertEqual('POSTED', res)


class AcceptHeaderTest(TestCase):
    """Test for honouring `Accept` header."""

    class TestView(MethodView):
        """Test View."""

        def get(self, request):
            """Return 'GOT DEFAULT'."""
            return 'GOT DEFAULT'

        def get_text_html(self, request):
            """Return 'GOT TEXT HTML'."""
            return 'GOT TEXT HTML'

        def get_application_json(self, request):
            """Return 'GOT APPLICATION JSON'."""
            return 'GOT APPLICATION JSON'

    def test(self):
        """Test `Accept` header."""
        view = AcceptHeaderTest.TestView()

        request = create_request('GET')
        res = view(request)
        self.assertEqual('GOT DEFAULT', res)

        request.META['HTTP_ACCEPT'] = 'text/html'
        res = view(request)
        self.assertEqual('GOT TEXT HTML', res)

        request.META['HTTP_ACCEPT'] = 'application/json'
        res = view(request)
        self.assertEqual('GOT APPLICATION JSON', res)


class AuthorizeTest(TestCase):
    """Test for honouring `Accept` header."""

    class TestView(MethodView):
        """Test View."""

        def authorize(self, request):
            """Authorize the request."""
            if 'auth' not in request.GET:
                raise AuthorizationError(401, 'No Auth', 'text/plain')

        def get(self, request):
            """Return 'AUTHORIZED'."""
            return HttpResponse('AUTHORIZED')

    def test_no_auth(self):
        """Test no authorization."""
        view = AuthorizeTest.TestView()

        request = create_request('GET')
        res = view(request)
        self.assertEqual(401, res.status_code)
        self.assertEqual(b'No Auth', res.content)

    def test_auth(self):
        """Test no authorization."""
        view = AuthorizeTest.TestView()

        request = create_request('GET', {'auth': 'yes'})
        res = view(request)
        self.assertEqual(200, res.status_code)
        self.assertEqual(b'AUTHORIZED', res.content)
