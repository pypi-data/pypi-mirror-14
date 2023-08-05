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


def create_request(method, get={}, post={}):
    """Creare a Mock HTTP Request."""
    request = Mock(META={}, POST=post, GET=get, method=method)
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

        def put_whatever(self, request):
            """Return 'PUT WHATEVER'."""
            return 'PUT WHATEVER'

        def post(self, request):
            """Return 'POST'."""
            return 'POST'

        def post_whatever(self, request):
            """Return 'POST'."""
            return 'POST'

        def delete_text_plain(self, request):
            """Return 'POST'."""
            return 'POST'

        def get_image_jif(self, request):
            """Return 'IMAGE JIF'."""
            return 'IMAGE JIF'

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

    def test_any_media(self):
        """Test */* media."""
        view = AcceptHeaderTest.TestView()

        request = create_request('PUT')
        request.META['HTTP_ACCEPT'] = '*/*'
        res = view(request)
        self.assertEqual('PUT WHATEVER', res)

        request = create_request('POST')
        request.META['HTTP_ACCEPT'] = '*/*'
        res = view(request)
        self.assertEqual('POST', res)

    def test_no_specific_handler(self):
        """Test 'whatever' media."""
        view = AcceptHeaderTest.TestView(allowed=['DELETE'])

        request = create_request('DELETE')
        request.META['HTTP_ACCEPT'] = 'whatever'
        res = view(request)
        self.assertEqual(406, res.status_code)

    def test_any_subtype(self):
        """Test 'whatever' media."""
        view = AcceptHeaderTest.TestView()

        request = create_request('GET')
        request.META['HTTP_ACCEPT'] = 'image/*'
        res = view(request)
        self.assertEqual('IMAGE JIF', res)


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


class AllowedMethodsTest(TestCase):
    """Test for only allowing specified methods."""

    class TestView(MethodView):
        """Test View."""

        def get(self, request):
            """Return 'GET ALLOWED'."""
            return HttpResponse('GET ALLOWED')

        def post(self, request):
            """Return 'POST ALLOWED'."""
            return HttpResponse('POST ALLOWED')

    def test_allowed(self):
        """Test no authorization."""
        view = AllowedMethodsTest.TestView(allowed=['GET'])

        request = create_request('GET')
        res = view(request)
        self.assertEqual(200, res.status_code)
        self.assertEqual(b'GET ALLOWED', res.content)

    def test_not_allowed(self):
        """Test no authorization."""
        view = AllowedMethodsTest.TestView(allowed=['GET'])

        request = create_request('POST')
        res = view(request)
        self.assertEqual(405, res.status_code)


class MethodRequestTest(TestCase):
    """Test for checking _method support."""

    class TestView(MethodView):
        """Test View."""

        def post(self, request):
            """Return 'POST'."""
            return HttpResponse('POST')

        def put(self, request):
            """Return 'PUT'."""
            return HttpResponse('PUT')

    def test_post_put_method(self):
        """Test a POST saying it's a PUT."""
        view = MethodRequestTest.TestView()

        request = create_request('POST', post={'_method': 'PUT'})
        res = view(request)
        self.assertEqual(200, res.status_code)
        self.assertEqual(b'PUT', res.content)


class MethodNotImplementedTest(TestCase):
    """Test for a not implemented method."""

    class TestView(MethodView):
        """Test View."""

        pass

    def test_no_get(self):
        """Test a GET request."""
        view = MethodNotImplementedTest.TestView()

        request = create_request('GET')
        res = view(request)
        self.assertEqual(501, res.status_code)


class HandlerTest(TestCase):
    """Test for checking _method support."""

    class DebugHandler(object):
        """Test Handler."""

        def __init__(self, *args, **kwargs):
            """Initialize the handler."""
            print("BOO" * 10)
            super(HandlerTest.DebugHandler, self).__init__(*args, **kwargs)
            self.add_handler(self)

        def handle(self, request):
            """Handle the request."""
            request.GET['DEBUG_HANDLER'] = True

    class TestView(MethodView, DebugHandler):
        """Test View."""

        def get(self, request):
            """Return 'GET'."""
            return HttpResponse('GET')

    def test_get(self):
        """Test a GET."""
        view = HandlerTest.TestView()

        request = create_request('GET')
        self.assertFalse('DEBUG_HANDLER' in request.GET)
        res = view(request)
        self.assertEqual(200, res.status_code)
        self.assertEqual(b'GET', res.content)
        self.assertTrue('DEBUG_HANDLER' in request.GET)
