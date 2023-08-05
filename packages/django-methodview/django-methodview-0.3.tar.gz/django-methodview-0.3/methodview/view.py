"""Django Method View."""
# -*- coding: utf-8 -*-
#
# Copyright 2012 keyes.ie
#
# License: http://jkeyes.mit-license.org/
#

import inspect

from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from .accept_header import AcceptHeader

ALLOWED_METHODS = ('GET', 'HEAD', 'POST', 'PUT')


def hasmethod(obj, method_name):
    """Check if `obj` has a callable attribute `method_name`."""
    if hasattr(obj, method_name):
        attr = getattr(obj, method_name)
        return inspect.ismethod(attr) or inspect.isfunction(attr)
    return False


class AuthorizationError(Exception):
    """An error raised when authorization fails."""

    def __init__(self, code, message, content_type):
        """Initialize the error."""
        self.code = code
        self.message = message
        self.content_type = content_type


class HttpResponseNotImplemented(HttpResponse):
    """HttpResponse 501."""

    status_code = 501

    def __init__(self, *args, **kwargs):  # noqa
        HttpResponse.__init__(self, *args, **kwargs)


class HttpResponseNotAcceptable(HttpResponse):
    """HttpResponse 406."""

    status_code = 406

    def __init__(self, *args, **kwargs):  # noqa
        HttpResponse.__init__(self, *args, **kwargs)


class MethodView(object):
    """The MethodView class."""

    def __init__(self, allowed=None):
        """Initialize the view.

        * allowed - what methods are allowed
        """
        if allowed is None:
            allowed = ALLOWED_METHODS
        self._allowed_methods = [a.upper() for a in allowed]
        self._method_supported = False
        self._handlers = []
        super(MethodView, self).__init__()

    def add_handler(self, request):
        """Add a handler."""
        self._handlers.append(request)

    def _get_handler(self, http_method, accept):
        self._methods = inspect.getmembers(self, inspect.ismethod)
        self._method_names = [method[0] for method in self._methods]
        for mname in self._method_names:
            if mname.lower().startswith(http_method):
                self._method_supported = True
        handler_name = None
        for media_range in accept:
            if media_range.any_media:
                # check for default first
                if http_method in self._method_names:
                    handler_name = http_method
                    break  # don't check anything else in the accept header
                # check for prefixed
                method_prefix = "%s_" % (http_method)
                for name in self._method_names:
                    if name.startswith(method_prefix):
                        handler_name = name
                        break
                # if handler_name is None and http_method in self._method_names:
                #     handler_name = http_method
            elif media_range.any_subtype:
                method_prefix = "%s_%s_" % (http_method, media_range.mtype)
                for name in self._method_names:
                    if name.startswith(method_prefix):
                        handler_name = name
                        break
            else:
                handler_name = "%s_%s_%s" % (
                    http_method, media_range.mtype, media_range.subtype)
            if handler_name and hasmethod(self, handler_name):
                return getattr(self, handler_name)
        if hasmethod(self, http_method):
            return getattr(self, http_method)
        return None

    def _authorize(self, request, accept):
        """Return an HTTP 401 if the request cannot be authorized."""
        if not hasmethod(self, 'authorize'):
            # nothing to authorize, move along
            return

        self.authorize(request)

    def _get_accept(self, request):
        if 'HTTP_ACCEPT' not in request.META:
            # From: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
            #     "If no Accept header field is present, then it is assumed
            #      that the client accepts all media types."
            accept = AcceptHeader("*/*")
        else:
            accept = AcceptHeader(request.META['HTTP_ACCEPT'])
        return accept

    def __call__(self, request, *args, **kwargs):
        """Method dispatcher."""
        method_name = request.method

        accept = self._get_accept(request)

        # call any handlers
        for h in self._handlers:
            resp = h.handle(request, *args, **kwargs)
            if resp:
                return resp

        # authorize the call if possible
        try:
            self._authorize(request, accept)
        except (AuthorizationError) as auth_error:
            # not authorized, send an error response
            return HttpResponse(
                auth_error.message, content_type=auth_error.content_type,
                status=auth_error.code)

        # check in POST then GET for _method.
        if '_method' in request.POST:
            method_name = request.POST['_method']
        elif '_method' in request.GET:
            method_name = request.GET['_method']

        method_name = method_name.upper()
        if method_name in self._allowed_methods:
            handler_name = method_name.lower()
            handler = self._get_handler(handler_name, accept)
            if handler is None:
                # if the method is handled for the Resource but
                # an allowed MIME type handler is not found the
                # return a NotAcceptable
                # TODO: determine the response content
                if self._method_supported:
                    return HttpResponseNotAcceptable()
                return HttpResponseNotImplemented()
            return handler(request, *args, **kwargs)
        return HttpResponseNotAllowed(self._allowed_methods)
