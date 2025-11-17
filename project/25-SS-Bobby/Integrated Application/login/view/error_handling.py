"""
===============================================================================
Module: Error Management
===============================================================================

Author:
    Arundas Mohandas
    
Functionality:
    Error handiling

===============================================================================
"""

import logging
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import SuspiciousOperation
from django.db import DatabaseError
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.views.decorators.cache import never_cache

logger = logging.getLogger(__name__)


def safe_render(request, template_name, context=None, *, status=200):

    context = context or {}
    try:
        return render(request, template_name, context, status=status)
    except TemplateDoesNotExist:
        logger.error("Template not found: %s", template_name, exc_info=True)
        return HttpResponseServerError(
            "<h1>Server Error</h1><p>Required page is temporarily unavailable.</p>"
        )
    except Exception:
        logger.exception("Unhandled error during render for template: %s", template_name)
        if template_name != "errors_500.html":
            try:
                return render(
                    request,
                    "errors_500.html",
                    {"message": "Something went wrong." if not settings.DEBUG else "See server logs for details."},
                    status=500,
                )
            except Exception:
                pass
        return HttpResponseServerError("<h1>Server Error</h1>")


def session_required(role_key):

    def decorator(view_func):
        @wraps(view_func)
        @never_cache
        def _wrapped_view(request, *args, **kwargs):
            try:
                if not request.session.get(role_key):
                    request.session.flush()
                    messages.warning(request, "Your session has expired. Please log in again.")
                    return redirect("index")
                return view_func(request, *args, **kwargs)
            except SuspiciousOperation:
                logger.warning("SuspiciousOperation detected for role_key=%s", role_key, exc_info=True)
                request.session.flush()
                messages.error(request, "We detected a problem with your session. Please sign in again.")
                return redirect("index")
            except DatabaseError:
                logger.exception("Database error while processing view: %s", view_func.__name__)
                return safe_render(
                    request,
                    "errors_500.html",
                    {"message": "A database error occurred. Please try again shortly."},
                    status=500,
                )
            except Exception:
                logger.exception("Unhandled error in session_required for view: %s", view_func.__name__)
                msg = "An unexpected error occurred. Please try again." if not settings.DEBUG else "Unexpected error (see logs)."
                return safe_render(request, "errors_500.html", {"message": msg}, status=500)
        return _wrapped_view
    return decorator
