"""
===============================================================================
Module: Error Handler
===============================================================================

Author:
    Arundas Mohandas
    
Functionality:
    Provides a fallback error page if rendering fails.
    Displays a user-friendly error message when the request is malformed.
    Displays a message when the user lacks permission to access a resource.
    Returns a friendly error page for missing resources.
    Provides a user-friendly fallback when server errors occur.

===============================================================================
"""

import logging
from django.conf import settings
from django.http import HttpResponseServerError
from django.shortcuts import render

logger = logging.getLogger(__name__)


def _safe_error_render(request, template_name, context=None, *, status=500):

    context = context or {}
    try:
        return render(request, template_name, context, status=status)
    except Exception:
        logger.exception("Failed to render error template: %s", template_name)
        if template_name != "login/errors_500.html":
            try:
                return render(
                    request,
                    "login/errors_500.html",
                    {
                        "message": "Something went wrong."
                        if not settings.DEBUG
                        else "See server logs for details."
                    },
                    status=500,
                )
            except Exception:
                pass
        # Final minimal fallback
        return HttpResponseServerError("<h1>Server Error</h1>")


def custom_bad_request_view(request, exception):
    # 400 Bad Request
    return _safe_error_render(
        request,
        "login/errors_400.html",
        {"message": "Your request could not be processed."},
        status=400,
    )


def custom_permission_denied_view(request, exception):
    # 403 Forbidden
    return _safe_error_render(
        request,
        "login/errors_403.html",
        {"message": "You do not have permission to view this page."},
        status=403,
    )


def custom_page_not_found_view(request, exception):
    return _safe_error_render(
        request,
        "login/errors_404.html",
        {"message": "The page you requested could not be found."},
        status=404,
    )


def custom_server_error_view(request):
    # 500 Internal Server Error
    return _safe_error_render(
        request,
        "login/errors_500.html",
        {"message": "Something went wrong on our end."},
        status=500,
    )
